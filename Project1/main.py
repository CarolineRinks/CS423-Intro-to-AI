'''
Author: Caroline Rinks
This file reads in a datafile of applicant records, determines if an applicant 
meets all four criterias for being accepted, and produces an output file named
results.csv which contains the result (ACCEPT or REJECT) for each applicant.
'''

import csv

def analyze_applicant1(App_Data) :
    """
    Given the GPA's of a single applicant, return True if they are qualified
    Qualification: An applicant is qualified if...
        - The average of all their grades is above 85
    
    @param App_Data: a list of GPA's (integers)
    @return True if the applicant qualifies
    """
    
    avg = 0
    for i in range(0, 6):
        avg += App_Data[i]
    avg = avg / 6

    return (avg > 85)

def analyze_applicant2(App_Data) :
    """
    Given the GPA's of a single applicant, return True if they are qualified
    Qualification: An applicant is qualified if...
        - None of their GPA's is below 65
    
    @param App_Data: a list of GPA's (integers)
    @return True if the applicant qualifies
    """
    
    for i in range(0, 6):
        if (App_Data[i] < 65):
            return False
    
    return True

def analyze_applicant3(App_Data) :
    """
    Given the GPA's of a single applicant, return True if they are qualified
    Qualification: An applicant is qualified if...
        - At least 4 of their GPA's are above 85
    
    @param App_Data: a list of GPA's (integers)
    @return True if the applicant qualifies
    """
    
    count = 0
    for i in range(0, 6):
        if (App_Data[i] > 85):
            count += 1

    return count >= 4

def analyze_applicant4(App_Data) :
    """
    Given the GPA's of a single applicant, return True if they are qualified
    Qualification: An applicant is qualified if...
        - Average of 5 CS courses is above 85
    
    @param App_Data: a list of GPA's (integers)
    @return True if the applicant qualifies
    """
    
    avg = 0
    for i in range(0, 5):
        avg += App_Data[i]
    avg = avg / 5

    return (avg > 85)

def main(file):    
    """
    Given a CSV file containing a list of grades for each applicant, produce an output
    file "results.csv" which indicates whether an applicant evaluates to ACCEPT or REJECT.
    An applicant evaluates to ACCEPT if...
        - All four criteria are met, i.e. all analyze_applicant() functions return True
    Else an applicant evaluates to REJECT
    
    @param file: The file of applicant data to read from
    @return 0 at end of process
    """
    
    App_Data = [0, 0, 0, 0, 0, 0]

    line_num = 0

    with open('results.csv', 'w') as results_file:
        csv_writer = csv.writer(results_file)
        results_file.write("Applicant Status:\n")

        with open(file, 'r') as data:
            csv_reader = csv.reader(data)
            for row in csv_reader:
                if line_num == 0:
                    line_num += 1
                else:
                    line_num += 1
                    App_Data[0] = int(row[0])
                    App_Data[1] = int(row[1])
                    App_Data[2] = int(row[2])
                    App_Data[3] = int(row[3])
                    App_Data[4] = int(row[4])
                    App_Data[5] = int(row[5])
                
                    if analyze_applicant1(App_Data):
                        if analyze_applicant2(App_Data):
                            if analyze_applicant3(App_Data):
                                if analyze_applicant4(App_Data):
                                    results_file.write("ACCEPT\n")
                                    continue
                                    
                    results_file.write("REJECT\n")

    return 0

if __name__ == '__main__':
    """Call the function main(file)"""
    main('applicants.csv')