import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNodeToLeafNode(unittest.TestCase):
    def test_text(self):
        input_node = TextNode(
            text="This should just be text", text_type="text", url=None)
        expected_node = LeafNode(
            tag=None, value="This should just be text", props=None)
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_bold(self):
        input_node = TextNode(text="This is bold!", text_type="bold", url=None)
        expected_node = LeafNode(tag="b", value="This is bold!", props=None)
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_italic(self):
        input_node = TextNode(text="This is italics!",
                              text_type="italic", url=None)
        expected_node = LeafNode(tag="i", value="This is italics!", props=None)
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_code(self):
        input_node = TextNode(text="print(\"Hello World!\")",
                              text_type="code", url=None)
        expected_node = LeafNode(
            tag="code", value="print(\"Hello World!\")", props=None)
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_image(self):
        url_image = "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"
        input_node = TextNode(text="This is an image",
                              text_type="image", url=url_image)
        expected_node = LeafNode(tag="img", value="", props={
                                 "src": url_image, "alt": "This is an image"})
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_link(self):
        url_link = "https://boot.dev"
        input_node = TextNode(text="We have a link!",
                              text_type="link", url=url_link)
        expected_node = LeafNode(
            tag="a", value="We have a link!", props={"href": url_link})
        self.assertEqual(text_node_to_html_node(
            input_node).to_html(), expected_node.to_html())

    def test_raises_error(self):
        text_type1 = "not text"
        text_type2 = ""
        text_type3 = None
        text_type4 = 1
        text_type5 = "text image link code bold italic"
        node1 = TextNode(text="This is some text", text_type=text_type1)
        node2 = TextNode(text="This is some text", text_type=text_type2)
        node3 = TextNode(text="This is some text", text_type=text_type3)
        node4 = TextNode(text="This is some text", text_type=text_type4)
        node5 = TextNode(text="This is some text", text_type=text_type5)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node1)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node2)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node3)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node4)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node5)


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
