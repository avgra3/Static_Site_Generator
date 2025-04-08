import os
import shutil
from extractor import generate_pages_recursive
import sys


# Write a recursive function that copies all files from static dir to public dir
# 1. Delete all contents of the destination directory to ensure that the copy is clean
# 2. Copy all files and subdirectories, nested files, etc.
# 3. Should log the path of each file copied to see what's happening
def remove_old_static():
    buildDir = "docs"
    if os.path.exists(os.path.join(os.getcwd(), buildDir)):
        shutil.rmtree(os.path.join(os.getcwd(), buildDir))
    os.mkdir(os.path.join(os.getcwd(), buildDir))


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
    # Get the arguments passed on start
    basepath = sys.argv[0]
    if basepath == "":
        basepath = "/"

    buildDir = "docs"

    remove_old_static()
    copy_static(STATIC_BASE_DIR="static", PUBLIC_BASE_DIR=buildDir)
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path=buildDir,
    )


if __name__ == "__main__":
    main()
