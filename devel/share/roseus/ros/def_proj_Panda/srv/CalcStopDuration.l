;; Auto-generated. Do not edit!


(when (boundp 'def_proj_Panda::CalcStopDuration)
  (if (not (find-package "DEF_PROJ_PANDA"))
    (make-package "DEF_PROJ_PANDA"))
  (shadow 'CalcStopDuration (find-package "DEF_PROJ_PANDA")))
(unless (find-package "DEF_PROJ_PANDA::CALCSTOPDURATION")
  (make-package "DEF_PROJ_PANDA::CALCSTOPDURATION"))
(unless (find-package "DEF_PROJ_PANDA::CALCSTOPDURATIONREQUEST")
  (make-package "DEF_PROJ_PANDA::CALCSTOPDURATIONREQUEST"))
(unless (find-package "DEF_PROJ_PANDA::CALCSTOPDURATIONRESPONSE")
  (make-package "DEF_PROJ_PANDA::CALCSTOPDURATIONRESPONSE"))

(in-package "ROS")





(defclass def_proj_Panda::CalcStopDurationRequest
  :super ros::object
  :slots (_q _q_p _q_pp ))

(defmethod def_proj_Panda::CalcStopDurationRequest
  (:init
   (&key
    ((:q __q) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_p __q_p) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_pp __q_pp) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _q __q)
   (setq _q_p __q_p)
   (setq _q_pp __q_pp)
   self)
  (:q
   (&optional __q)
   (if __q (setq _q __q)) _q)
  (:q_p
   (&optional __q_p)
   (if __q_p (setq _q_p __q_p)) _q_p)
  (:q_pp
   (&optional __q_pp)
   (if __q_pp (setq _q_pp __q_pp)) _q_pp)
  (:serialization-length
   ()
   (+
    ;; float64[] _q
    (* 8    (length _q)) 4
    ;; float64[] _q_p
    (* 8    (length _q_p)) 4
    ;; float64[] _q_pp
    (* 8    (length _q_pp)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _q
     (write-long (length _q) s)
     (dotimes (i (length _q))
       (sys::poke (elt _q i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _q_p
     (write-long (length _q_p) s)
     (dotimes (i (length _q_p))
       (sys::poke (elt _q_p i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _q_pp
     (write-long (length _q_pp) s)
     (dotimes (i (length _q_pp))
       (sys::poke (elt _q_pp i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _q
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _q_p
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_p (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_p i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _q_pp
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _q_pp (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _q_pp i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(defclass def_proj_Panda::CalcStopDurationResponse
  :super ros::object
  :slots (_stop_duration ))

(defmethod def_proj_Panda::CalcStopDurationResponse
  (:init
   (&key
    ((:stop_duration __stop_duration) 0.0)
    )
   (send-super :init)
   (setq _stop_duration (float __stop_duration))
   self)
  (:stop_duration
   (&optional __stop_duration)
   (if __stop_duration (setq _stop_duration __stop_duration)) _stop_duration)
  (:serialization-length
   ()
   (+
    ;; float64 _stop_duration
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _stop_duration
       (sys::poke _stop_duration (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _stop_duration
     (setq _stop_duration (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass def_proj_Panda::CalcStopDuration
  :super ros::object
  :slots ())

(setf (get def_proj_Panda::CalcStopDuration :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj_Panda::CalcStopDuration :datatype-) "def_proj_Panda/CalcStopDuration")
(setf (get def_proj_Panda::CalcStopDuration :request) def_proj_Panda::CalcStopDurationRequest)
(setf (get def_proj_Panda::CalcStopDuration :response) def_proj_Panda::CalcStopDurationResponse)

(defmethod def_proj_Panda::CalcStopDurationRequest
  (:response () (instance def_proj_Panda::CalcStopDurationResponse :init)))

(setf (get def_proj_Panda::CalcStopDurationRequest :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj_Panda::CalcStopDurationRequest :datatype-) "def_proj_Panda/CalcStopDurationRequest")
(setf (get def_proj_Panda::CalcStopDurationRequest :definition-)
      "float64[] q
float64[] q_p
float64[] q_pp
---
float64 stop_duration

")

(setf (get def_proj_Panda::CalcStopDurationResponse :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj_Panda::CalcStopDurationResponse :datatype-) "def_proj_Panda/CalcStopDurationResponse")
(setf (get def_proj_Panda::CalcStopDurationResponse :definition-)
      "float64[] q
float64[] q_p
float64[] q_pp
---
float64 stop_duration

")



(provide :def_proj_Panda/CalcStopDuration "a8531c49262635abe6abcd3257d5d874")


