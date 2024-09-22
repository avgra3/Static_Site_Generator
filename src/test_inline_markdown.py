import unittest
from inline_markdown import split_nodes_delimiter
from textnode import (TextNode, text_type_text, text_type_code,
                      text_type_bold, text_type_image, text_type_link, text_type_italic)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("Unclosed **bold delimiter!", text_type_text)
        with self.assertRaises(Exception):
            new_node = split_nodes_delimiter(
                old_nodes=[node], delimiter="**", text_type=text_type_bold)

    def test_multiple_delims(self):
        node = TextNode(
            "This has two code blocks: `print(\"Hello world!\")` and `print(\"Goodbye world!\")`", text_type_text
        )
        expected = [
            TextNode("This has two code blocks: ", text_type_text),
            TextNode("print(\"Hello world!\")", text_type_code),
            TextNode(" and ", text_type_text),
            TextNode("print(\"Goodbye world!\")", text_type_code),
        ]
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
