// Server side implementation of UDP client-server model
#include <bits/stdc++.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <fstream>

#define PORT 8080
#define MAXLINE 1024


Eigen::Matrix<float, 3, 1> nearest_point(Eigen::Vector3f end1, Eigen::Vector3f end2, Eigen::Matrix<float, 3, 1> ext){
	Eigen::Matrix<float, 3, 1> p;
	float t;
	t = -((end1-ext).dot((end2-end1)))/((end2-end1).dot((end2-end1)));
	t = std::max(std::min(t,1.0f),0.0f);
	p << end1 + t * (end2 - end1);
	return p;
}


// Driver code
int main() {
	int sockfd;
	float buffer[MAXLINE];
    //int length = 1024;
	struct sockaddr_in servaddr, cliaddr;
	
	// Creating socket file descriptor
	if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}
	
	memset(&servaddr, 0, sizeof(servaddr));
	memset(&cliaddr, 0, sizeof(cliaddr));
	
	// Filling server information
	servaddr.sin_family = AF_INET; // IPv4
	servaddr.sin_addr.s_addr = INADDR_ANY;
	servaddr.sin_port = htons(PORT);
	
	// Bind the socket with the server address
	if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
		perror("bind failed");
		exit(EXIT_FAILURE);
	}
	
	socklen_t len;
	int n;

	len = sizeof(cliaddr);

	Eigen::Matrix4f R_base2cam, R_cam2base;
	float t;
	std::ifstream myfile ("/home/panda/Documents/Data_Collision_Avoidance/rotation_matrix.txt");
	if (myfile.is_open()){
		for (int row = 0; row < 4; row++){
			for (int col = 0; col < 4; col++){
				myfile >> t;
				R_base2cam(row, col) = t;
			}
		}
		myfile.close();
	}

	R_cam2base = R_base2cam.inverse();
	std::cout << "Camera-to-robot base rotation matrix:" << std::endl;
	std::cout << R_cam2base << std::endl;

	std::cout << std::endl << "Waiting for data.." << std::endl;

	//bodyparts:
	Eigen::Matrix<float, 15, 3> keypoints;
	Eigen::Vector4f omg_vect;
	float t_curr;
	float t_0;
	float temp;
	int do_once = 0;
	Eigen::Vector3f ee_pos, temp_close, repul_final;
	repul_final << 10.0, 10.0, 10.0;

	std::ofstream outfile_skel("/home/panda/Documents/Data_Collision_Avoidance/skeleton_coords.xml");
	if (outfile_skel.is_open()){
		outfile_skel << "<skeleton>" << std::endl;
	}

	std::ofstream outfile_temp;

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
    
    while (true){
        n = recvfrom(sockfd, (float *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr, &len);
        buffer[n] = '\0';

		if (do_once++ == 0){
			t_0 = buffer[4];
		}

		omg_vect << buffer[1], buffer[3], -buffer[2], 1.0; //attenzione e stato cambiata l'orientazione in [x z -y]
		t_curr = buffer[4] - t_0;

		if (!std::isnan(buffer[1]) && !std::isnan(buffer[2]) && !std::isnan(buffer[3])){
			keypoints(static_cast<int>(buffer[0]), 0) = (R_cam2base*omg_vect).head(3)[0];
			keypoints(static_cast<int>(buffer[0]), 1) = (R_cam2base*omg_vect).head(3)[1];
			keypoints(static_cast<int>(buffer[0]), 2) = (R_cam2base*omg_vect).head(3)[2];
		} else{
			keypoints(static_cast<int>(buffer[0]), 0) = std::nanf("0");
			keypoints(static_cast<int>(buffer[0]), 1) = std::nanf("0");
			keypoints(static_cast<int>(buffer[0]), 2) = std::nanf("0");
		}
		
		if (outfile_skel.is_open()){
			if (static_cast<int>(buffer[0]) == 0){
				outfile_skel << "\t" << "<keypoint time='" << t_curr << "'>" << std::endl;
			}
			outfile_skel << "\t\t" << "<point id='" << buffer[0] << "'>" << keypoints(static_cast<int>(buffer[0]), 0) << " " << keypoints(static_cast<int>(buffer[0]), 1) << " " << keypoints(static_cast<int>(buffer[0]), 2) << "</point>" << std::endl;
			if (static_cast<int>(buffer[0]) == 14){
				outfile_skel << "\t" << "</keypoint>" << std::endl;
			}
		}

		if (static_cast<int>(buffer[0]) == 0){
			outfile_temp.open("/home/panda/Documents/Data_Collision_Avoidance/skeleton_temp.txt");
		}
		if (outfile_temp.is_open()){
			outfile_temp << buffer[0] << "\t" << keypoints(static_cast<int>(buffer[0]), 0) << "\t" << keypoints(static_cast<int>(buffer[0]), 1) << "\t" << keypoints(static_cast<int>(buffer[0]), 2) << "\t" << std::endl;
			if (static_cast<int>(buffer[0]) == 14){
				outfile_temp.close();
			}
		}

		std::cout << buffer[0] << " " << keypoints(static_cast<int>(buffer[0]), 0) << " " << keypoints(static_cast<int>(buffer[0]), 1) << " " << keypoints(static_cast<int>(buffer[0]), 2) << std::endl;
	
		if (static_cast<int>(buffer[0]) == 14){
			int j = 0;
			std::ifstream myfile ("/home/panda/Documents/Data_Collision_Avoidance/ee_pos.txt");
			if (myfile.is_open()){
				while (myfile >> temp){
					ee_pos(j++) = temp;
				}
				myfile.close();
			}
			
			// calculates the closest keypoint
			for (int i = 0; i < 10; i++){
				Eigen::Vector3f joint_1;
				Eigen::Vector3f joint_2;

				int ind_1 = skel_index[i][0];
				int ind_2 = skel_index[i][1];
				joint_1 << keypoints(ind_1, 0), keypoints(ind_1, 1), keypoints(ind_1, 2);
				joint_2 << keypoints(ind_2, 0), keypoints(ind_2, 1), keypoints(ind_2, 2);

				temp_close = nearest_point(joint_1, joint_2, ee_pos);
				if (!std::isnan(temp_close[0]) && !std::isnan(temp_close[1]) && !std::isnan(temp_close[2])){
					if ((ee_pos - temp_close).norm() < (repul_final - ee_pos).norm()){
						repul_final << temp_close;
					}
				}
			}

			std::cout << "repul final: " << repul_final << std::endl;

			std::ofstream outfile_repul("/home/panda/Documents/Data_Collision_Avoidance/repul_pos.txt");
			if (outfile_repul.is_open()){
				for (int i = 0; i < 3; i++){
					outfile_repul << repul_final[i] << std::endl;
				}
				outfile_repul.close();
			}

			repul_final << 10.0, 10.0, 10.0;
		}
    }
	
	if (outfile_skel.is_open()){
		outfile_skel << "</skeleton>" << std::endl;
	}
	
	outfile_skel.close();

	return 0;
}
