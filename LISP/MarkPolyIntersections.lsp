;Program: When the command MarkPolyIntersections is called in autocad/civil 3d, it promptes user to select all the polylines, after that it makrs the intesection of the polylines by circles.
;Author: Suman Kumar
;Github: github.com/BHUTUU
;Date: 08-Jan-2026
(defun c:MarkPolyIntersections ( / ss i j obj1 obj2 res pts pt)
  (vl-load-com)
  (setq ss (ssget "X" '((0 . "LWPOLYLINE") (70 . 1))))
  (if ss
    (progn
      (setq i 0)

      (while (< i (sslength ss))
        (setq j (1+ i))

        (while (< j (sslength ss))
          (setq obj1 (vlax-ename->vla-object (ssname ss i)))
          (setq obj2 (vlax-ename->vla-object (ssname ss j)))
          (setq res (vlax-invoke obj1 'IntersectWith obj2 acExtendNone))
          (cond
            ((= (type res) 'VARIANT)
             (setq pts (vlax-safearray->list (vlax-variant-value res)))
            )
            ((listp res)
             (setq pts res)
            )
            (t (setq pts nil))
          )
          (while pts
            (setq pt (list (car pts) (cadr pts) (caddr pts)))

            (entmakex
              (list
                '(0 . "CIRCLE")
                (cons 10 pt)
                '(40 . 1.0)
                '(62 . 1)
              )
            )
            (setq pts (cdddr pts))
          )
          (setq j (1+ j))
        )
        (setq i (1+ i))
      )
      (princ "\nIntersection points marked.")
    )
    (princ "\nNo closed polylines found.")
  )
  (princ)
)
