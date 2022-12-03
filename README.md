# DoE & Automated Engine Test
# Introduction
Salam (Peace). I wrote this repository for generation of test points in accordance with D-Optimality criterion for 4 variables and to automate engine tests which is a time consuming and exhaustive process. Automated engine test is available for ATI Vision (a program mainly used for ECU test) via generated or imported test points.

Basic steps for D-Optimality criterion is as follows. 2. Order Taylor Series is assumed for the model of the system (ICE). It's determined upon the effect of each factors change in relation to other factors. Based on this assumption information matrix is generated. Let X be the information matrix then determinant of transpose of X * X (to be precise det(transpose(X)*X)) should be maximized to obtain D-Optimality criterion.


# How it works?
In order to run the tool main.py should be executed. 
main.py is the initial script to run. 
page_manager.py is used for switching between pages and signals to be transferred from öne class to another.
doe_manager.py arranges all the things that's related to DoE.
table_manager.py simply responsible for generation of tables that's. This is used as an instance in doe_manager.py
doe_point_generator.py is solely for generating D-Optimal test points. This is used as an instance in table_manager.py
button_manager.py is responsible for bittin generation  and links buttons to respective functions.
print_manager.py is responsible for giving notifications to the user.
engine_test_manager.py is responsible for automated engine test. 
engine_test_automation.py is solely responsible for running the engine test with güven test points. This is used as an instance in engine_test_manager.py


# To do
More models should be available for D-Optimality criterion. Right now 2. Order Taylor Series is the only option.
Automated test for Inca should be available.
Right now the algorithm cannot guarantee global d-optimality, for this algorithms like "row exchange" should be implemented.




