from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode

def main():
    node = TextNode("Hello fool!", TextType.BOLD, "www.example.com")
    print(node)

main()