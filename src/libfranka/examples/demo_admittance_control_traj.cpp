#include <array>
#include <cmath>
#include <functional>
#include <iostream>
#include <fstream>
#include <mutex>
#include <Eigen/Dense>
#include <franka/duration.h>
#include <franka/exception.h>
#include <franka/model.h>
#include <franka/robot.h>
#include "examples_common.h"

// real cartesian impedance control + repulsion point from skeleton tracking + inner capsule stoppage (final version)

// admittance control - real admittance control with repulsion point

Eigen::MatrixXd Ax (6,1);
Eigen::MatrixXd Ay (6,1);
Eigen::MatrixXd Az (6,1);
Eigen::MatrixXd Ax_stop (6,1);
Eigen::MatrixXd Ay_stop (6,1);
Eigen::MatrixXd Az_stop (6,1);


Eigen::Matrix<float, 3, 1> nearest_point(Eigen::Vector3f end1, Eigen::Vector3f end2, Eigen::Matrix<float, 3, 1> ext){
	Eigen::Matrix<float, 3, 1> p;
	float t;
	t = -((end1-ext).dot((end2-end1)))/((end2-end1).dot((end2-end1)));
	t = std::max(std::min(t,1.0f),0.0f);
	p << end1 + t * (end2 - end1);
	return p;
}


Eigen::MatrixXd trajectory_coef(float t0, float tf, std::vector<double> x0, std::vector<double> xf){

	Eigen::MatrixXd X (6,6);
	X << 1,t0,std::pow(t0,2),std::pow(t0,3),std::pow(t0,4),std::pow(t0,5),
		   0,1,2*t0,3*std::pow(t0,2),4*std::pow(t0,3),5*std::pow(t0,4),
		   0,0,2,6*t0,12*std::pow(t0,2),20*std::pow(t0,3),
	     1,tf,std::pow(tf,2),std::pow(tf,3),std::pow(tf,4),std::pow(tf,5),
		   0,1,2*tf,3*std::pow(tf,2),4*std::pow(tf,3),5*std::pow(tf,4),
		   0,0,2,6*tf,12*std::pow(tf,2),20*std::pow(tf,3);
		 
    Eigen::MatrixXd B (6,1);
    B << x0[0],x0[1],x0[2],xf[0],xf[1],xf[2];
    
	return (X.inverse()*B);
}


void trajectory_updater(Eigen::Matrix<double, 3, 1> &xd, double t, double t_start, Eigen::MatrixXd Ax, Eigen::MatrixXd Ay, Eigen::MatrixXd Az){
	//update x_d
	xd[0] = Ax(0) + Ax(1)*(t-t_start) + Ax(2)*std::pow((t-t_start),2) + Ax(3)*std::pow((t-t_start),3) + Ax(4)*std::pow((t-t_start),4) + Ax(5)*std::pow((t-t_start),5);
	xd[1] = Ay(0) + Ay(1)*(t-t_start) + Ay(2)*std::pow((t-t_start),2) + Ay(3)*std::pow((t-t_start),3) + Ay(4)*std::pow((t-t_start),4) + Ay(5)*std::pow((t-t_start),5);
	xd[2] = Az(0) + Az(1)*(t-t_start) + Az(2)*std::pow((t-t_start),2) + Az(3)*std::pow((t-t_start),3) + Az(4)*std::pow((t-t_start),4) + Az(5)*std::pow((t-t_start),5);
}


void trajectory_manager(Eigen::Matrix<double, 3, 1> &xd, double t, Eigen::Vector3d pos0, Eigen::Matrix<double, 3, 1> d_pos, bool flag_stop, std::vector<std::vector<double>> p_traj, std::vector<double> t_traj){
  static float t_stop = 0.0;
  static float t_stop_init = 0.0;
  static float t_stop_prec = 0.0;
  static float t_traj_stop = 0.0;
  static Eigen::Vector3d pos_stop;
  static std::vector<double> prova;
  static Eigen::Vector3d pos_des;

  for (int i = 0; i <= static_cast<int>(t_traj.size()); i++){
    if (t <= t_traj[i]){
      if (flag_stop == true){
        static int do_once_stop;

        if (do_once_stop++ == 0){
          pos_stop << pos0;
          t_stop_init = t;
          t_stop_prec = t_stop;
          t_traj_stop = 0.4;
          std::vector<double> x0x = {pos0[0], d_pos[0], 0.0};
          std::vector<double> xfx = {pos_stop(0), 0.0, 0.0};
          std::vector<double> x0y = {pos0[1], d_pos[1], 0.0};
          std::vector<double> xfy = {pos_stop(1), 0.0, 0.0};
          std::vector<double> x0z = {pos0[2], d_pos[2], 0.0};
          std::vector<double> xfz = {pos_stop(2), 0.0, 0.0};
          Ax_stop = trajectory_coef(0.0, t_traj_stop, x0x, xfx);
          Ay_stop = trajectory_coef(0.0, t_traj_stop, x0y, xfy);
          Az_stop = trajectory_coef(0.0, t_traj_stop, x0z, xfz);
        }

        if ((t - t_stop_init) < t_traj_stop){
          trajectory_updater(xd, t, t_stop_init, Ax_stop, Ay_stop, Az_stop);
        } else{
          xd << pos_stop;
        }

        t_stop = t - t_stop_init + t_stop_prec;
        return;
      }

      float t_start = (t_traj[i-1] < t_traj[i]) ? t_traj[i-1] : 0;
      
      static int do_once;
      if (do_once == i){
        pos_des << p_traj[i][0], p_traj[i][1], p_traj[i][2];

        std::vector<double> x0x = {pos0[0], d_pos[0], 0.0};
        std::vector<double> xfx = {pos_des[0], 0.0, 0.0};
        std::vector<double> x0y = {pos0[1], d_pos[1], 0.0};
        std::vector<double> xfy = {pos_des[1], 0.0, 0.0};
        std::vector<double> x0z = {pos0[2], d_pos[2], 0.0};
        std::vector<double> xfz = {pos_des[2], 0.0, 0.0};
        Ax = trajectory_coef(0.0, t_traj[i] - t_start, x0x, xfx);
        Ay = trajectory_coef(0.0, t_traj[i] - t_start, x0y, xfy);
        Az = trajectory_coef(0.0, t_traj[i] - t_start, x0z, xfz);

        do_once++;
      }

      trajectory_updater(xd, t, t_start, Ax, Ay, Az);
      return;
    }
  }
}



int main(int argc, char** argv){
  // Check whether the required arguments were passed
  bool virtual_skel;
  if (argc < 2){
    std::cerr << "Usage: " << argv[0] << " <robot-hostname>" << std::endl;
    return -1;
  }
  if (argc > 2){
    std::string arg = argv[2];
    virtual_skel = (arg == "virt") ? true : false;
  } else{
    virtual_skel = false;
  }

  // Read and create p_traj and t_traj vector with robot waypoint configuration
  std::vector<std::vector<double>> p_traj;
  std::vector<double> t_traj;

  std::ifstream infile("/home/panda/Desktop/demo/collision_avoidance/p_traj.txt");
  // Checking whether the file is open.
  if (infile.is_open()){ 
    std::string row;
    std::vector<double> row_temp;
    std::string elem_temp;      

    while (std::getline(infile, row)){
      std::stringstream row_str(row);
      while (row_str >> elem_temp){
        row_temp.push_back(std::stod(elem_temp));
      }
      p_traj.push_back(row_temp);
      row_temp.clear();
    }

    infile.close(); 
  }

  infile.open("/home/panda/Desktop/demo/collision_avoidance/t_traj.txt");
  // Checking whether the file is open.
  if (infile.is_open()){ 
    std::string row;      
    while (std::getline(infile, row)){
      t_traj.push_back(std::stod(row));
    }
    infile.close(); 
  }

  // Write joints configuration
	std::ofstream outfile_q("/home/panda/Documents/Data_Collision_Avoidance/demo_admittance_control/q_robot.xml");
  if (outfile_q.is_open()){
		outfile_q << "<q>" << std::endl;
	}

  // Read virtual skeleton coordinates from file
  std::fstream outfile_skel("/home/panda/Documents/Data_Collision_Avoidance/skeleton_coords.xml");

  // Write distance segment
  std::fstream outfile_dist("/home/panda/Documents/Data_Collision_Avoidance/demo_admittance_control/dist_segment.xml");
  if (outfile_dist.is_open()){
		outfile_dist << "<distance>" << std::endl;
	}

  std::string read;
  std::string line;
  std::string time_str;
  float skel_time = 0;
  Eigen::Matrix<float, 15, 3> keypoint;
  Eigen::Vector3f ee_pos, temp_close, repul_final;
  repul_final << 10.0, 10.0, 10.0;

  std::vector<std::vector<int>> skel_index;
	skel_index.push_back({0, 1});
	skel_index.push_back({2, 3});
	skel_index.push_back({3, 4});
	skel_index.push_back({5, 6});
	skel_index.push_back({6, 7});
	skel_index.push_back({1, 8});
	skel_index.push_back({9, 10});
	skel_index.push_back({10, 11});
	skel_index.push_back({12, 13});
	skel_index.push_back({13, 14});

  // Compliance parameters
  double t_exe = 0.0;
  std::array<double, 16> pos_actual;
  Eigen::Matrix<double, 6, 1> dx;
  Eigen::Matrix<double, 3, 1> x_d;
  Eigen::Vector3d pos, pos_admit, f_ext, f_ee, f_ee_init;
  Eigen::VectorXd X_state(6);
  X_state.setZero();
  Eigen::MatrixXd A(6, 6), Ad(6,6);
  Eigen::MatrixXd B(6, 3), Bd(6,3);
  Eigen::MatrixXd C(3, 6), Cd(3,6);
  Eigen::MatrixXd D(3, 3), Dd(3,3);
  Eigen::MatrixXd stiff(3, 3), damp(3,3), mass(3,3);
  A.setZero();
  B.setZero();
  C.setZero();
  D.setZero();
  Ad.setZero();
  Bd.setZero();
  Cd.setZero();
  Dd.setZero();
  stiff.setZero();
  double k_stiff = 600.0;
  stiff << k_stiff * Eigen::MatrixXd::Identity(3, 3);
  damp.setZero();
  //damp << (2.0 * sqrt(k_stiff)) * Eigen::MatrixXd::Identity(3, 3);
  mass.setZero();
  Eigen::MatrixXd k_caps(3, 3);
  bool isClose = false;
  k_caps.setZero();
  k_caps <<  1200.0 * Eigen::MatrixXd::Identity(3, 3);
  double dim_caps = 0.6;
  double dim_inner_caps = 0.1;
  Eigen::Matrix<double, 3, 1> dist_repul, f_repul;
  f_repul.setZero();

  try{
    // connect to robot
    franka::Robot robot(argv[1]);
    setDefaultBehavior(robot);
    // setting the end-effector load
    robot.setLoad(0.73,{-0.01,0,0.03},{0.001,0,0,0,0.0025,0,0,0,0.0017});

    // move the robot to a start joint configuration
    std::array<double, 7> q_start = {{0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4}};
    MotionGenerator motion_generator(0.3, q_start);
    std::cout << "WARNING: This example will move the robot! "
              << "Please make sure to have the user stop button at hand!" << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();
    robot.control(motion_generator);
    std::cout << "Finished moving to initial joint configuration." << std::endl;    

    franka::Model model = robot.loadModel();
    
    franka::RobotState initial_state = robot.readOnce();
    std::array<double, 16> pos_matrix = initial_state.O_T_EE_c;    
    
    // setting various parameters
    std::array<double, 42> jacobian_array = model.zeroJacobian(franka::Frame::kEndEffector, initial_state);
    Eigen::Map<const Eigen::Matrix<double, 6, 7>> J(jacobian_array.data());
    Eigen::Map<const Eigen::Matrix<double, 7, 1>> tau_ext(initial_state.tau_ext_hat_filtered.data());
    f_ee_init << (J * tau_ext).head(3);
    Eigen::Matrix<double, 3, 1> pos_repul;
    float read;
    std::string read_str;
    std::fstream repulfile;
    int temp_int;

    std::ofstream outfile("/home/panda/Documents/Data_Collision_Avoidance/repul_pos.txt");
    if (outfile.is_open()){
      for (int i=0;i<3;i++){
        outfile << 100.0 << std::endl;  //dummy values
      }
      outfile.close();
    }
 
    Eigen::VectorXd tau_task(7), tau_d(7), tau_repul(7);
    
    //std::ofstream myfile ("dati_test12_5.txt");

    // set collision behavior
    robot.setCollisionBehavior({{100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0}});

    // define callback for the torque control loop
    std::function<franka::CartesianPose(const franka::RobotState&, franka::Duration)>
        admittance_control_callback = [&](const franka::RobotState& state,
                                         franka::Duration duration) -> franka::CartesianPose {

      //auto start = std::chrono::steady_clock::now();
      // get state variables
      std::array<double, 49> mass_array = model.mass(state);
      std::array<double, 42> jacobian_array = model.zeroJacobian(franka::Frame::kEndEffector, state);

      Eigen::Map<const Eigen::Matrix<double, 7, 7>> M(mass_array.data());
      Eigen::Map<const Eigen::Matrix<double, 6, 7>> J(jacobian_array.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 1>> dq(state.dq.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 1>> q(state.q.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 1>> tau_ext(state.tau_ext_hat_filtered.data());
      
      pos_actual = state.O_T_EE_c;
      pos << pos_actual[12], pos_actual[13], pos_actual[14];   
      dx << J*dq;
      
      double dt = duration.toSec();
      t_exe += dt;

      temp_int = int (t_exe*1000);
      //std::cout << "tempo int: " << temp_int << std::endl;

      // Write joints configuration
			if (outfile_q.is_open()){
        outfile_q << "\t" << "<point time='" << t_exe << "'>" << q[0] << " " << q[1] << " " << q[2] << " " << q[3] << " " << q[4] << " " << q[5] << " " << q[6] << " " << "</point>" << std::endl;
			}

      // Write ee_pose
			std::ofstream outfile("/home/panda/Documents/Data_Collision_Avoidance/ee_pos.txt");
			if (outfile.is_open()){
				for (int i=0;i<3;i++){
					outfile << pos[i] << std::endl;
				}
        outfile.close();
			}

      // Read pos repul
      if (!virtual_skel){
        int k = 0;
        std::ifstream repulfile("/home/panda/Documents/Data_Collision_Avoidance/repul_pos.txt");
        if (repulfile.is_open()){
          while (repulfile >> read){
            pos_repul(k) = read;
            k++;
          }
          repulfile.close();
        }
      } else{
        std::cout << "skel time = " << skel_time << std::endl;
        std::cout << "exe time = " << t_exe << std::endl;
        if (outfile_skel.is_open()){
          if (skel_time <= t_exe){
            while (outfile_skel >> read_str){
              if (read_str == "<keypoint"){
                outfile_skel >> time_str;
                skel_time = stof(time_str.substr(6, time_str.find('>') - 7));
                
                outfile_skel.ignore();
                for (int i = 0; i <= 14; i++){
                  getline(outfile_skel, line);
                  line = line.substr(line.find('>') + 1, line.find("</") - line.find('>') - 1);

                  std::stringstream key_str(line);
                  int j = 0;
                  for(std::string key; getline(key_str, key, ' '); ){
                    keypoint(i, j++) = stof(key);
                  }
                }

                // calculates the closest keypoint
                for (int i = 0; i < 10; i++){
                  Eigen::Vector3f joint_1;
                  Eigen::Vector3f joint_2;

                  int ind_1 = skel_index[i][0];
                  int ind_2 = skel_index[i][1];
                  joint_1 << keypoint(ind_1, 0), keypoint(ind_1, 1), keypoint(ind_1, 2);
                  joint_2 << keypoint(ind_2, 0), keypoint(ind_2, 1), keypoint(ind_2, 2);

                  temp_close = nearest_point(joint_1, joint_2, ee_pos);
                  if (!std::isnan(temp_close[0]) && !std::isnan(temp_close[1]) && !std::isnan(temp_close[2])){
                    if ((ee_pos - temp_close).norm() < (repul_final - ee_pos).norm()){
                      repul_final << temp_close;
                    }
                  }
                }

                //pos_repul << repul_final[0], repul_final[1], repul_final[2];
                pos_repul << 0.4, 0.4, 0.3;

                break;
              }
            }
          }
        }
      }

      if (outfile_dist.is_open()){
        outfile_dist << "\t" << "<keypoint time='" << t_exe << "'>" << std::endl;
        outfile_dist << "\t\t" << "<point id='0'>" << ee_pos[0] << " " << ee_pos[1] << " " << ee_pos[2] << "</point>" << std::endl;
        outfile_dist << "\t\t" << "<point id='1'>" << repul_final[0] << " " << repul_final[1] << " " << repul_final[2] << "</point>" << std::endl;
        outfile_dist << "\t" << "</keypoint>" << std::endl;
      }
      
      std::cout << pos_repul[0] << pos_repul[1] << pos_repul[2] << std::endl;
      // compute repulsion force
      dist_repul << pos_repul - pos;
      if (dist_repul.norm() < dim_caps){
        f_repul << -k_caps * (dim_caps - dist_repul.norm())*(dist_repul / dist_repul.norm());
      } else{
        f_repul << 0.0,0.0,0.0;
      }

      // check if the inner security capsule has been breached
      if (dist_repul.norm() < dim_inner_caps){
        isClose = true;
      } else{
        isClose = false;
      }

      std::cout << "pos_repul: " << pos_repul[0] << " " << pos_repul[1] << " " << pos_repul[2] << std::endl;
      std::cout << "pos_ee: " << pos[0] << " " << pos[1] << " " << pos[2] << std::endl;
      std::cout << "distance: " << dist_repul.head(3).norm() << std::endl;
      std::cout << std::endl;

      // compute A, B, C, D and their descrete version

      for (int i = 0; i < (int)(dt/0.001); i++){
          mass << ((J * M.inverse() * J.transpose()).inverse()).topLeftCorner(3,3);
          damp << 2.0 * (stiff.array() * mass.array()).cwiseSqrt();
          
          A.topRightCorner(3, 3) << Eigen::MatrixXd::Identity(3, 3);
          A.bottomLeftCorner(3,3) << -stiff * mass.inverse();
          A.bottomRightCorner(3,3) << -damp * mass.inverse();
          B.bottomRows(3) << mass.inverse();
          C.leftCols(3) << Eigen::MatrixXd::Identity(3, 3);
          
          Ad << (Eigen::MatrixXd::Identity(6, 6) + (0.001/2) * A) * (Eigen::MatrixXd::Identity(6, 6) - (0.001/2) * A).inverse();
          Bd << (Eigen::MatrixXd::Identity(6, 6) - (0.001/2) * A).inverse() * B * sqrt(0.001);
          Cd << sqrt(0.001) * C * (Eigen::MatrixXd::Identity(6, 6) - (0.001/2) * A).inverse();
          Dd << D + C * (Eigen::MatrixXd::Identity(6, 6) - (0.001/2) * A).inverse() * B * (0.001/2);

          f_ee << (J * tau_ext).head(3) - f_ee_init;
          //f_ext << f_repul + f_ee;
          f_ext << f_repul;
          //f_ext << 0.0, 0.0, 0.0;
          
          pos_admit << Cd * X_state + Dd * f_ext;
          X_state << Ad * X_state + Bd * f_ext;
      }
      
      // getting the desired trajectory
      trajectory_manager(x_d, t_exe, pos, dx.head(3), isClose, p_traj, t_traj);
 
      pos_matrix[12] = x_d[0] + pos_admit[0];
      pos_matrix[13] = x_d[1] + pos_admit[1];
      pos_matrix[14] = x_d[2] + pos_admit[2];

      if (t_exe >= t_traj.back()){
        std::cout << "Trajectory completed, " << t_traj.back() << " seconds has passed, shutting down example" << std::endl;
        robot.stop();
      }

      return pos_matrix;
    };

    // start real-time control loop
    std::cout << "WARNING: Collision thresholds are set to high values. "
              << "Make sure you have the user stop at hand!" << std::endl
              << "This will start the admittance control task" << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();
    
    robot.control(admittance_control_callback);
    
    if (outfile_q.is_open()){
      outfile_q << "</q>" << std::endl;
    }
    if (outfile_dist.is_open()){
      outfile_dist << "</distance>" << std::endl;
    }
    outfile_q.close();
    outfile_skel.close();
    outfile_dist.close();

  } catch (const franka::Exception& ex){
    // print exception
    std::cout << ex.what() << std::endl;
  }

  return 0;
}
