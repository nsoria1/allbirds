import unittest
import modules.file_handler as fh
import modules.csv_processor as cp

TEST_CASE = [('/Users/nsoria/Documents/github/allbirds/specs/testformat1.csv', '/Users/nsoria/Documents/github/allbirds/data/testformat1_2020-06-28.txt')]

class TestFileHandler(unittest.TestCase):
    def test_file_handler_output(self):
        raw = fh.FileHandler()
        data = raw.spec_and_file()
        self.assertEqual(data, TEST_CASE)

    def test_csv_schema_dict(self):
        raw = cp.CsvProcessor(TEST_CASE[0])
        raw.load_schema()
        data = raw.schema_dict
        self.assertEqual(type(data), dict)

    def test_csv_schema_data(self):
        raw = cp.CsvProcessor(TEST_CASE[0])
        raw.load_schema()
        data = raw.schema_dict
        self.assertDictEqual(data, {0: ['name', 10, 'TEXT'], 1: ['valid', 1, 'BOOLEAN'], 2: ['count', 3, 'INTEGER']})

if __name__ == '__main__':
    unittest.main()