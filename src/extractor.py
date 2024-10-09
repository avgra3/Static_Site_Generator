from block_markdown import markdown_to_html_node
import os


def extract_title(markdown: str) -> str:
    # Pull the h1 header from the markdown file and returns it
    # If there is no h1, raise an exception
    for line in markdown.strip().split("\n"):
        if line[0:2] == "# ":
            return line[2:].strip()
    raise Exception("There is no header!")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    message = f"Generating page {from_path} to {dest_path} using {template_path}"
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    updated_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_dirs = "".join(dest_path.split("/")[:-1])
    os.makedirs(os.path.join(dest_dirs), exist_ok=True)
    new_file_name = from_path.split("/")[-1].replace("md", "html")
    print(new_file_name)
    with open(os.path.join(dest_dirs, new_file_name), "w") as file:
        file.write(updated_html)
