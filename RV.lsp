;Author: Suman Kumar ~BHUTUU sumankumar91356865@gmail.com, raj259942@gmail.com
;Date: 04-05-2025
;Program: To rotate the viewport with the help of two reference point such that the line(may not exist) joing the give two point, becomes horizontal or parallel to the x axis of view.
;Command to run this: RV

(defun c:RV ( / *error* cmde pt1 pt2 ang deg )
  ;; Define error handler to restore settings on error or exit
  (defun *error* ( msg )
    (if cmde (setvar 'cmdecho cmde))
    (if msg (prompt msg))
    (princ)
  )
  ;; Save and suppress command echo
  (setq cmde (getvar 'cmdecho))
  (setvar 'cmdecho 0)

  ;; Ensure we're inside a viewport (i.e., model space inside a layout)
  (if (> (getvar 'cvport) 1)
    (progn
      (prompt "\nSelect two points to define the direction to be made horizontal:")
      (setq pt1 (getpoint "\nFirst point: "))
      (setq pt2 (getpoint pt1 "\nSecond point: "))
      (if (and pt1 pt2)
        (progn
          (setq ang (angle pt1 pt2))             ; angle in radians
          (setq deg (* -1.0 (rtd ang)))           ; convert to degrees and negate for clockwise
          (command "._dview" "" "_twist" deg "") ; apply twist to viewport
          (setvar 'snapang ang)                  ; align crosshairs
          (prompt (strcat "\nRotated view " (rtos (abs deg) 2 2) " degrees clockwise."))
        )
        (prompt "\nInvalid points selected.")
      )
    )
    (prompt "\nPlease activate a model viewport first.")
  )
  ;; Restore environment
  (*error* nil)
)
;; Helper: convert radians to degrees
(defun rtd (a) (* 180.0 (/ a pi)))
