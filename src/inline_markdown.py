from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        inner_nodes = []
        # Need to raise an error if there is not a closing delimiter
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0 and "http" not in node.text:
            print(f"NODE => {node.text}")
            raise Exception("No closing delimiter!")
        for i in range(len(sections)):
            if sections[i] == "":
                # We don't want to add empty text to our nodes
                continue
            if i % 2 == 0:
                inner_nodes.append(TextNode(text=sections[i], text_type=text_type_text))
            else:
                inner_nodes.append(TextNode(text=sections[i], text_type=text_type))
        new_nodes.extend(inner_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    # Each tuple contains the alt text and URL of markdown images
    regex_expression = r"!\[(.*?)\]\((.*?)\)"
    image_list = re.findall(regex_expression, text)
    return image_list


def extract_markdown_links(text: str) -> list[tuple]:
    regex_expression = r"(?<!!)\[(.*?)\]\((.*?)\)"
    link_list = re.findall(regex_expression, text)
    return link_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        # If no images, just append the node to list
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for image in images:
            alt_text = image[0]
            image_url = image[1]
            sections = original_text.split(f"![{alt_text}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown! Image section not closed!")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(text=sections[0], text_type=text_type_text, url=None)
                )
            new_nodes.append(
                TextNode(text=alt_text, text_type=text_type_image, url=image_url)
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        # If no links, just append the node to list
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for link in links:
            alt_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{alt_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown! Link section not closed!")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        text=sections[0],
                        text_type=text_type_text,
                        url=None,
                    )
                )
            new_nodes.append(
                TextNode(text=alt_text, text_type=text_type_link, url=link_url)
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text=text, text_type=text_type_text)]
    new_nodes = split_nodes_delimiter(
        old_nodes=new_nodes, delimiter="**", text_type=text_type_bold
    )
    new_nodes = split_nodes_delimiter(
        old_nodes=new_nodes, delimiter="__", text_type=text_type_bold
    )
    new_nodes = split_nodes_delimiter(
        old_nodes=new_nodes, delimiter="*", text_type=text_type_italic
    )
    new_nodes = split_nodes_delimiter(
        old_nodes=new_nodes, delimiter="_", text_type=text_type_italic
    )
    new_nodes = split_nodes_delimiter(
        old_nodes=new_nodes, delimiter="`", text_type=text_type_code
    )
    new_nodes = split_nodes_link(old_nodes=new_nodes)
    new_nodes = split_nodes_image(old_nodes=new_nodes)
    return new_nodes
