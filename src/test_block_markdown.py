import unittest
from block_markdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
