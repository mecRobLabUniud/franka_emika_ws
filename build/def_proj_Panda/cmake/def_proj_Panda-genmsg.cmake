# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "def_proj_Panda: 0 messages, 3 services")

set(MSG_I_FLAGS "-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(def_proj_Panda_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_custom_target(_def_proj_Panda_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "def_proj_Panda" "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" ""
)

get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_custom_target(_def_proj_Panda_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "def_proj_Panda" "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" ""
)

get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_custom_target(_def_proj_Panda_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "def_proj_Panda" "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_cpp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_cpp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda
)

### Generating Module File
_generate_module_cpp(def_proj_Panda
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(def_proj_Panda_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(def_proj_Panda_generate_messages def_proj_Panda_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_cpp _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_cpp _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_cpp _def_proj_Panda_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(def_proj_Panda_gencpp)
add_dependencies(def_proj_Panda_gencpp def_proj_Panda_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS def_proj_Panda_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_eus(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_eus(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda
)

### Generating Module File
_generate_module_eus(def_proj_Panda
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(def_proj_Panda_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(def_proj_Panda_generate_messages def_proj_Panda_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_eus _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_eus _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_eus _def_proj_Panda_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(def_proj_Panda_geneus)
add_dependencies(def_proj_Panda_geneus def_proj_Panda_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS def_proj_Panda_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_lisp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_lisp(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda
)

### Generating Module File
_generate_module_lisp(def_proj_Panda
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(def_proj_Panda_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(def_proj_Panda_generate_messages def_proj_Panda_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_lisp _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_lisp _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_lisp _def_proj_Panda_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(def_proj_Panda_genlisp)
add_dependencies(def_proj_Panda_genlisp def_proj_Panda_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS def_proj_Panda_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services
_generate_srv_nodejs(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_nodejs(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_nodejs(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda
)

### Generating Module File
_generate_module_nodejs(def_proj_Panda
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(def_proj_Panda_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(def_proj_Panda_generate_messages def_proj_Panda_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_nodejs _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_nodejs _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_nodejs _def_proj_Panda_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(def_proj_Panda_gennodejs)
add_dependencies(def_proj_Panda_gennodejs def_proj_Panda_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS def_proj_Panda_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_py(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda
)
_generate_srv_py(def_proj_Panda
  "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda
)

### Generating Module File
_generate_module_py(def_proj_Panda
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(def_proj_Panda_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(def_proj_Panda_generate_messages def_proj_Panda_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_py _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/FlagStop.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_py _def_proj_Panda_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/def_proj_Panda/srv/CalcValidTraj.srv" NAME_WE)
add_dependencies(def_proj_Panda_generate_messages_py _def_proj_Panda_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(def_proj_Panda_genpy)
add_dependencies(def_proj_Panda_genpy def_proj_Panda_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS def_proj_Panda_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/def_proj_Panda
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(def_proj_Panda_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/def_proj_Panda
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(def_proj_Panda_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/def_proj_Panda
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(def_proj_Panda_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/def_proj_Panda
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(def_proj_Panda_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/def_proj_Panda
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(def_proj_Panda_generate_messages_py std_msgs_generate_messages_py)
endif()
