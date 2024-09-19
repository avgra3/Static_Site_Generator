class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
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
                output += f" {key}={value}"

        return output

    def __repr__(self):
        children = ""
        if self.children:
            for child in self.children:
                children += f" {child}"
        return f"HTMLNODE(tag={self.tag}, value={self.value}, children=[{children}], props={self.props})"
