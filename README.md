# DoE & Automated Engine Test
# Introduction
Salam (Peace). I wrote this repository for generation of test points in accordance with D-Optimality criterion for 4 variables and to automate engine tests which is a time consuming and exhaustive process. Automated engine test is available for ATI Vision (a program mainly used for ECU test) via generated or imported test points.

Basic steps for D-Optimality criterion is as follows. 2. Order Taylor Series is assumed for the model of the system (ICE). It's determined upon the effect of each factors change in relation to other factors. Based on this assumption information matrix is generated. Let X be the information matrix then determinant of transpose of X * X (to be precise det(transpose(X)*X)) should be maximized to obtain D-Optimality criterion.


# How it works?
In order to run the tool main.py should be executed. 

# To do
More models should be available for D-Optimality criterion. Right now 2. Order Taylor Series is the only option.
Automated test for Inca should be available.
Right now the algorithm cannot guarantee global d-optimality, for this algorithms like "row exchange" should be implemented.
