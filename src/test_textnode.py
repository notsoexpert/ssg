import unittest

from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node, LeafNode
from conversions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_ineq_text(self):
        node = TextNode("This is aNOTHER text NODE", TextType.ITALIC)
        node2 = TextNode("this is node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_ineq_type_link(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK, "http://boot.dev")
        self.assertNotEqual(node, node2)

    def test_ineq_type(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_text_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_text_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        
    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href":"https://www.google.com"})
    
    def test_bold_delim(self):
        node = TextNode("This is a **bold** statement!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node],'**', TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" statement!", TextType.NORMAL)])

    def test_italic_delim(self):
        node = TextNode("This is an _italic_ statement!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node],'_', TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is an ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" statement!", TextType.NORMAL)])
    
    def test_code_delim(self):
        node = TextNode("This is a `code` statement!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node],'`', TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is a ", TextType.NORMAL), TextNode("code", TextType.CODE), TextNode(" statement!", TextType.NORMAL)])
    
    def test_missing_delim(self):
        node = TextNode("This isn't a bold statement!", TextType.NORMAL)
        try:
            new_nodes = split_nodes_delimiter([node],'**', TextType.BOLD)
        except Exception as e:
            self.assertEqual(e.__repr__(), "Exception('delimiter not found in node')")

    def test_missing_closing_delim(self):
        node = TextNode("This isn't a **bold statement!", TextType.NORMAL)
        try:
            new_nodes = split_nodes_delimiter([node],'**', TextType.BOLD)
        except Exception as e:
            self.assertEqual(e.__repr__(), "Exception('closing delimiter not found in node')")

    def test_abnormal_type(self):
        node = TextNode("This is an entire bold statement!", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node],'**', TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is an entire bold statement!", TextType.BOLD)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


if __name__ == "__main__":
    unittest.main()