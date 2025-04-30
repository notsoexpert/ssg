import unittest

from htmlnode import BlockType, HTMLNode, LeafNode, ParentNode
from conversions import markdown_to_blocks, block_to_block_type

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Click this link!", None, {"href":"https://boot.dev"})
        node2 = HTMLNode("a", "Click this link!", None, {"href":"https://boot.dev"})
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_output(self):
        node = HTMLNode("a", "Don't click this link!", None, {"href":"https://boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://boot.dev\"")

    def test_output_2(self):
        node = HTMLNode("a", "Google it.", None, {"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Go To Boot.Dev!", {"href":"https://boot.dev", "target":"_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://boot.dev\" target=\"_blank\">Go To Boot.Dev!</a>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "THIS IS IMPORTANT!")
        self.assertEqual(node.to_html(), "<b>THIS IS IMPORTANT!</b>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_high_bredth(self):
        lots_of_children = []
        for i in range(0, 10):
            lots_of_children.append(LeafNode("b" if i % 2 == 0 else "i", "child"))
        parent_node = ParentNode("div", lots_of_children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child</b><i>child</i><b>child</b><i>child</i><b>child</b><i>child</i><b>child</b><i>child</i><b>child</b><i>child</i></div>",
        )

    def test_to_html_with_high_depth(self): 
        parent_node = ParentNode("div",[ParentNode("span",[ParentNode("span",[ParentNode("span",[ParentNode("span",[LeafNode("b", "greatgreatgreatgrandchild")])])])])])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><span><span><span><b>greatgreatgreatgrandchild</b></span></span></span></span></div>"
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """

Check out this link: [Click Here!](www.youtube.com)

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
Check out this link, too: [And Here!](www.google.com)

- This is a list
- with items
- and an image: ![it's an image idiot](https://i.imgur.com/fJRm4Vk.jpeg) <- right there
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Check out this link: [Click Here!](www.youtube.com)",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nCheck out this link, too: [And Here!](www.google.com)",
                "- This is a list\n- with items\n- and an image: ![it's an image idiot](https://i.imgur.com/fJRm4Vk.jpeg) <- right there",
            ],
        )
    
    def test_block_to_block_type_1(self):
        md = """

Check out this link: [Click Here!](www.youtube.com)

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
Check out this link, too: [And Here!](www.google.com)

- This is a list
- with items
- and an image: ![it's an image idiot](https://i.imgur.com/fJRm4Vk.jpeg) <- right there

> "I think you're an idiot."
> - Steven Hawking, probably

1. This is an ordered list...
2. With multiple...
3. Items...

```python is for snakes```

idiot
    """
        blocks = markdown_to_blocks(md)
        print(f"Blocks of length: {len(blocks)}\nBlocks:\n{blocks}")
        block_types = list(map(block_to_block_type, blocks))
        print(f"Block types of length: {len(block_types)}\n{block_types}")
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.QUOTE,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.PARAGRAPH
            ]
        )

    def test_block_to_block_type_1(self):
            md = """
- t

- h
- i

- s

-s-s-s-s

```lol

``no``

`MORON`

!. nope

1.yep

0. NO!

< HAHA

>kek

#egay

```This is long code...
you know...```

bigot
    """
            def print_b2bt(md):
                type = block_to_block_type(md)
                print(f"Block type: {type}")
                return type
            
            blocks = markdown_to_blocks(md)
            print(f"Blocks of length: {len(blocks)}\nBlocks:\n{blocks}")
            block_types = list(map(print_b2bt, blocks))
            print(f"Block types of length: {len(block_types)}\n{block_types}")
            self.assertEqual(
                block_types,
                [
                    BlockType.UNORDERED_LIST,
                    BlockType.UNORDERED_LIST,
                    BlockType.UNORDERED_LIST,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.QUOTE,
                    BlockType.PARAGRAPH,
                    BlockType.CODE,
                    BlockType.PARAGRAPH
                ]
            )
        
if __name__ == "__main__":
    unittest.main()