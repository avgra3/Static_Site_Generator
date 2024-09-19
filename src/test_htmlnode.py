import unittest
from htmlnode import HTMLNode


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
        expected = " value=key other_value=other_key"
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


if __name__ == "__main__":
    unittest.main()
