;; Auto-generated. Do not edit!


(when (boundp 'def_proj::CalcStopDuration)
  (if (not (find-package "DEF_PROJ"))
    (make-package "DEF_PROJ"))
  (shadow 'CalcStopDuration (find-package "DEF_PROJ")))
(unless (find-package "DEF_PROJ::CALCSTOPDURATION")
  (make-package "DEF_PROJ::CALCSTOPDURATION"))
(unless (find-package "DEF_PROJ::CALCSTOPDURATIONREQUEST")
  (make-package "DEF_PROJ::CALCSTOPDURATIONREQUEST"))
(unless (find-package "DEF_PROJ::CALCSTOPDURATIONRESPONSE")
  (make-package "DEF_PROJ::CALCSTOPDURATIONRESPONSE"))

(in-package "ROS")





(defclass def_proj::CalcStopDurationRequest
  :super ros::object
  :slots (_q _q_p _q_pp ))

(defmethod def_proj::CalcStopDurationRequest
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

(defclass def_proj::CalcStopDurationResponse
  :super ros::object
  :slots (_stop_duration ))

(defmethod def_proj::CalcStopDurationResponse
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

(defclass def_proj::CalcStopDuration
  :super ros::object
  :slots ())

(setf (get def_proj::CalcStopDuration :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj::CalcStopDuration :datatype-) "def_proj/CalcStopDuration")
(setf (get def_proj::CalcStopDuration :request) def_proj::CalcStopDurationRequest)
(setf (get def_proj::CalcStopDuration :response) def_proj::CalcStopDurationResponse)

(defmethod def_proj::CalcStopDurationRequest
  (:response () (instance def_proj::CalcStopDurationResponse :init)))

(setf (get def_proj::CalcStopDurationRequest :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj::CalcStopDurationRequest :datatype-) "def_proj/CalcStopDurationRequest")
(setf (get def_proj::CalcStopDurationRequest :definition-)
      "float64[] q
float64[] q_p
float64[] q_pp
---
float64 stop_duration

")

(setf (get def_proj::CalcStopDurationResponse :md5sum-) "a8531c49262635abe6abcd3257d5d874")
(setf (get def_proj::CalcStopDurationResponse :datatype-) "def_proj/CalcStopDurationResponse")
(setf (get def_proj::CalcStopDurationResponse :definition-)
      "float64[] q
float64[] q_p
float64[] q_pp
---
float64 stop_duration

")



(provide :def_proj/CalcStopDuration "a8531c49262635abe6abcd3257d5d874")


