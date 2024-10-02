import re


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        if block != "":
            blocks.append(block.strip())
    return blocks


def block_to_block_type(block: str) -> str:
    # Want to return a string representing
    # the type of block it is.
    # Assume all leading and trailing whitespace
    # was already sripped
    # HEADINGS: start with 1-5 "#" followed by a space then heading text
    # CODE: start with 3 "`" and end with 3 "`"
    # QUOTE: must start with ">"
    # UNORDERED LIST: Must start with "*" or "-" followed by a space
    # ORDERED LIST: Must start with a number followed by "." and space,
    #   must start with 1 and increment by 1 for each line
    # ELSE: normal paragraph
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
