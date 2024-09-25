# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "Collision_Avoidance: 0 messages, 2 services")

set(MSG_I_FLAGS "-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(Collision_Avoidance_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_custom_target(_Collision_Avoidance_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "Collision_Avoidance" "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" ""
)

get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_custom_target(_Collision_Avoidance_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "Collision_Avoidance" "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Collision_Avoidance
)
_generate_srv_cpp(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Collision_Avoidance
)

### Generating Module File
_generate_module_cpp(Collision_Avoidance
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Collision_Avoidance
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(Collision_Avoidance_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(Collision_Avoidance_generate_messages Collision_Avoidance_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_cpp _Collision_Avoidance_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_cpp _Collision_Avoidance_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Collision_Avoidance_gencpp)
add_dependencies(Collision_Avoidance_gencpp Collision_Avoidance_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Collision_Avoidance_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Collision_Avoidance
)
_generate_srv_eus(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Collision_Avoidance
)

### Generating Module File
_generate_module_eus(Collision_Avoidance
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Collision_Avoidance
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(Collision_Avoidance_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(Collision_Avoidance_generate_messages Collision_Avoidance_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_eus _Collision_Avoidance_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_eus _Collision_Avoidance_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Collision_Avoidance_geneus)
add_dependencies(Collision_Avoidance_geneus Collision_Avoidance_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Collision_Avoidance_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Collision_Avoidance
)
_generate_srv_lisp(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Collision_Avoidance
)

### Generating Module File
_generate_module_lisp(Collision_Avoidance
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Collision_Avoidance
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(Collision_Avoidance_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(Collision_Avoidance_generate_messages Collision_Avoidance_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_lisp _Collision_Avoidance_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_lisp _Collision_Avoidance_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Collision_Avoidance_genlisp)
add_dependencies(Collision_Avoidance_genlisp Collision_Avoidance_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Collision_Avoidance_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services
_generate_srv_nodejs(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Collision_Avoidance
)
_generate_srv_nodejs(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Collision_Avoidance
)

### Generating Module File
_generate_module_nodejs(Collision_Avoidance
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Collision_Avoidance
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(Collision_Avoidance_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(Collision_Avoidance_generate_messages Collision_Avoidance_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_nodejs _Collision_Avoidance_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_nodejs _Collision_Avoidance_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Collision_Avoidance_gennodejs)
add_dependencies(Collision_Avoidance_gennodejs Collision_Avoidance_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Collision_Avoidance_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance
)
_generate_srv_py(Collision_Avoidance
  "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance
)

### Generating Module File
_generate_module_py(Collision_Avoidance
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(Collision_Avoidance_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(Collision_Avoidance_generate_messages Collision_Avoidance_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/CalcStopDuration.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_py _Collision_Avoidance_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/panda/franka_emika_ws/src/Collision_Avoidance/srv/FlagStop.srv" NAME_WE)
add_dependencies(Collision_Avoidance_generate_messages_py _Collision_Avoidance_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(Collision_Avoidance_genpy)
add_dependencies(Collision_Avoidance_genpy Collision_Avoidance_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS Collision_Avoidance_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Collision_Avoidance)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/Collision_Avoidance
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(Collision_Avoidance_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Collision_Avoidance)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/Collision_Avoidance
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(Collision_Avoidance_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Collision_Avoidance)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/Collision_Avoidance
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(Collision_Avoidance_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Collision_Avoidance)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/Collision_Avoidance
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(Collision_Avoidance_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/Collision_Avoidance
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(Collision_Avoidance_generate_messages_py std_msgs_generate_messages_py)
endif()
