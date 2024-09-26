# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/home/panda/franka_emika_ws/src/libfranka/include".split(';') if "${prefix}/include;/home/panda/franka_emika_ws/src/libfranka/include" != "" else []
PROJECT_CATKIN_DEPENDS = "controller_interface;dynamic_reconfigure;eigen_conversions;franka_hw;franka_gripper;geometry_msgs;hardware_interface;tf;tf_conversions;message_runtime;pluginlib;realtime_tools;roscpp".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lfranka_example_controllers;/home/panda/franka_emika_ws/src/libfranka/build/libfranka.so.0.8.0".split(';') if "-lfranka_example_controllers;/home/panda/franka_emika_ws/src/libfranka/build/libfranka.so.0.8.0" != "" else []
PROJECT_NAME = "franka_example_controllers"
PROJECT_SPACE_DIR = "/home/panda/franka_emika_ws/install"
PROJECT_VERSION = "0.8.0"
