;; Auto-generated. Do not edit!


(when (boundp 'def_proj_Panda::CalcValidTraj)
  (if (not (find-package "DEF_PROJ_PANDA"))
    (make-package "DEF_PROJ_PANDA"))
  (shadow 'CalcValidTraj (find-package "DEF_PROJ_PANDA")))
(unless (find-package "DEF_PROJ_PANDA::CALCVALIDTRAJ")
  (make-package "DEF_PROJ_PANDA::CALCVALIDTRAJ"))
(unless (find-package "DEF_PROJ_PANDA::CALCVALIDTRAJREQUEST")
  (make-package "DEF_PROJ_PANDA::CALCVALIDTRAJREQUEST"))
(unless (find-package "DEF_PROJ_PANDA::CALCVALIDTRAJRESPONSE")
  (make-package "DEF_PROJ_PANDA::CALCVALIDTRAJRESPONSE"))

(in-package "ROS")





(defclass def_proj_Panda::CalcValidTrajRequest
  :super ros::object
  :slots (_q_s _q_e _traj_duration _traj_step ))

(defmethod def_proj_Panda::CalcValidTrajRequest
  (:init
   (&key
    ((:q_s __q_s) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_e __q_e) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:traj_duration __traj_duration) 0.0)
    ((:traj_step __traj_step) 0.0)
    )
   (send-super :init)
   (setq _q_s __q_s)
   (setq _q_e __q_e)
   (setq _traj_duration (float __traj_duration))
   (setq _traj_step (float __traj_step))
   self)
  (:q_s
   (&optional __q_s)
   (if __q_s (setq _q_s __q_s)) _q_s)
  (:q_e
   (&optional __q_e)
   (if __q_e (setq _q_e __q_e)) _q_e)
  (:traj_duration
   (&optional __traj_duration)
   (if __traj_duration (setq _traj_duration __traj_duration)) _traj_duration)
  (:traj_step
   (&optional __traj_step)
   (if __traj_step (setq _traj_step __traj_step)) _traj_step)
  (:serialization-length
   ()
   (+
    ;; float64[] _q_s
    (* 8    (length _q_s)) 4
    ;; float64[] _q_e
    (* 8    (length _q_e)) 4
    ;; float64 _traj_duration
    8
    ;; float64 _traj_step
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _q_s
     (write-long (length _q_s) s)
     (dotimes (i (length _q_s))
       (sys::poke (elt _q_s i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _q_e
     (write-long (length _q_e) s)
     (dotimes (i (length _q_e))
       (sys::poke (elt _q_e i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64 _traj_duration
       (sys::poke _traj_duration (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _traj_step
       (sys::poke _traj_step (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _q_s
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_s (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_s i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _q_e
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_e (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_e i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64 _traj_duration
     (setq _traj_duration (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _traj_step
     (setq _traj_step (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass def_proj_Panda::CalcValidTrajResponse
  :super ros::object
  :slots (_flag_valid ))

(defmethod def_proj_Panda::CalcValidTrajResponse
  (:init
   (&key
    ((:flag_valid __flag_valid) 0)
    )
   (send-super :init)
   (setq _flag_valid (round __flag_valid))
   self)
  (:flag_valid
   (&optional __flag_valid)
   (if __flag_valid (setq _flag_valid __flag_valid)) _flag_valid)
  (:serialization-length
   ()
   (+
    ;; uint8 _flag_valid
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _flag_valid
       (write-byte _flag_valid s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _flag_valid
     (setq _flag_valid (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(defclass def_proj_Panda::CalcValidTraj
  :super ros::object
  :slots ())

(setf (get def_proj_Panda::CalcValidTraj :md5sum-) "70855c1f975352ceba80c99de40d0931")
(setf (get def_proj_Panda::CalcValidTraj :datatype-) "def_proj_Panda/CalcValidTraj")
(setf (get def_proj_Panda::CalcValidTraj :request) def_proj_Panda::CalcValidTrajRequest)
(setf (get def_proj_Panda::CalcValidTraj :response) def_proj_Panda::CalcValidTrajResponse)

(defmethod def_proj_Panda::CalcValidTrajRequest
  (:response () (instance def_proj_Panda::CalcValidTrajResponse :init)))

(setf (get def_proj_Panda::CalcValidTrajRequest :md5sum-) "70855c1f975352ceba80c99de40d0931")
(setf (get def_proj_Panda::CalcValidTrajRequest :datatype-) "def_proj_Panda/CalcValidTrajRequest")
(setf (get def_proj_Panda::CalcValidTrajRequest :definition-)
      "float64[] q_s
float64[] q_e
float64 traj_duration
float64 traj_step
---
uint8 flag_valid

")

(setf (get def_proj_Panda::CalcValidTrajResponse :md5sum-) "70855c1f975352ceba80c99de40d0931")
(setf (get def_proj_Panda::CalcValidTrajResponse :datatype-) "def_proj_Panda/CalcValidTrajResponse")
(setf (get def_proj_Panda::CalcValidTrajResponse :definition-)
      "float64[] q_s
float64[] q_e
float64 traj_duration
float64 traj_step
---
uint8 flag_valid

")



(provide :def_proj_Panda/CalcValidTraj "70855c1f975352ceba80c99de40d0931")


