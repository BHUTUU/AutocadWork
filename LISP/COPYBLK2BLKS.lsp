(defun c:COPYBLK2BLKS ( / srcEnt srcData srcName ss i tgtEnt tgtData tgtInsPt tgtRot )
  (command "-.undo" "MARK")
  (setq srcEnt (car (entsel "\nSelect SOURCE block: ")))
  (if (not srcEnt)
    (progn
      (princ "\nNothing selected.")
      (princ)
      (return)
    )
  )

  (setq srcData (entget srcEnt))
  (if (/= (cdr (assoc 0 srcData)) "INSERT")
    (progn
      (princ "\nSelected object is not a block.")
      (princ)
      (return)
    )
  )
  (setq srcName (cdr (assoc 2 srcData)))

  (setq ss (ssget '((0 . "INSERT"))))
  (if (not ss)
    (progn
      (princ "\nNo target blocks selected.")
      (princ)
      (return)
    )
  )
  ; (setq driftAngle (* (/ pi 180.0) (getreal "\nEnter additional rotation (degrees): ")))
  (setq driftAngle (getreal "\nEnter additional rotation (degrees): "))
  ; (if (not driftAngle) (setq driftAngle 0.0))
  (setq i 0)
  (while (< i (sslength ss))
    (setq tgtEnt  (ssname ss i))
    (setq tgtData (entget tgtEnt))
    (setq tgtInsPt (cdr (assoc 10 tgtData)))
    (setq tgtRot (if (assoc 50 tgtData) (cdr (assoc 50 tgtData)) 0.0))


    (command
      "-INSERT"
      srcName
      tgtInsPt
      1.0
      1.0
      tgtRot
    )

    (setq i (1+ i))
  )

  (princ "\nDone: block copied with matching rotations.")
  (princ)
)
