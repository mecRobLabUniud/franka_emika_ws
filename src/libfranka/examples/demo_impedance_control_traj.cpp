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

Eigen::MatrixXd Ax(6,1);
Eigen::MatrixXd Ay(6,1);
Eigen::MatrixXd Az(6,1);
Eigen::MatrixXd Ax_stop(6,1);
Eigen::MatrixXd Ay_stop(6,1);
Eigen::MatrixXd Az_stop(6,1);


Eigen::Matrix<float, 3, 1> nearest_point(Eigen::Vector3f end1, Eigen::Vector3f end2, Eigen::Matrix<float, 3, 1> ext){
	Eigen::Matrix<float, 3, 1> p;
	float t;
	t = -((end1-ext).dot((end2-end1)))/((end2-end1).dot((end2-end1)));
	t = std::max(std::min(t,1.0f),0.0f);
	p << end1 + t * (end2 - end1);
	return p;
}


Eigen::MatrixXd trajectory_coef(float t0, float tf, std::vector<double> x0, std::vector<double> xf){

	Eigen::MatrixXd X(6,6);
	X << 1,t0,std::pow(t0,2),std::pow(t0,3),std::pow(t0,4),std::pow(t0,5),
		   0,1,2*t0,3*std::pow(t0,2),4*std::pow(t0,3),5*std::pow(t0,4),
		   0,0,2,6*t0,12*std::pow(t0,2),20*std::pow(t0,3),
	     1,tf,std::pow(tf,2),std::pow(tf,3),std::pow(tf,4),std::pow(tf,5),
		   0,1,2*tf,3*std::pow(tf,2),4*std::pow(tf,3),5*std::pow(tf,4),
		   0,0,2,6*tf,12*std::pow(tf,2),20*std::pow(tf,3);
		 
	Eigen::MatrixXd B(6,1);
	B << x0[0],x0[1],x0[2],xf[0],xf[1],xf[2];
    
	return (X.inverse()*B);
}


void trajectory_updater(Eigen::Matrix<double, 3, 1> &xd, Eigen::Matrix<double, 6, 1> &dxd, Eigen::Matrix<double, 6, 1> &ddxd, double t, double t_start, Eigen::MatrixXd Ax, Eigen::MatrixXd Ay, Eigen::MatrixXd Az){
	//update x_d
	xd[0] = Ax(0) + Ax(1)*(t-t_start) + Ax(2)*std::pow((t-t_start),2) + Ax(3)*std::pow((t-t_start),3) + Ax(4)*std::pow((t-t_start),4) + Ax(5)*std::pow((t-t_start),5);
	xd[1] = Ay(0) + Ay(1)*(t-t_start) + Ay(2)*std::pow((t-t_start),2) + Ay(3)*std::pow((t-t_start),3) + Ay(4)*std::pow((t-t_start),4) + Ay(5)*std::pow((t-t_start),5);
	xd[2] = Az(0) + Az(1)*(t-t_start) + Az(2)*std::pow((t-t_start),2) + Az(3)*std::pow((t-t_start),3) + Az(4)*std::pow((t-t_start),4) + Az(5)*std::pow((t-t_start),5);
	//update dx_d
	dxd[0] = Ax(1) + 2*Ax(2)*(t-t_start) + 3*Ax(3)*std::pow((t-t_start),2) + 4*Ax(4)*std::pow((t-t_start),3) + 5*Ax(5)*std::pow((t-t_start),4);
	dxd[1] = Ay(1) + 2*Ay(2)*(t-t_start) + 3*Ay(3)*std::pow((t-t_start),2) + 4*Ay(4)*std::pow((t-t_start),3) + 5*Ay(5)*std::pow((t-t_start),4);
	dxd[2] = Az(1) + 2*Az(2)*(t-t_start) + 3*Az(3)*std::pow((t-t_start),2) + 4*Az(4)*std::pow((t-t_start),3) + 5*Az(5)*std::pow((t-t_start),4);
	dxd.tail(3) << 0.0,0.0,0.0;
	//update ddx_d
	ddxd[0] = 2*Ax(2) + 6*Ax(3)*(t-t_start) + 12*Ax(4)*std::pow((t-t_start),2) + 20*Ax(5)*std::pow((t-t_start),3);
	ddxd[1] = 2*Ay(2) + 6*Ay(3)*(t-t_start) + 12*Ay(4)*std::pow((t-t_start),2) + 20*Ay(5)*std::pow((t-t_start),3);
	ddxd[2] = 2*Az(2) + 6*Az(3)*(t-t_start) + 12*Az(4)*std::pow((t-t_start),2) + 20*Az(5)*std::pow((t-t_start),3);
	ddxd.tail(3) << 0.0,0.0,0.0;
}


void trajectory_manager(Eigen::Matrix<double, 3, 1> &xd, Eigen::Matrix<double, 6, 1> &dxd, Eigen::Matrix<double, 6, 1> &ddxd, double t, Eigen::Vector3d pos0, Eigen::Matrix<double, 3, 1> d_pos, bool flag_stop, std::vector<std::vector<double>> p_traj, std::vector<double> t_traj){
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
          trajectory_updater(xd, dxd, ddxd, t, t_stop_init, Ax_stop, Ay_stop, Az_stop);
        } else{
          xd << pos_stop;
	        dxd << 0.0;
	        ddxd << 0.0;
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
      
      trajectory_updater(xd, dxd, ddxd, t, t_start, Ax, Ay, Az);
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
	std::ofstream outfile_q("/home/panda/Documents/Data_Collision_Avoidance/demo_impedance_control/q_robot.xml");
  if (outfile_q.is_open()){
		outfile_q << "<q>" << std::endl;
	}

  // Read virtual skeleton coordinates from file
  std::fstream outfile_skel("/home/panda/Documents/Data_Collision_Avoidance/skeleton_coords.xml");

  // Write distance segment
  std::fstream outfile_dist("/home/panda/Documents/Data_Collision_Avoidance/demo_impedance_control/dist_segment.xml");
  if (outfile_dist.is_open()){
		outfile_dist << "<distance>" << std::endl;
	}

  std::string read;
  std::string line;
  std::string time_str;
  float skel_time;
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
  Eigen::Vector3d pos;
  const double translational_stiffness{400.0};
  const double rotational_stiffness{50.0};
  Eigen::MatrixXd stiffness(6, 6), damping(6, 6), mass(6,6);
  stiffness.setZero();
  stiffness.topLeftCorner(3, 3) << translational_stiffness * Eigen::MatrixXd::Identity(3, 3);
  stiffness.bottomRightCorner(3, 3) << rotational_stiffness * Eigen::MatrixXd::Identity(3, 3);
  damping.setZero();
  damping.topLeftCorner(3, 3) << 2.0 * sqrt(translational_stiffness) * Eigen::MatrixXd::Identity(3, 3);
  damping.bottomRightCorner(3, 3) << 2.0 * sqrt(rotational_stiffness) * Eigen::MatrixXd::Identity(3, 3);
  mass.setZero();
  double t_exe = 0;

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
    Eigen::Affine3d initial_transform(Eigen::Matrix4d::Map(initial_state.O_T_EE.data()));
    Eigen::Vector3d pos_init(initial_transform.translation());
    Eigen::Quaterniond ori_d(initial_transform.rotation());
    
    // setting various parameters
    Eigen::Matrix<double, 3, 1> x_d, x_d_old, x_fin;
    Eigen::Matrix<double, 6, 1> dx_d, dx_d_old, ddx_d, error, dx;
    Eigen::Matrix<double, 6, 7> dJ, J_old;
    Eigen::Matrix<double, 7, 6> J_pseinv;
    Eigen::MatrixXd k_caps(6, 6);
    bool isClose = false;
    k_caps.setZero();
    k_caps.topLeftCorner(3, 3) <<  1800.0 * Eigen::MatrixXd::Identity(3, 3);
    Eigen::Matrix<double, 3, 1> pos_repul;
    double dim_caps = 0.6;
    double dim_inner_caps = 0.1;
    Eigen::Matrix<double, 6, 1> dist_repul, f_repul;
    f_repul.setZero();
    std::array<double, 42> jacobian_array = model.zeroJacobian(franka::Frame::kEndEffector, initial_state);
    Eigen::Map<const Eigen::Matrix<double, 6, 7>> J(jacobian_array.data());
    Eigen::Map<const Eigen::Matrix<double, 7, 1>> tau_ext_init(initial_state.tau_ext_hat_filtered.data());
    float read;
    std::string read_str;
    std::string c_read;
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

    // set collision behavior
    robot.setCollisionBehavior({{100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0}},
                               {{100.0, 100.0, 100.0, 100.0, 100.0, 100.0}});

    // define callback for the torque control loop
    std::function<franka::Torques(const franka::RobotState&, franka::Duration)>
        impedance_control_callback = [&](const franka::RobotState& state,
                                         franka::Duration duration) -> franka::Torques {

      //auto start = std::chrono::steady_clock::now();
      // get state variables
      std::array<double, 7> coriolis_array = model.coriolis(state);
      std::array<double, 49> mass_array = model.mass(state);
      std::array<double, 42> jacobian_array = model.zeroJacobian(franka::Frame::kEndEffector, state);

      Eigen::Map<const Eigen::Matrix<double, 7, 1>> coriolis(coriolis_array.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 7>> B(mass_array.data());
      Eigen::Map<const Eigen::Matrix<double, 6, 7>> J(jacobian_array.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 1>> q(state.q.data());
      Eigen::Map<const Eigen::Matrix<double, 7, 1>> dq(state.dq.data());
      
      Eigen::Affine3d transform(Eigen::Matrix4d::Map(state.O_T_EE.data()));
      Eigen::Vector3d pos(transform.translation());
      Eigen::Quaterniond ori(transform.rotation());

	    dx << J*dq;
      
      double dt = duration.toSec();
      t_exe += dt;

      temp_int = int (t_exe*1000);
      //std::cout << "tempo int: " << temp_int << std::endl;

      mass << (J * B.inverse() * J.transpose()).inverse();
      damping << 2.0 * (stiffness.array() * mass.array()).cwiseSqrt();

      // Write joints configuration
			if (outfile_q.is_open()){
        outfile_q << "\t" << "<point time='" << t_exe << "'>" << q[0] << " " << q[1] << " " << q[2] << " " << q[3] << " " << q[4] << " " << q[5] << " " << q[6] << " " << "</point>" << std::endl;
			}

      // write ee_pose
			std::ofstream outfile("/home/panda/Documents/Data_Collision_Avoidance/ee_pos.txt");
			if (outfile.is_open()){
				for (int i = 0; i < 3; i++){
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

                pos_repul << repul_final[0], repul_final[1], repul_final[2];

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
    
      // check if the inner security capsule has been breached
      if (dist_repul.head(3).norm() < dim_inner_caps){
        isClose = true;
      } else{
        isClose = false;
      }
      
      // compute repulsion force
      dist_repul.head(3) << pos_repul - pos;
      dist_repul.tail(3) << 0.0,0.0,0.0;
      if ((dist_repul.head(3).norm() < dim_caps) && (isClose == false)){
        f_repul << -k_caps * (dim_caps - dist_repul.norm())*(dist_repul / dist_repul.norm());
        tau_repul << J.transpose() * f_repul;
      } else{
        tau_repul << 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0;
      }
      
      std::cout << "pos_repul: " << pos_repul[0] << " " << pos_repul[1] << " " << pos_repul[2] << std::endl;
      std::cout << "pos_ee: " << pos[0] << " " << pos[1] << " " << pos[2] << std::endl;
      std::cout << "distance: " << dist_repul.head(3).norm() << std::endl;
      std::cout << std::endl;

      // getting the desired trajectory x_d and its speed and acceleration
      trajectory_manager(x_d, dx_d, ddx_d, t_exe, pos, dx.head(3), isClose, p_traj, t_traj);
      
      // calculating the derivative of the jacobian and its pseudo-inverse
      if ( dt != 0 ){
        dJ = ( J - J_old ) / dt;
      } else{
        dJ << 0.0;
      }
      J_old = J;
      
      J_pseinv = J.transpose() * (J * J.transpose()).inverse();

      // compute error to desired equilibrium pose
      // position error
      error.head(3) << pos - x_d.head(3); 

      // saturation of the position error
      for (int i = 0; i < 3; i++){
        error[i] = std::max(std::min(error[i],0.08),-0.08);
      }
      
      // orientation error
      // "difference" quaternion
      if (ori_d.coeffs().dot(ori.coeffs()) < 0.0){
        ori.coeffs() << -ori.coeffs();
      }
      // "difference" quaternion
      Eigen::Quaterniond error_quaternion(ori.inverse() * ori_d);
      error.tail(3) << error_quaternion.x(), error_quaternion.y(), error_quaternion.z();
      // Transform to base frame
      error.tail(3) << -transform.rotation() * error.tail(3);

      // compute control
      tau_task << B * J_pseinv * (ddx_d - dJ * dq) + J.transpose() * ( - stiffness * error + damping *(dx_d - (J * dq)));
           
      tau_d << tau_task + coriolis + tau_repul + tau_ext_init;

      std::array<double, 7> tau_d_array{};
      Eigen::VectorXd::Map(&tau_d_array[0], 7) = tau_d;

      if (t_exe >= t_traj.back()){
        std::cout << "Trajectory completed, " << t_traj.back() << " seconds has passed, shutting down example" << std::endl;
        robot.stop();
      }
	  
      return tau_d_array;
    };

    // start real-time control loop
    std::cout << "WARNING: Collision thresholds are set to high values. "
              << "Make sure you have the user stop at hand!" << std::endl
              << "This will start the impedance control task" << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();
    
    robot.control(impedance_control_callback);
    
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
