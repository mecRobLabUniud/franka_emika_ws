; Auto-generated. Do not edit!


(cl:in-package def_proj_Panda-srv)


;//! \htmlinclude CalcValidTraj-request.msg.html

(cl:defclass <CalcValidTraj-request> (roslisp-msg-protocol:ros-message)
  ((q_s
    :reader q_s
    :initarg :q_s
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (q_e
    :reader q_e
    :initarg :q_e
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (traj_duration
    :reader traj_duration
    :initarg :traj_duration
    :type cl:float
    :initform 0.0)
   (traj_step
    :reader traj_step
    :initarg :traj_step
    :type cl:float
    :initform 0.0))
)

(cl:defclass CalcValidTraj-request (<CalcValidTraj-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CalcValidTraj-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CalcValidTraj-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name def_proj_Panda-srv:<CalcValidTraj-request> is deprecated: use def_proj_Panda-srv:CalcValidTraj-request instead.")))

(cl:ensure-generic-function 'q_s-val :lambda-list '(m))
(cl:defmethod q_s-val ((m <CalcValidTraj-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader def_proj_Panda-srv:q_s-val is deprecated.  Use def_proj_Panda-srv:q_s instead.")
  (q_s m))

(cl:ensure-generic-function 'q_e-val :lambda-list '(m))
(cl:defmethod q_e-val ((m <CalcValidTraj-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader def_proj_Panda-srv:q_e-val is deprecated.  Use def_proj_Panda-srv:q_e instead.")
  (q_e m))

(cl:ensure-generic-function 'traj_duration-val :lambda-list '(m))
(cl:defmethod traj_duration-val ((m <CalcValidTraj-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader def_proj_Panda-srv:traj_duration-val is deprecated.  Use def_proj_Panda-srv:traj_duration instead.")
  (traj_duration m))

(cl:ensure-generic-function 'traj_step-val :lambda-list '(m))
(cl:defmethod traj_step-val ((m <CalcValidTraj-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader def_proj_Panda-srv:traj_step-val is deprecated.  Use def_proj_Panda-srv:traj_step instead.")
  (traj_step m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CalcValidTraj-request>) ostream)
  "Serializes a message object of type '<CalcValidTraj-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'q_s))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'q_s))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'q_e))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'q_e))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'traj_duration))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'traj_step))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CalcValidTraj-request>) istream)
  "Deserializes a message object of type '<CalcValidTraj-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'q_s) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'q_s)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'q_e) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'q_e)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'traj_duration) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'traj_step) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CalcValidTraj-request>)))
  "Returns string type for a service object of type '<CalcValidTraj-request>"
  "def_proj_Panda/CalcValidTrajRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CalcValidTraj-request)))
  "Returns string type for a service object of type 'CalcValidTraj-request"
  "def_proj_Panda/CalcValidTrajRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CalcValidTraj-request>)))
  "Returns md5sum for a message object of type '<CalcValidTraj-request>"
  "70855c1f975352ceba80c99de40d0931")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CalcValidTraj-request)))
  "Returns md5sum for a message object of type 'CalcValidTraj-request"
  "70855c1f975352ceba80c99de40d0931")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CalcValidTraj-request>)))
  "Returns full string definition for message of type '<CalcValidTraj-request>"
  (cl:format cl:nil "float64[] q_s~%float64[] q_e~%float64 traj_duration~%float64 traj_step~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CalcValidTraj-request)))
  "Returns full string definition for message of type 'CalcValidTraj-request"
  (cl:format cl:nil "float64[] q_s~%float64[] q_e~%float64 traj_duration~%float64 traj_step~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CalcValidTraj-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'q_s) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'q_e) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CalcValidTraj-request>))
  "Converts a ROS message object to a list"
  (cl:list 'CalcValidTraj-request
    (cl:cons ':q_s (q_s msg))
    (cl:cons ':q_e (q_e msg))
    (cl:cons ':traj_duration (traj_duration msg))
    (cl:cons ':traj_step (traj_step msg))
))
;//! \htmlinclude CalcValidTraj-response.msg.html

(cl:defclass <CalcValidTraj-response> (roslisp-msg-protocol:ros-message)
  ((flag_valid
    :reader flag_valid
    :initarg :flag_valid
    :type cl:fixnum
    :initform 0))
)

(cl:defclass CalcValidTraj-response (<CalcValidTraj-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CalcValidTraj-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CalcValidTraj-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name def_proj_Panda-srv:<CalcValidTraj-response> is deprecated: use def_proj_Panda-srv:CalcValidTraj-response instead.")))

(cl:ensure-generic-function 'flag_valid-val :lambda-list '(m))
(cl:defmethod flag_valid-val ((m <CalcValidTraj-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader def_proj_Panda-srv:flag_valid-val is deprecated.  Use def_proj_Panda-srv:flag_valid instead.")
  (flag_valid m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CalcValidTraj-response>) ostream)
  "Serializes a message object of type '<CalcValidTraj-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'flag_valid)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CalcValidTraj-response>) istream)
  "Deserializes a message object of type '<CalcValidTraj-response>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'flag_valid)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CalcValidTraj-response>)))
  "Returns string type for a service object of type '<CalcValidTraj-response>"
  "def_proj_Panda/CalcValidTrajResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CalcValidTraj-response)))
  "Returns string type for a service object of type 'CalcValidTraj-response"
  "def_proj_Panda/CalcValidTrajResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CalcValidTraj-response>)))
  "Returns md5sum for a message object of type '<CalcValidTraj-response>"
  "70855c1f975352ceba80c99de40d0931")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CalcValidTraj-response)))
  "Returns md5sum for a message object of type 'CalcValidTraj-response"
  "70855c1f975352ceba80c99de40d0931")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CalcValidTraj-response>)))
  "Returns full string definition for message of type '<CalcValidTraj-response>"
  (cl:format cl:nil "uint8 flag_valid~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CalcValidTraj-response)))
  "Returns full string definition for message of type 'CalcValidTraj-response"
  (cl:format cl:nil "uint8 flag_valid~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CalcValidTraj-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CalcValidTraj-response>))
  "Converts a ROS message object to a list"
  (cl:list 'CalcValidTraj-response
    (cl:cons ':flag_valid (flag_valid msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'CalcValidTraj)))
  'CalcValidTraj-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'CalcValidTraj)))
  'CalcValidTraj-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CalcValidTraj)))
  "Returns string type for a service object of type '<CalcValidTraj>"
  "def_proj_Panda/CalcValidTraj")