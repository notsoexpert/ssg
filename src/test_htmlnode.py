import unittest

from htmlnode import BlockType, HTMLNode, LeafNode, ParentNode
from conversions import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

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
            
            blocks = markdown_to_blocks(md)
            block_types = list(map(block_to_block_type, blocks))
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
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Head1

## Head2

### Head3

#### Head4

##### Head5

###### Head 6
CHECKING
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Head1</h1><h2>Head2</h2><h3>Head3</h3><h4>Head4</h4><h5>Head5</h5><h6>Head 6 CHECKING</h6></div>",
        )
    
    def test_quote(self):
        md = """
> Quote 1 with **bold** text

> Quote 2 with > < angle brackets and _italic_ text

> Quote 3 with **bold** and _italic_ text

> Quote 4 with nothing else

> Quote 5 with a `code` section next to an _italic_ section

> Quote 6 with a [link](www.google.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote 1 with <b>bold</b> text</blockquote><blockquote>Quote 2 with > < angle brackets and <i>italic</i> text</blockquote><blockquote>Quote 3 with <b>bold</b> and <i>italic</i> text</blockquote><blockquote>Quote 4 with nothing else</blockquote><blockquote>Quote 5 with a <code>code</code> section next to an <i>italic</i> section</blockquote><blockquote>Quote 6 with a <a href=\"www.google.com\">link</a></blockquote></div>",
        )
    
    def test_unordered_list(self):
        md = """
- List 1 Item 1
- List 1 Item 2
- List 1 Item 3

- List 2 Item 1
- List 2 Item 2 with **bold** text

- List 3 is only 1 item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List 1 Item 1</li><li>List 1 Item 2</li><li>List 1 Item 3</li></ul><ul><li>List 2 Item 1</li><li>List 2 Item 2 with <b>bold</b> text</li></ul><ul><li>List 3 is only 1 item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. List 1 Item 1
2. List 1 Item 2
3. List 1 Item 3

1. List 2 Item 1
2. List 2 Item 2 with **bold** text

1. List 3 is only 1 item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>List 1 Item 1</li><li>List 1 Item 2</li><li>List 1 Item 3</li></ol><ol><li>List 2 Item 1</li><li>List 2 Item 2 with <b>bold</b> text</li></ol><ol><li>List 3 is only 1 item</li></ol></div>",
        )
    
    def test_extract_title_1(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )

    def test_extract_title_2(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )

    def test_extract_title_2(self):
        md = "Hello"
        try:
            title = extract_title(md)
        except Exception as e:
            self.assertEqual(e.__repr__(), "Exception('h1 heading / title missing')")

    def test_extract_title_3(self):
        md = """
        Hello!

        There's no # way this is a title heading!
        
        ## Testing Testing

        # Title
        """
        title = extract_title(md)
        self.assertEqual(
            title,
            "Title"
        )

        
if __name__ == "__main__":
    unittest.main()