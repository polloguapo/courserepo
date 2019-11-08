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
        #self.classes = []

        #read instructors from file
        fullpath = join(dir_path, "instructors.txt")
        fp = open(fullpath, "r")
        with fp:
            for line in fp:
                items = line.strip().split("\t")
                instructor = Instructor(items[0], items[1], items[2])
                self.instructors.append(instructor)
        
        #read students from file
        fullpath = join(dir_path, "students.txt")
        fp = open(fullpath, "r")
        with fp:
            for line in fp:
                items = line.strip().split("\t")
                student = Student(items[0], items[1], items[2])
                self.students.append(student)

        #read student grades from file
        fullpath = join(dir_path, "grades.txt")
        fp = open(fullpath, "r")
        with fp:
            for line in fp:
                items = line.strip().split("\t")
                for student in self.students:
                    if student.cwid == items[0]:
                        student.add_grade(items[1], items[2])
                for instructor in self.instructors:
                    if instructor.cwid == items[3]:
                        instructor.add_course(items[1], 1)

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
                for course_id in student.grade_list:
                    courses += [course_id]
                table.add_row([student.cwid, student.name, courses])
        else:
            raise ValueError("ERROR: Invalid table type for PrettyPrint")

        return table


class Person():
    """ Implementation of Person parent class, which can be subclassed. """
    def __init__(self, cwid, name):
        """ Initialization code for Person class """
        self.name = name
        self.cwid = cwid


class Student(Person):
    """ Implementation of students class, derived from class Person """
    def __init__(self, cwid, name, major=None):
        self.major = major
        self.grade_list = dict()
        super().__init__(cwid, name)

    def add_grade(self, course_id, grade=None):
        """ Manually add a grade to the student """
        self.grade_list[course_id] = grade

class Instructor(Person):
    """ Implementation of instructors class, derived from class Person """
    def __init__(self, cwid, name, department=None):
        """ Initialization code for Instructor class """
        self.department = department
        self.course_list = defaultdict(int)
        super().__init__(cwid, name)

    def add_course(self, course_id, increment=1):
        """ Manually add a course to the instructor """
        self.course_list[course_id] += increment

def main():
    """ Run some testing code to display data from repositories """
    print("Stevens Institute of Technology")
    stevens = Repository("./Stevens")
    result_table = stevens.pretty_print("instructors")
    print(result_table)
    result_table = stevens.pretty_print("students")
    print(result_table)
    
    print("NJIT")
    njit = Repository("./NJIT")
    result_table = njit.pretty_print("instructors")
    print(result_table)
    #result_table = njit.pretty_print("students")
    #print(result_table)
    
if __name__ == "__main__":
    main()