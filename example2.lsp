(let expr1 
  (∨ (= 1 1) (≠ 1 2)))
(let expr2 
  (∧ (≠ 2 3) (≤ 4 4)))

(let expr3 
  (∧ expr1 expr2))

(print expr3)
(let expr4
  (if expr3
    (1 2 3 4 5)
    (5 4 3 2 1)))

(print expr4)
