1.a. ∃x. like(Alice,x) ∧ like(x,Bob)
1.b. ∀x. ¬ smile(x,Jan)
1.c. ∀x. ¬ coughed(x) ∧ ¬ sneezed(x)

2.a. λx. feed(x,Chester) ∧ compliment(x,Alice)
2.b. λx. ∀y. love(y,x)
2.c. λx. ∀y. love(y,x) ∧ detest(y,x)

3. λg. λx. ∀y.(dog(y) -> (∃e. act(e,g) ∧ actor(e,x) ∧ actee(e,y)))

4. λg. λz.λx.∃y.(present(y) ∧ (∃e. act(e,g) ∧ actor(e,x) ∧ actee(e,y,z)))

5. see wordList.txt (if file does not exist, run parser.py)

6. 
