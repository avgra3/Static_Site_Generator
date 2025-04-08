from block_markdown import markdown_to_html_node
import os


def extract_title(markdown: str) -> str:
    # Pull the h1 header from the markdown file and returns it
    # If there is no h1, raise an exception
    for line in markdown.strip().split("\n"):
        if line[0:2] == "# ":
            return line[2:].strip()
    raise Exception("There is no header!")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
) -> None:
    message = f"Generating page {from_path} to {dest_path} using {template_path}"
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    updated_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    dest_dirs = "".join(dest_path.split("/")[:-1])
    print(f"Dest path: {dest_path}")
    print(f"Dest dirs: {dest_dirs}")
    # os.makedirs(os.path.join(dest_dirs), exist_ok=True)
    new_file_name = from_path.split("/")[-1].replace("md", "html")
    print(f"New file name: {new_file_name}")
    output_path = os.path.join(dest_dirs, new_file_name)
    print(f"New output file: {output_path}")
    with open(dest_path.replace("md", "html"), "w") as file:
        file.write(updated_html)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str = "/",
):
    items_in_dir = os.listdir(dir_path_content)
    for item in items_in_dir:
        static = os.path.join(dir_path_content, item)
        copied = os.path.join(dest_dir_path, item)
        print(f"Static: {static}")
        print(f"Copied: {copied}")
        if os.path.isfile(static) and static.endswith(".md"):
            message = f"Generating page {static} to {copied} using {template_path}"
            generate_page(
                from_path=static,
                template_path=template_path,
                dest_path=copied,
                basepath=basepath,
            )
        if os.path.isdir(static):
            if not os.path.exists(copied):
                os.mkdir(copied)
                print(f"Directory made: {copied}")
            generate_pages_recursive(
                dir_path_content=static,
                template_path=template_path,
                dest_dir_path=copied,
            )
