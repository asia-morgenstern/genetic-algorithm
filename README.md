# genetic-algorithm
Asia Morgenstern | 1 December 2023

Utilizes a genetic algorithm to implement 3 different optimization problems:

- Matching randomly generated strings to a target string
- Solving the trancendental equation cos(x) = x
- Finding a root of polynomial-like functions

These programs demonstrate various uses for a small-scale genetic algorithm.

Target String (match_target_string.py)
-

My implementation is based significantly on the code provided in https://www.geeksforgeeks.org/genetic-algorithms/.

In the first section, we define 3 different global constants:  the population size, the characters allowed, and the target string.  From there, the program will apply the genetic algorithm until it converges.  The system converges when the fitness score reaches 0;  the fitness score is calculated based on the number of different characters between the string in question and the target string.

Transcendental Equation (transcendental_eq.py)
-

My program takes advantage of the code I wrote for match_target_string.py and makes the necessary adaptations to address that the search space are the real numbers, not a string of characters.  As such, this program relies on converting floats to binary and vice versa.  Additionally, we define a maximum value (such that the value is less than or equal to 1) to bound our search space to the range [0, MAX_VAL).  Furthermore, since we want to solve cos(x) = x, we define our fitness score based on the quantity cos(x) - x.  Due to 

As with the above implementation, we can vary our value for the population size.  We can also vary the precision of the binary representation, i.e. adjusting the number of decimal places used in the binary representation.  Technically, we can also vary the maximum bound, but it must be less than 1 can greater than 0.739, the value for which cos(x) - x = 0, in order for the program to converge.

Root Finding (root_finder.py)
-

The code for the root finder algorithm is nearly identical to that of transcendental_eq.py.  The only change is we now also define a minimum bound on the search space (and account for such bounds when crossing two parents).  Just as with the previous implementations, we can vary our value for the population size and the precision of the binary representation.  We can also define the function for which we want to find the roots, as well the minimum and maximum bounds.  However, the defined function must have at least 1 real root.  Furthermore, these bounds, which are dependent on the function of choice, must bracket the root.
