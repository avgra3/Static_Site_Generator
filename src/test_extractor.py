import unittest
from extractor import extract_title


class TestExtractor(unittest.TestCase):
    def test_extract_title_base(self):
        input = "# Hello"
        expected = "Hello"
        self.assertEqual(extract_title(input), expected)

    def test_extract_title_exception(self):
        input = "Hello"
        with self.assertRaises(Exception):
            extract_title(input)

    def test_extract_title_not_first_line(self):
        input = "This is not a title\n# This is a title"
        expected = "This is a title"
        self.assertEqual(extract_title(input), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
