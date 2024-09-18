from textnode import TextNode


def main():
    dummy = TextNode(text="This is a text node",
                     text_type="bold", url="https://www.boot.dev")

    print(dummy)


if __name__ == "__main__":
    main()
