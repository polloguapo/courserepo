""" This script contains classes, functions, etc to implement a data bank
    of information for universities including students, instructors, classes,
    and other related information.
"""
from os.path import isdir, join
from collections import defaultdict
from prettytable import PrettyTable


class Repository:
    """ Implementation of a repository class.  This is a container
        to hold students, instructors, and classes in one place for
        any given educational institution.
    """
    def __init__(self, dir_path):
        """ Initialization code for repositories """
        if(not isdir(dir_path)):
            raise FileNotFoundError(f"ERROR: Repository.__init__: Error accessing {dir_path}")
        
        self.instructors = []
        self.students = []
        self.majors = []

        self.read_data_files(dir_path)

    def read_data_files(self, dir_path):
        #read instructors from file
        filename = join(dir_path, "instructors.txt")
        try:
            for cwid, name, department in \
                    self.file_reading_gen(filename, fields=3, sep="|", \
                                          header=True):
                instructor = Instructor(cwid, name, department)
                self.instructors.append(instructor)
        except ValueError:
            print("Error reading instructors.txt.  Exiting.")
            return
        
        #read students from file
        filename = join(dir_path, "students.txt")
        try:
            for cwid, name, major in \
                    self.file_reading_gen(filename, fields=3, sep=";", \
                                          header=True):
                student = Student(cwid, name, major)
                self.students.append(student)
        except ValueError:
            print("Error reading students.txt.  Exiting.")
            return

        #read student grades from file
        filename = join(dir_path, "grades.txt")
        for cwid, course_id, grade, instructor_id in \
                    self.file_reading_gen(filename, fields=4, sep="|", \
                                          header=True):
            #add grade to the appropriate student's class
            found = False
            for student in self.students:
                if student.cwid == cwid:
                    found = True
                    student.add_grade(course_id, grade)
            if not found:
                print(f"ERROR:  No student with CWID {cwid} in students.txt.  Skipped.")

            #add course to the instructor's list of courses taught
            found = False
            for instructor in self.instructors:
                if instructor.cwid == instructor_id:
                    found = True
                    instructor.add_course(course_id)
            if not found:
                print(f"ERROR: No instructor with CWID {instructor_id} in instructors.txt. Skipped.")

        #read majors from file
        filename = join(dir_path, "majors.txt")
        try:
            for major_name, flag, course in \
                                self.file_reading_gen(filename, fields=3, \
                                                      sep="\t", header=True):
                major = Major(major_name, flag, course)
                self.majors.append(major)
        except ValueError:
            print("Error reading majors file.  Exiting.")
            return
 
    def file_reading_gen(self, path, fields, sep=',', header=False):
        """ This generator yields each line of an input file one at a time
            as long as the file exists, and each line has the exact number
            of fields specified in 'fields'
        """
        try:
            input_file = open(path, 'r')
        except IOError:
            raise FileNotFoundError("ERROR: File {path} not found while executing \
                                     file_reading_gen.")
        line_number = 1

        with input_file:
            for line in input_file:
                if((header != True) or (line_number != 1)):
                    field_values = line.strip("\n").split(sep)
    
                    #correct number of fields?
                    if(len(field_values) != fields):
                        raise ValueError(f"ValueError: {path} has {len(field_values)} fields on line {line_number}, but should have {fields} fields.")
                    else:
                        yield field_values

                line_number += 1

    def add_instructor(self, cwid, name):
        """ Manually add an instructor to the repository """
        self.instructors.append(Instructor(cwid, name))

    def add_student(self, cwid, name):
        """ Manually add a student to the repository """
        self.students.append(Student(cwid, name))

    def pretty_print(self, collection):
        """ Use PrettyTable to print a table of files and statistics for them. """
        if(collection == "instructors"):
            table = PrettyTable(field_names=["CWID", "Name", "Dept", \
                                             "Course", "Students"])
            for instructor in self.instructors:
                for course_id in instructor.course_list:
                    table.add_row([instructor.cwid, instructor.name, \
                                   instructor.department, course_id, instructor.course_list[course_id]])
        elif (collection == "students"):
            table = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
            for student in self.students:
                courses = []
                for course_id in sorted(student.grade_list):
                    courses += [course_id]
                table.add_row([student.cwid, student.name, courses])
        else:
            raise ValueError("ERROR: Invalid table type for PrettyPrint")

        return table


class Student():
    """ Implementation of students class """
    def __init__(self, cwid, name, major=None):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.grade_list = dict()
        
    def add_grade(self, course_id, grade=None):
        """ Manually add a grade to the student """
        self.grade_list[course_id] = grade

class Instructor():
    """ Implementation of instructors class """
    def __init__(self, cwid, name, department=None):
        """ Initialization code for Instructor class """
        self.cwid = cwid
        self.name = name
        self.department = department
        self.course_list = defaultdict(int)
        
    def add_course(self, course_id, increment=1):
        """ Manually add a course to the instructor """
        self.course_list[course_id] += increment


class Major():
    """ Implementation of Majors class """
    def __init__(self, major, flag, course):
        self.major = major
        self.flag = flag
        self.course = course

def main():
    """ Run some testing code to display data from repositories """
    print("Stevens Institute of Technology")
    
    try:
        stevens = Repository("./Stevens")
    except FileNotFoundError:
        print("ERROR:  Unable to access Stevens repository")
    else:
        result_table = stevens.pretty_print("instructors")
        print(result_table)
        result_table = stevens.pretty_print("students")
        print(result_table)

if __name__ == "__main__":
    main()