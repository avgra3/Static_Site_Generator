import unittest
from block_markdown import markdown_to_blocks, block_to_block_type


class TestBlockMarkdown(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is a single block!"
        expeceted = [markdown]
        self.assertListEqual(markdown_to_blocks(markdown), expeceted)

    def test_multiple_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    """* This is the first list item in a list block
* This is a list item
* This is another list item"""]
        self.assertListEqual(markdown_to_blocks(markdown), expected)

    def test_block_to_block_type_heading(self):
        input1 = "# H1"
        input2 = "## H2"
        input3 = "###### H6"
        expected1 = "heading"

        input4 = "THIS SHOULD NOT MATCH ### "
        input5 = "THIS SHOULD # NOT MATCH"
        input6 = "#THIS SHOULD NOT MATCH"
        input7 = "THIS SHOULD NOT MATCH"
        expected2 = "paragraph"

        self.assertEqual(block_to_block_type(input1), expected1)
        self.assertEqual(block_to_block_type(input2), expected1)
        self.assertEqual(block_to_block_type(input3), expected1)
        self.assertEqual(block_to_block_type(input4), expected2)
        self.assertEqual(block_to_block_type(input5), expected2)
        self.assertEqual(block_to_block_type(input6), expected2)
        self.assertEqual(block_to_block_type(input7), expected2)

    def test_block_to_block_type_quote(self):
        input1 = "> This should match"
        expected1 = "quote"

        input2 = "THIS SHOULD NOT MATCH > "
        input3 = ">> THIS SHOULD NOT MATCH"
        input4 = ">THIS SHOULD NOT MATCH"
        input5 = "THIS SHOULD NOT MATCH"
        expected2 = "paragraph"

        self.assertEqual(block_to_block_type(input1), expected1)
        self.assertEqual(block_to_block_type(input2), expected2)
        self.assertEqual(block_to_block_type(input3), expected2)
        self.assertEqual(block_to_block_type(input4), expected2)
        self.assertEqual(block_to_block_type(input5), expected2)

    def test_block_to_block_type_unordered_list(self):
        input1 = """- This is part of a list\n- This is also part of a list\n- Item 3 in the list"""
        input2 = """* This is part of a list\n* This is also part of a list\n* Item 3 in the list"""
        expecetd1 = "unordered_list"

        self.assertEqual(block_to_block_type(input1), expecetd1)
        self.assertEqual(block_to_block_type(input2), expecetd1)

        input3 = """-This is not an ordered list"""
        input4 = """*This is not an ordered list"""
        input5 = """* This is part of a list\n*This is not part of a list"""
        expecetd2 = "paragraph"

        self.assertEqual(block_to_block_type(input3), expecetd2)
        self.assertEqual(block_to_block_type(input4), expecetd2)
        self.assertEqual(block_to_block_type(input5), expecetd1)

    def test_block_to_block_type_ordered_list(self):
        input1 = """1. Should be found\n2. Should be found\n3. Should be found\n4. Should be found"""
        expected1 = "ordered_list"

        input2 = "SHOULD NOT BE FOUND"
        input3 = "4.SHOULD NOT BE FOUND"
        input4 = "SHOULD NOT BE FOUND 1. "
        input5 = "SHOULD NOT 1. BE FOUND"
        expected2 = "paragraph"

        self.assertEqual(block_to_block_type(input1), expected1)
        self.assertEqual(block_to_block_type(input2), expected2)
        self.assertEqual(block_to_block_type(input3), expected2)
        self.assertEqual(block_to_block_type(input4), expected2)
        self.assertEqual(block_to_block_type(input5), expected2)

    def test_block_to_block_type_paragraph(self):
        input = "This is a paragraph!"
        expecetd = "paragraph"
        self.assertEqual(block_to_block_type(input), expecetd)


if __name__ == "__main__":
    unittest.main()
