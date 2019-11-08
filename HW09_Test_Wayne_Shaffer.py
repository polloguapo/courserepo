""" Test cases for HW09 """
import unittest
from HW09_Wayne_Shaffer import Repository, Person, Student, Instructor

class TestRepository(unittest.TestCase):
    """ Class containing unit test cases for class Repository """
    def setUp(self):
        """ Initial setup code for unit tests """
        self.stevens = Repository("./Stevens")
        self.njit = Repository("./NJIT")

    def test_add_instructor(self):
        """ Test cases for add_instructor """
        pass

    def test_add_student(self):
        """ Test cases for add_student """
        pass

    def test_pretty_print(self):
        """ Test cases for pretty_print """
        

class TestStudent(unittest.TestCase):
    """ Test cases for class Student """
    def setUp(self):
        """ Initial setup code """

    def add_grade(self):
        """ Test cases for add_grade """

class TestInstructor(unittest.TestCase):
    """ Test cases for class Instructor """
    def setUp(self):
        """ Initial setup code """

    def add_course(self):
        """ Test cases for add_course """


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    