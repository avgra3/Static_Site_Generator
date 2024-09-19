from htmlnode import LeafNode

# Acceptable Node text types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode(TEXT: {self.text}, TEXT_TYPE: {self.text_type}, URL: {self.url})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(tag=None, value=text_node.text, props=None)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text, props=None)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text, props=None)
    if text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text, props=None)
    if text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    error_message = f"The text_type '{text_node.text_type}' not allowed"
    raise ValueError(error_message)
