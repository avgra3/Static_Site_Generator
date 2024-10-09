import re
from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


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
        leaf_nodes = []
        block_type = block_to_block_type(block)
        if block_type == "quote":
            updated_block = block.replace(">", "").strip()
            text_nodes = text_to_textnodes(updated_block)
            for node in text_nodes:
                leaf_nodes.append(text_node_to_html_node(node))
            leaf_node = ParentNode(tag="blockquote", children=leaf_nodes)
        if block_type == "paragraph":
            text_node = text_to_textnodes(block)
            # leaf_nodes = []
            for node in text_node:
                leaf_nodes.append(text_node_to_html_node(node))
            leaf_node = ParentNode(tag="p", children=leaf_nodes)
        if block_type == "heading":
            header_level = block.index(" ", 0)
            leaf_node = LeafNode(
                tag=f"h{header_level}", value=block.replace("#", "").strip()
            )
        if block_type == "unordered_list":
            list_children = []
            lines_of_block = block.split("\n")
            for line in lines_of_block:
                text_nodes = text_to_textnodes(line.lstrip("* ").lstrip("- "))
                inner_children = []
                for node in text_nodes:
                    inner_children.append(text_node_to_html_node(node))
                inner_leaf_node = ParentNode(tag="li", children=inner_children)
                list_children.append(inner_leaf_node)
            leaf_node = ParentNode(tag="ul", children=list_children)
        if block_type == "ordered_list":
            list_children = []
            lines_of_block = block.split("\n")
            for line in lines_of_block:
                # line[:2].strip()
                text_nodes = text_to_textnodes(line[2:].strip())
                inner_children = []
                for node in text_nodes:
                    inner_children.append(text_node_to_html_node(node))
                inner_leaf_node = ParentNode(tag="li", children=inner_children)
                list_children.append(inner_leaf_node)
            leaf_node = ParentNode(tag="ol", children=list_children)
        if block_type == "code":
            inner_html = LeafNode(tag="code", value=block.replace("`", ""), props=None)
            leaf_node = ParentNode(tag="pre", children=[inner_html])
        if isinstance(leaf_node, list):
            child_html_nodes.extend(leaf_node)
            continue
        child_html_nodes.append(leaf_node)
    return ParentNode(tag="div", children=child_html_nodes, props=None)
