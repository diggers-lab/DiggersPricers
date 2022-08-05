# DiggersPricers


This library aims at developing a generic tool to price any financial products. In its first version, it will be able
to price with a monte-carlo and a binomial pricer on products such as:
1. Call European/American option
2. Put European/American option
3. Barrier option
4. Asian(Arithmetic & Geometric Average) option
5. Basket option
   
The code structure should be as generic as possible so that it will be up
to the user to choose:
- Trajectory generator model
- Pricer 
- Product Type or metric

Any pull request will be studied and are welcome.
Please respect naming convention otherwise request 
won't be accepted right away.
