;;; ------------------------------------------------------------
;;; Bind all Xrefs (attached, overlayed, nested) in one go
;;; ------------------------------------------------------------
(defun c:BindAllXrefs ( / doc coll xrefList)
  (vl-load-com) ;; Load Visual LISP extensions

  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))
  (setq coll (vla-get-Blocks doc))

  (defun GetXrefs ( / lst)
    (setq lst '())
    (vlax-for blk coll
      (if (= :vlax-true (vla-get-IsXRef blk))
        (setq lst (cons (vla-get-Name blk) lst))
      )
    )
    lst
  )

  ;; First collection of Xrefs
  (setq xrefList (GetXrefs))

  (if xrefList
    (progn
      (princ (strcat "\nFound " (itoa (length xrefList)) " Xref(s). Binding..."))
      ;; Loop until no more Xrefs remain
      (while xrefList
        ;; Pass all names directly to the command
        (apply 'command (append (list "_.-XREF" "_BIND") xrefList (list "")))
        ;; Rebuild list for nested Xrefs
        (setq xrefList (GetXrefs))
      )
      (princ "\nAll Xrefs have been bound successfully.")
    )
    (princ "\nNo Xrefs found in this drawing.")
  )

  (princ)
)
