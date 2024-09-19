import unittest
from htmlnode import HTMLNode, LeafNode


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


if __name__ == "__main__":
    unittest.main()
