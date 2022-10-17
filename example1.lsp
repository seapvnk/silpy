(let x 10)
(let y 10)

(fun movementOf (x y)
  (if (= x y)
    (~ (+ x y) (+ 30 y))
    (~ (+ x 10) (+ 15 y))
  )
)

(print 
  (movementOf x y))
