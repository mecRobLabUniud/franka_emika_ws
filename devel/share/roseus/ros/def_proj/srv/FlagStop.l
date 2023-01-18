;; Auto-generated. Do not edit!


(when (boundp 'def_proj::FlagStop)
  (if (not (find-package "DEF_PROJ"))
    (make-package "DEF_PROJ"))
  (shadow 'FlagStop (find-package "DEF_PROJ")))
(unless (find-package "DEF_PROJ::FLAGSTOP")
  (make-package "DEF_PROJ::FLAGSTOP"))
(unless (find-package "DEF_PROJ::FLAGSTOPREQUEST")
  (make-package "DEF_PROJ::FLAGSTOPREQUEST"))
(unless (find-package "DEF_PROJ::FLAGSTOPRESPONSE")
  (make-package "DEF_PROJ::FLAGSTOPRESPONSE"))

(in-package "ROS")





(defclass def_proj::FlagStopRequest
  :super ros::object
  :slots (_T_stop _q _q_p _q_pp ))

(defmethod def_proj::FlagStopRequest
  (:init
   (&key
    ((:T_stop __T_stop) 0.0)
    ((:q __q) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_p __q_p) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:q_pp __q_pp) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _T_stop (float __T_stop))
   (setq _q __q)
   (setq _q_p __q_p)
   (setq _q_pp __q_pp)
   self)
  (:T_stop
   (&optional __T_stop)
   (if __T_stop (setq _T_stop __T_stop)) _T_stop)
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
    ;; float64 _T_stop
    8
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
     ;; float64 _T_stop
       (sys::poke _T_stop (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
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
   ;; float64 _T_stop
     (setq _T_stop (sys::peek buf ptr- :double)) (incf ptr- 8)
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

(defclass def_proj::FlagStopResponse
  :super ros::object
  :slots (_flag_stop ))

(defmethod def_proj::FlagStopResponse
  (:init
   (&key
    ((:flag_stop __flag_stop) nil)
    )
   (send-super :init)
   (setq _flag_stop __flag_stop)
   self)
  (:flag_stop
   (&optional __flag_stop)
   (if __flag_stop (setq _flag_stop __flag_stop)) _flag_stop)
  (:serialization-length
   ()
   (+
    ;; bool _flag_stop
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _flag_stop
       (if _flag_stop (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _flag_stop
     (setq _flag_stop (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass def_proj::FlagStop
  :super ros::object
  :slots ())

(setf (get def_proj::FlagStop :md5sum-) "7b0aefe35bb755536b8814d5dcb2c19d")
(setf (get def_proj::FlagStop :datatype-) "def_proj/FlagStop")
(setf (get def_proj::FlagStop :request) def_proj::FlagStopRequest)
(setf (get def_proj::FlagStop :response) def_proj::FlagStopResponse)

(defmethod def_proj::FlagStopRequest
  (:response () (instance def_proj::FlagStopResponse :init)))

(setf (get def_proj::FlagStopRequest :md5sum-) "7b0aefe35bb755536b8814d5dcb2c19d")
(setf (get def_proj::FlagStopRequest :datatype-) "def_proj/FlagStopRequest")
(setf (get def_proj::FlagStopRequest :definition-)
      "float64 T_stop
float64[] q
float64[] q_p
float64[] q_pp
---
bool flag_stop

")

(setf (get def_proj::FlagStopResponse :md5sum-) "7b0aefe35bb755536b8814d5dcb2c19d")
(setf (get def_proj::FlagStopResponse :datatype-) "def_proj/FlagStopResponse")
(setf (get def_proj::FlagStopResponse :definition-)
      "float64 T_stop
float64[] q
float64[] q_p
float64[] q_pp
---
bool flag_stop

")



(provide :def_proj/FlagStop "7b0aefe35bb755536b8814d5dcb2c19d")


