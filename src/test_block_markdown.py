import unittest
from block_markdown import (markdown_to_blocks,
                            block_to_block_type,
                            markdown_to_html_node,
                            )
from htmlnode import ParentNode, LeafNode


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

    def test_markdown_to_html_node_paragraph(self):
        input = "This is a paragraph"
        output = markdown_to_html_node(input)
        expected = ParentNode(tag="div", children=[
            LeafNode(tag="p", value=input)], props=None)
        self.assertEqual(output.to_html(), expected.to_html())

    def test_markdown_to_html_node_quote(self):
        input = "```print('Hello world!')```"
        output = markdown_to_html_node(input)
        expected = ParentNode(tag="div", children=[ParentNode(tag="pre", children=[
                              LeafNode(tag="code", value="print('Hello world!')")])])
        self.assertEqual(
            output.to_html(), expected.to_html())

    def test_markdown_to_html_node_unordered_list(self):
        input = "* This is a one item list\n* This is a second item list"
        output = markdown_to_html_node(input)
        children = [LeafNode(tag="li", value=input.split("\n")[0][2:]), LeafNode(
            tag="li", value=input.split("\n")[1][2:])]
        parent_inner = ParentNode(tag="ul", children=children)
        expected = ParentNode(tag="div", children=[parent_inner])
        self.assertEqual(output.to_html(), expected.to_html())

    def test_markdown_to_html_node_ordered_list(self):
        input = "1. This is a one item list\n2. This is a second item list"
        output = markdown_to_html_node(input)
        children = [LeafNode(tag="li", value="This is a one item list"), LeafNode(
            tag="li", value="This is a second item list")]
        parent_inner = ParentNode(tag="ol", children=children)
        expected = ParentNode(tag="div", children=[parent_inner])
        self.assertEqual(output.to_html(), expected.to_html())

    def test_markdown_to_html_node_heading(self):
        input1 = "# H1"
        input2 = "## H2"
        input3 = "### H3"
        input4 = "#### H4"
        input5 = "##### H5"
        input6 = "###### H6"
        expected1 = ParentNode(tag="div", children=[LeafNode(
            tag="h1", value="H1")])
        actual1 = markdown_to_html_node(input1)
        expected2 = ParentNode(tag="div", children=[
                               LeafNode(tag="h2", value="H2")])
        actual2 = markdown_to_html_node(input2)
        expected3 = ParentNode(tag="div", children=[
                               LeafNode(tag="h3", value="H3")])
        actual3 = markdown_to_html_node(input3)
        expected4 = ParentNode(tag="div", children=[
                               LeafNode(tag="h4", value="H4")])
        actual4 = markdown_to_html_node(input4)
        expected5 = ParentNode(tag="div", children=[
                               LeafNode(tag="h5", value="H5")])
        actual5 = markdown_to_html_node(input5)
        expected6 = ParentNode(tag="div", children=[
                               LeafNode(tag="h6", value="H6")])
        actual6 = markdown_to_html_node(input6)

        self.assertEqual(actual1.to_html(), expected1.to_html())
        self.assertEqual(actual2.to_html(), expected2.to_html())
        self.assertEqual(actual3.to_html(), expected3.to_html())
        self.assertEqual(actual4.to_html(), expected4.to_html())
        self.assertEqual(actual5.to_html(), expected5.to_html())
        self.assertEqual(actual6.to_html(), expected6.to_html())

    def test_markdown_to_html_mixed(self):
        input = "# Header\n\n```print('hello world!')```\n\n1. Item one\n2. Item two\n\n* Unordered\n* Unordered\n\n> This is a quote"
        actual = markdown_to_html_node(input)
        inner_expected1 = LeafNode(tag="h1", value="Header")
        inner_expected2 = ParentNode(
            tag="pre", children=[LeafNode(tag="code", value="print('hello world!')")])
        inner_expected3 = ParentNode(tag="ol", children=[LeafNode(
            tag="li", value="Item one"), LeafNode(tag="li", value="Item two")])
        inner_expected4 = ParentNode(tag="ul", children=[LeafNode(
            tag="li", value="Unordered"), LeafNode(tag="li", value="Unordered")])
        inner_expected5 = LeafNode(tag="blockquote", value="This is a quote")
        expected = ParentNode(tag="div", children=[
                              inner_expected1, inner_expected2, inner_expected3, inner_expected4, inner_expected5])
        self.assertEqual(actual.to_html(), expected.to_html())


if __name__ == "__main__":
    unittest.main(verbosity=2)
