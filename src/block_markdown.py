import re
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, text_node_to_html_node, text_type_text


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks


def block_to_block_type(block: str) -> str:
    heading_regex = r"(^|\r|\n|\r\n)#{1,6} .*"
    quote_regex = r"(^|\r|\n|\r\n)> .*"
    unordered_list_regex = r"(^|\r|\n|\r\n)(\-|\*) .*"
    ordered_list_regex = r"(^|\r|\n|\r\n)\d\. .*"
    if re.search(heading_regex, block):
        return "heading"
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    if re.search(quote_regex, block):
        return "quote"
    if re.search(unordered_list_regex, block):
        return "unordered_list"
    if re.search(ordered_list_regex, block):
        initial = 1
        incremented = block.split("\n")
        for line in incremented:
            if initial != line[0]:
                break
            initial += 1
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown: str) -> HTMLNode:
    child_html_nodes = []
    # Split markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "quote":
            leaf_node = LeafNode(
                tag="blockquote", value=block.replace(">", "").strip(), )
        if block_type == "paragraph":
            leaf_node = LeafNode(tag="p", value=block,
                                 props=None)
        if block_type == "heading":
            header_level = block.index(" ", 0)
            leaf_node = LeafNode(
                tag=f"h{header_level}", value=block.replace("#", "").strip())
        if block_type == "unordered_list":
            list_children = []
            lines_of_block = block.split("\n")
            for line in lines_of_block:
                inner_leaf_node = LeafNode(
                    tag="li", value=line.lstrip("* ").lstrip("- "))
                list_children.append(inner_leaf_node)
                leaf_node = ParentNode(tag="ul", children=list_children)
        if block_type == "ordered_list":
            list_children = []
            lines_of_block = block.split("\n")
            for line in lines_of_block:
                inner_leaf_node = LeafNode(tag="li", value=line[2:].strip())
                list_children.append(inner_leaf_node)
                leaf_node = ParentNode(
                    tag="ol", children=list_children)
        if block_type == "code":
            inner_html = LeafNode(
                tag="code", value=block.replace("`", ""), props=None)
            leaf_node = ParentNode(
                tag="pre", children=[inner_html])
        child_html_nodes.append(leaf_node)
    return ParentNode(tag="div", children=child_html_nodes, props=None)
