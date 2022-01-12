Author: Caroline Rinks
Name: Project 1 (Applicant Qualification Test)

------------
Instructions
------------
    To run this program, navigate to the directory where main.py is stored and type 
    the following command into a terminal:
        python3 main.py

-----------
Description
-----------
    This program contains 4 functions that test an applicant on 4 different criteria:
        - An overall grade average above 85
        - No grade below 65
        - At least 4 grades above 85
        - An average above 85 in the 5 CS courses
    If an applicant meets all 4 criteria, the program will output "ACCEPT".
    If an applicant does not meet all 4 criteria, the program will output "REJECT".
    
    The program processes a CSV file (applicants.csv) containing the grades of each
    applicant. Each applicant is then tested for the above criteria, the result of which is 
    written to a file named "results.csv".

-----------------
Ethical Statement
-----------------
    This software should not be permissible for real-world use because the only information
    of a candidate that it evaluates is grades, which are not always an accurate representation
    of knowledge and cannot be used exclusively to predict success for a particular job. There is
    also a problem with arbitrary numbers chosen for certain criteria. For example, one of the
    criteria requires that at least 4 of the applicant's grades be above 85, but is a grade of
    85 really more deserving than a grade of 84?