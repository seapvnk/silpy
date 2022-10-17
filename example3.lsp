(let x 19)

; x -> 19
(:x (+ x 1))


; x -> 20
(if (= x 20)
  (:x (+ x 20)))

; x -> 40
(print x) ; print 40
