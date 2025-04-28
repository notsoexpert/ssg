import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions import markdown_to_blocks

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



    
if __name__ == "__main__":
    unittest.main()