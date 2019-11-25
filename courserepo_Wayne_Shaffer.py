""" This script contains classes, functions, etc to implement a data bank
    of information for universities including students, instructors, classes,
    and other related information.
"""
from os.path import isdir, join
from collections import defaultdict
from prettytable import PrettyTable
import sqlite3


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
        self.majors = defaultdict(dict)

        self.read_majors(dir_path)
        self.read_instructors(dir_path)
        self.read_students(dir_path)
        self.read_grades(dir_path)

    def read_instructors(self, dir_path):
        #read instructors from file
        filename = join(dir_path, "instructors.txt")
        try:
            for cwid, name, department in \
                    self.file_reading_gen(filename, fields=3, sep="\t", \
                                          header=True):
                instructor = Instructor(cwid, name, department)
                self.instructors.append(instructor)
        except ValueError:
            print("Error reading instructors.txt.  Exiting.")
            return
        
    def read_students(self, dir_path):
        #read students from file
        filename = join(dir_path, "students.txt")
        try:
            for cwid, name, major in \
                    self.file_reading_gen(filename, fields=3, sep="\t", \
                                          header=True):
                student = Student(cwid, name, major)
                
                #initialize student's course list with the
                #required and elective courses, no grade.
                for course in self.majors[major]:
                    student.add_grade(course)

                self.students.append(student)
        except ValueError:
            print("Error reading students.txt.  Exiting.")
            return

    def read_grades(self, dir_path):
        #read student grades from file
        filename = join(dir_path, "grades.txt")
        for cwid, course_id, grade, instructor_id in \
                    self.file_reading_gen(filename, fields=4, sep="\t", \
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

    def read_majors(self, dir_path):
        #read majors from file
        filename = join(dir_path, "majors.txt")
        try:
            for major, flag, course in \
                                self.file_reading_gen(filename, fields=3, \
                                                      sep="\t", header=True):
                self.majors[major][course] = flag
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

    def instructor_table_db(self, db_path):
        """ Read Instructor data from SQLite database provided by db_path """
        DB_FILE = join(db_path, "810_startup.db")
        db = sqlite3.connect(DB_FILE)

        table = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])

        for row in db.execute("select i.cwid, i.name, i.dept, g.course, count(*) \
                               as NumStudents from instructors i join grades g \
                               on i.cwid=g.instructorcwid group by course"):
            table.add_row(list(row))

        return table
    
    def add_instructor(self, cwid, name):
        """ Manually add an instructor to the repository """
        self.instructors.append(Instructor(cwid, name))

    def add_student(self, cwid, name):
        """ Manually add a student to the repository """
        self.students.append(Student(cwid, name))

    def pretty_print(self, collection):
        """ Use PrettyTable to print a table of files and statistics for them. """
        if(collection == "majors"):
            table = PrettyTable(field_names=["Dept", "Required", "Electives"])
            for major in self.majors:
                required_courses = [course for course in self.majors[major].keys()
                                if self.majors[major][course] == "R"]
                elective_courses = [course for course in self.majors[major].keys()
                                if self.majors[major][course] == "E"]
                table.add_row([major, required_courses, elective_courses])
        
        elif(collection == "instructors"):
            table = PrettyTable(field_names=["CWID", "Name", "Dept", \
                                             "Course", "Students"])
            for instructor in self.instructors:
                for course_id in instructor.course_list:
                    table.add_row([instructor.cwid, instructor.name, \
                                   instructor.department, course_id, instructor.course_list[course_id]])
        
        elif (collection == "students"):
            table = PrettyTable(field_names=["CWID", "Name", "Major", \
                                             "Completed Courses", \
                                             "Remaining Required", \
                                             "Remaining Electives"])
            for student in self.students:
                #completed_courses = []
                #required = []
                #electives = []
                
                #build list for completed (valid passing grade) courses
                completed_courses = [course for course in student.course_grades.keys() \
                                     if student.course_grades[course] in \
                                         ["A", "A-", "B+", "B", "B-", "C+", "C"]
                                    ]
                #try: #build list of required courses (failing/no grade) courses
                required = [course for course in self.majors[student.major] \
                                #if (student.course_grades[course] not in completed_courses)
                                if (self.majors[student.major][course] == "R") \
                                    and (course not in completed_courses)
                                ]
                #except KeyError:
                #    print("Student took a class not listed in his/her major!")
                
                #try: #Build list of electives (failing/no grade) remaining
                electives = [course for course in self.majors[student.major] \
                                 if (self.majors[student.major][course] == "E") \
                                     and (course not in completed_courses)
                                ]
                #except KeyError:
                #    print("Student took an elective not in his/her major!")

                table.add_row([student.cwid, student.name, student.major, \
                               completed_courses, required, electives])
        
        else:
            raise ValueError("ERROR: Invalid table type for PrettyPrint")

        return table


class Student():
    """ Implementation of students class """
    def __init__(self, cwid, name, major=None):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course_grades = dict()
        
    def add_grade(self, course_id, grade=None):
        """ Manually add a grade to the student """
        self.course_grades[course_id] = grade

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

def main():
    """ Run some testing code to display data from repositories """
    print("Stevens Institute of Technology")
    
    try:
        stevens = Repository("./Stevens")
    except FileNotFoundError:
        print("ERROR:  Unable to access Stevens repository")
    else:
        majors_table = stevens.pretty_print("majors")
        student_table = stevens.pretty_print("students")
        instructor_table = stevens.pretty_print("instructors")
        instructor_db_table = stevens.instructor_table_db("./database")
        print("\nMajors Summary")
        print(majors_table)
        print("\nStudents Summary")
        print(student_table)
        print("\nInstructors Summary")
        print(instructor_table)
        print("\nInstructors Summary (from DB)")
        print(instructor_db_table)
        print("\n\n")
        

        
if __name__ == "__main__":
    main()