class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[any] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output = ""
        if self.props:
            for key, value in self.props.items():
                output += f' {key}="{value}"'

        return output

    def __repr__(self):
        children = ""
        if self.children:
            for child in self.children:
                children += f" {child}"
        return f"HTMLNODE(tag={self.tag}, value={self.value}, children=[{children}], props={self.props})"


class LeafNode(HTMLNode):
    # No children allowed
    # Value is required
    def __init__(self, value: str, tag: str = None, props: dict = None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        # If no vlaue: raise Value error
        if not self.value:
            raise ValueError("Value cannot be None!")
        # If no tag, should return the value as raw text
        if not self.tag:
            return f"{self.value}"
        # Render an html tag
        props_text = ""
        if self.props:
            props_text = f"{self.props_to_html()}"
        return f"<{self.tag}{props_text}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    # No value
    # Children must be included
    def __init__(self, children: list[HTMLNode], tag: str = None, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("You must include a tag!")
        if not self.children:
            raise ValueError("You must include the list of children!")
        # For each node in children, we want to call to_html
        output = ""
        for node in self.children:
            output += node.to_html()
        props_text = ""
        if self.props:
            for key, value in self.props.items():
                props_text += f" {key}=\"{value}\""
        return f"<{self.tag}{props_text}>{output}</{self.tag}>"
