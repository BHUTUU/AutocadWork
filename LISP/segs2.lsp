;Program: Makes segments twice the length of arc, circle, ellipse line polyline, spline. Actually, creates new polyline with 2*length segments and erase the existing one.
;Author: Suman Kumar
;Github: github.com/BHUTUU
;Date: 15-Jan-2026

(defun c:segs2 ( / *error* dis ent idx inc len lst num pnt sel )
    (defun *error* ( msg )
        (LM:endundo (LM:acdoc))
        (if (not (wcmatch (strcase msg t) "*break,*cancel*,*exit*"))
            (princ (strcat "\nError: " msg))
        )
        (princ)
    )
    (if
        (setq sel
            (ssget "_:L"
               '(
                    (0 . "ARC,CIRCLE,ELLIPSE,LINE,*POLYLINE,SPLINE")
                    (-4 . "<NOT")
                        (-4 . "<AND")
                            (0 . "POLYLINE") (-4 . "&") (70 . 88)
                        (-4 . "AND>")
                    (-4 . "NOT>")
                )
            )
        )
        (progn
            (LM:startundo (LM:acdoc))
            (repeat (setq idx (sslength sel))
                (setq ent (ssname sel (setq idx (1- idx))))
                (setq len
                    (vlax-curve-getdistatparam
                        ent
                        (vlax-curve-getendparam ent)
                    )
                )
                (setq num (max 1 (fix (* len 2.0))))
                (setq inc (/ len (float num))
                      dis 0.0
                      lst nil
                )
                (repeat (1+ num)
                    (if (setq pnt (vlax-curve-getpointatdist ent dis))
                        (setq lst (cons (cons 10 (trans pnt 0 ent)) lst))
                    )
                    (setq dis (+ dis inc))
                )
                (if
                    (not
                        (equal
                            (vlax-curve-getendpoint ent)
                            (trans (cdar lst) ent 0)
                            1e-6
                        )
                    )
                    (setq lst
                        (cons
                            (cons 10
                                (trans (vlax-curve-getendpoint ent) 0 ent)
                            )
                            lst
                        )
                    )
                )
                (if
                    (entmake
                        (append
                            (list
                               '(000 . "LWPOLYLINE")
                               '(100 . "AcDbEntity")
                               '(100 . "AcDbPolyline")
                                (cons 90 (length lst))
                                (cons 38 (last (car lst)))
                                (cons 70 (if (vlax-curve-isclosed ent) 1 0))
                            )
                            (LM:defaultprops (entget ent))
                            (reverse lst)
                            (list (assoc 210 (entget ent)))
                        )
                    )
                    (entdel ent)
                )
            )

            (LM:endundo (LM:acdoc))
        )
    )
    (princ)
)
(defun LM:defaultprops ( enx )
    (mapcar
        '(lambda ( x ) (cond ((assoc (car x) enx)) ( x )))
       '(
            (006 . "BYLAYER")
            (008 . "0")
            (039 . 0.0)
            (048 . 1.0)
            (062 . 256)
            (370 . -1)
        )
    )
)
(defun LM:startundo ( doc )
    (LM:endundo doc)
    (vla-startundomark doc)
)
(defun LM:endundo ( doc )
    (while (= 8 (logand 8 (getvar 'undoctl)))
        (vla-endundomark doc)
    )
)
(defun LM:acdoc nil
    (eval
        (list
            'defun 'LM:acdoc 'nil
            (vla-get-activedocument (vlax-get-acad-object))
        )
    )
    (LM:acdoc)
)
(vl-load-com)
(princ
    (strcat
        "\n:: SegmentCurve.lsp | Modified | \u00A9 Lee Mac "
        (menucmd "m=$(edtime,0,yyyy)")
        " www.lee-mac.com ::"
        "\n:: Type \"SEGS\" to Invoke ::"
    )
)
(princ)