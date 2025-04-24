from textnode import TextType, TextNode

def main():
    node = TextNode("Hello fool!", TextType.Bold, "www.example.com")
    print(node)

main()