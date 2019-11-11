""" Test cases for HW09 """
import unittest
from courserepo_Wayne_Shaffer import Repository, Student, Instructor


class TestRepository(unittest.TestCase):
    """ Class containing unit test cases for class Repository """
    def setUp(self):
        """ Initial setup code for unit tests """
        self.stevens = Repository("./Stevens")
        self.NJIT = Repository("./NJIT")
        self.test_repo = None
        
    def test_bad_path(self):
        """ Test cases for bad directory path """
        try:
            self.test_repo = Repository("./Missing")
        except FileNotFoundError:
            print("ERROR:  Unable to access ./Missing")
            self.assertTrue(True)
        
    def test_corrupted_data(self):
        """ Test case for corrupted data """
        try:
            self.test_repo = Repository("./Corrupted")
        except ValueError:
            print("ERROR: Corrupted files found importing Corrupted University data")
            self.assertTrue(True)

    def test_pretty_print(self):
        """ Test cases for pretty_print """
        table_rows = ["98765  Einstein, A  SFEN  SSW 567  4", \
                      "98765  Einstein, A  SFEN  SSW 540  3", \
                      "98764  Feynman, R  SFEN  SSW 564  3", \
                      "98764  Feynman, R  SFEN  SSW 687  3", \
                      "98764  Feynman, R  SFEN  CS 501  1", \
                      "98764  Feynman, R  SFEN  CS 545  1", \
                      "98763  Newton, I  SFEN  SSW 555  1", \
                      "98763  Newton, I  SFEN  SSW 689  1", \
                      "98760  Darwin, C  SYEN  SYS 800  1", \
                      "98760  Darwin, C  SYEN  SYS 750  1", \
                      "98760  Darwin, C  SYEN  SYS 611  2", \
                      "98760  Darwin, C  SYEN  SYS 645  1"
        ]
        result_table = self.stevens.pretty_print("instructors")
        result_table.border = False
        result_table.header = False
        index = 0
        for row in result_table:
            row_str = row.get_string().strip()
            self.assertTrue(row_str == table_rows[index])
            index += 1
        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    