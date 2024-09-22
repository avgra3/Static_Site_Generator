from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        # Need to raise an error if there is not a closing delimiter
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception(f"No closing delimiter \"{delimiter}\" found!")
        inner_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                # We don't want to add empty text to our nodes
                continue
            if i % 2 == 0:
                inner_nodes.append(
                    TextNode(text=sections[i], text_type=text_type_text))
            else:
                inner_nodes.append(
                    TextNode(text=sections[i], text_type=text_type))
        new_nodes.extend(inner_nodes)
        return new_nodes
