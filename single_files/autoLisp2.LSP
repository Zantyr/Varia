(defun avg(lista/num i x y z);to be debugged never
	 (setq num (length lista) x 0.0 y 0.0 z 0.0)
	(foreach i lista (setq x (+ x (nth 0 i)) y (+ y (nth 1 i)) z (+ z (nth 2 i)) ) )
  	(setq x (/ x num) y (/ y num) z (/ z num))
  	(command "_circle" '(x y z) 10)
	)

(defun XD(/ p l i)
	(setq i 3)
	(setq p (getpoint "Gimme da point: "))
	(while (not (null p))
		(command "_circle" p i)
		(setq i (+ i 3))
		(setq l (append l (list p)))
		(setq p (getpoint "Giveth-thou ye nexte pointe: "))
		)
  	;(print l)
  	;(avg l)
	(eval 'l)
	)

(defun prostokat(/ pts p x y xmin ymin c1 xmax ymax c2 nx ny)
  (setq p (getpoint "Gimme da point: "))
  (while (not (null p))
    (command "_circle" p 3)
    (setq pts (append pts (list p)))
    (setq p (getpoint "Giveth-thou ye nexte pointe: "))
  )
  (foreach p pts
    (setq x (nth 0 p) y (nth 1 p))
    (setq nx (append nx (list x)) ny (append ny (list y)))
    )
  (setq xmin (apply 'min nx) ymin (apply 'min ny) xmax (apply 'max nx) ymax (apply 'max ny))
  (setq c1 (list xmin ymin) c2 (list xmax ymax))
  (command "_color" 4)
  (command "_line")
  (foreach p pts (command p))
  (command nil)
  (command "_color" 1)
  (command "_rectangle" c1 c2)
  (command "_color" "_bylayer")
  )
