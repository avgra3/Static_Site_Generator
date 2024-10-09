from textnode import TextNode
import os
import shutil
from extractor import generate_page


# Write a recursive function that copies all files from static dir to public dir
# 1. Delete all contents of the destination directory to ensure that the copy is clean
# 2. Copy all files and subdirectories, nested files, etc.
# 3. Should log the path of each file copied to see what's happening
def remove_old_static():
    if os.path.exists(os.path.join(os.getcwd(), "public")):
        shutil.rmtree(os.path.join(os.getcwd(), "public"))
    os.mkdir(os.path.join(os.getcwd(), "public"))


def copy_static(STATIC_BASE_DIR: str, PUBLIC_BASE_DIR: str):
    items_in_dir = os.listdir(STATIC_BASE_DIR)
    for item in items_in_dir:
        static = os.path.join(STATIC_BASE_DIR, item)
        copied = os.path.join(PUBLIC_BASE_DIR, item)
        if os.path.isfile(static):
            shutil.copy(src=static, dst=copied)
            print(f"src={static} ==> dst={copied}")
        if os.path.isdir(static):
            # Make the directory if not exist
            if not os.path.exists(copied):
                os.mkdir(copied)
                print(f"Directory made: {copied}")
            copy_static(STATIC_BASE_DIR=static, PUBLIC_BASE_DIR=copied)


def main():
    remove_old_static()
    copy_static(STATIC_BASE_DIR="static", PUBLIC_BASE_DIR="public")
    content = os.listdir("content")
    for item in content:
        generate_page(
            from_path=os.path.join("content", item),
            template_path="template.html",
            dest_path=os.path.join("public", item),
        )


if __name__ == "__main__":
    main()
