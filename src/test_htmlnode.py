import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(tag=None, value=None, children=None, props=None)
        node2 = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertEqual(repr(node1), repr(node2))

        node3 = HTMLNode(tag="href", value=None, children=None, props=None)
        node4 = HTMLNode(tag="href")
        self.assertEqual(repr(node3), repr(node4))

    def test_props_to_html(self):
        props = {"value": "key", "other_value": "other_key"}
        node = HTMLNode(props=props)
        expected = ' value="key" other_value="other_key"'
        self.assertEqual(node.props_to_html(), expected)

        node2 = HTMLNode()
        expected2 = ""
        self.assertEqual(node2.props_to_html(), expected2)

        node4 = HTMLNode(props=props)
        node5 = HTMLNode(tag="href", value="Hello world",
                         children=None, props=props)
        self.assertEqual(node4.props_to_html(), node5.props_to_html())

    def test_to_html_not_impl(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_raises_no_value(self):
        node = LeafNode(value=None, tag=None, props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html(self):
        # Test No tag
        node1 = LeafNode(value="Text only!")
        expected1 = "Text only!"
        self.assertEqual(node1.to_html(), expected1)

        # Test No props
        node2 = LeafNode(value="This is a paragraph of text.", tag="p")
        expected2 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node2.to_html(), expected2)

        # Test with props
        node3 = LeafNode(value="Click me!", tag="a", props={
                         "href": "https://www.google.com"})
        expected3 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node3.to_html(), expected3)


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        child_node = LeafNode(value="Click me!", tag="a", props={
                              "href": "https://google.com"})
        parent_node = ParentNode(children=[child_node], tag=None, props=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_no_children(self):
        parent_node = ParentNode(children=None, tag="p", props=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_hmtl(self):
        # Multiple LeafNodes, mix of tag and no tag in children
        node1 = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        expected1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node1.to_html(), expected1)

        # One LeafNode with no tags
        node2 = ParentNode(tag="h3", children=[
                           LeafNode(tag=None, value="We have no tag")])
        expected2 = "<h3>We have no tag</h3>"
        self.assertEqual(node2.to_html(), expected2)

        # Parent node with props
        node3 = ParentNode(tag="a", children=[LeafNode(
            tag=None, value="We have no tag!")], props={"href": "https://boot.dev"})
        expected3 = "<a href=\"https://boot.dev\">We have no tag!</a>"
        self.assertEqual(node3.to_html(), expected3)

    def test_nested_parent_nodes(self):
        node1 = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        node2 = ParentNode(tag="h3", children=[
                           LeafNode(tag=None, value="We have no tag")])
        node3 = ParentNode(tag="a", children=[LeafNode(
            tag=None, value="We have no tag!")], props={"href": "https://boot.dev"})
        big_node = ParentNode(tag="h2", children=[node1, node2, node3])
        big_node_to_html = big_node.to_html()
        expected = "<h2><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><h3>We have no tag</h3><a href=\"https://boot.dev\">We have no tag!</a></h2>"
        self.assertEqual(big_node_to_html, expected)


if __name__ == "__main__":
    unittest.main()
