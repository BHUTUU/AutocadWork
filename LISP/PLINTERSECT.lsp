;Program: When PLINTERSECT command is called in AutoCAD/Civil 3D, it prompts user to select polylines, when selected, then, it converts them into region and run intersection command on that, which results to leave their intersecting part only as region.
;Author: Suman Kumar
;Github: github.com/BHUTUU
;Date: 10-Jan-2026
(defun c:PLINTERSECT ( / ss i ent regList baseReg)
  (prompt "\nSelect CLOSED polylines to intersect: ")
  (setq ss (ssget '((0 . "LWPOLYLINE") (70 . 1))))
  (if (or (null ss) (< (sslength ss) 2))
    (progn
      (prompt "\nAt least two closed polylines are required.")
      (princ)
    )
    (progn
      (setq regList '())
      (setq i 0)
      (repeat (sslength ss)
        (setq ent (ssname ss i))
        (command "_.REGION" ent "")
        (setq regList (cons (entlast) regList))
        (setq i (1+ i))
      )
      (setq baseReg (car regList))
      (setq regList (cdr regList))
      (foreach r regList
        (command "_.INTERSECT" baseReg r "")
        (setq baseReg (entlast))
      )
      (prompt "\nIntersection completed.")
    )
  )
  (princ)
)
