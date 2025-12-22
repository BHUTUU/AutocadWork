;Program: AutoCAD lisp script to put MLeader at a give point.
;Author: Suman Kumar
;Github: github.com/BHUTUU
;Date: 19-Dec-2025
(defun c:IDML ( / pt x y txt)
  (setq pt (getpoint "\nSelect point to annotate: "))
  (if pt
    (progn
      (setq x (rtos (car pt) 2 3))
      (setq y (rtos (cadr pt) 2 3))
      (setq txt (strcat "E=" x "\nN=" y))
      (command
        "_MLEADER"
        pt
        pause
        txt
      )
    )
    (prompt "\nNo point selected.")
  )
  (princ)
)
