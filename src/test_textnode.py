import unittest
from textnode import TextNode


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", "bold", "https://google.com")
        node4 = TextNode("This is a text node", "bold", "https://google.com")
        self.assertEqual(node3, node4)

    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", "bold", "https://google.com")
        node4 = TextNode("This is a text node", "bold", "https://yahoo.com")
        self.assertNotEqual(node3, node4)

        node5 = TextNode("This is a text node", "bold")
        node6 = TextNode("This is not a text node", "bold")
        self.assertNotEqual(node5, node6)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        expected = "TextNode(TEXT: This is a text node, TEXT_TYPE: bold, URL: None)"
        self.assertEqual(node.__repr__(), expected)


if __name__ == "__main__":
    unittest.main()
