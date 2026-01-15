;Program: when PLBORDER command is called in AutoCAD/Civil 3D, it prompts user to select a polyline having some width>0, then it creates a boundary around that polyline with 0 thickness and in the same layer.
;Author: Suman Kumar
;Github: github.com/BHUTUU
;Date: 15-Jan-2026
(defun c:PLBORDER (/ ent ed w sw ew off o1 o2 p1 p2 l1 l2 ss)
  (vl-load-com)
  (setq ent (car (entsel "\nSelect polyline: ")))
  (if (null ent) (exit))
  (setq ed (entget ent))
  (if (/= (cdr (assoc 0 ed)) "LWPOLYLINE")
    (progn
      (princ "\nOnly LWPOLYLINE supported.")
      (exit)
    )
  )
  (setq w  (cdr (assoc 43 ed)))
  (setq sw (cdr (assoc 40 ed)))
  (setq ew (cdr (assoc 41 ed)))
  (cond
    ((and w (> w 0)) nil)
    ((and sw ew (= sw ew) (> sw 0)) (setq w sw))
    (T
     (princ "\nWidth not found or start/end widths not equal.")
     (exit)
    )
  )
  (setq off (/ w 2.0))
(setq o1 (vlax-vla-object->ename
           (car (vlax-safearray->list
                  (vlax-variant-value
                    (vla-offset (vlax-ename->vla-object ent) off))))))
(setq o2 (vlax-vla-object->ename
           (car (vlax-safearray->list
                  (vlax-variant-value
                    (vla-offset (vlax-ename->vla-object ent) (- off)))))))
  (setq p1 (vlax-curve-getStartPoint o1))
  (setq p2 (vlax-curve-getEndPoint   o1))
  (setq l1
        (entmakex (list '(0 . "LINE")
                        (cons 10 p1)
                        (cons 11 (vlax-curve-getStartPoint o2)))))

  (setq l2
        (entmakex (list '(0 . "LINE")
                        (cons 10 p2)
                        (cons 11 (vlax-curve-getEndPoint o2)))))
  (setq ss (ssadd))
  (ssadd o1 ss)
  (ssadd o2 ss)
  (ssadd l1 ss)
  (ssadd l2 ss)
  (command
    "_.PEDIT" "_M" ss "" "Y"
    "_J" "0"
    "_W" "0"
    ""
  )
  (princ "\nClosed boundary created successfully (width = 0).")
  (princ)
)
