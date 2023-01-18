
(cl:in-package :asdf)

(defsystem "def_proj-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "CalcStopDuration" :depends-on ("_package_CalcStopDuration"))
    (:file "_package_CalcStopDuration" :depends-on ("_package"))
    (:file "CalcValidTraj" :depends-on ("_package_CalcValidTraj"))
    (:file "_package_CalcValidTraj" :depends-on ("_package"))
    (:file "FlagStop" :depends-on ("_package_FlagStop"))
    (:file "_package_FlagStop" :depends-on ("_package"))
  ))