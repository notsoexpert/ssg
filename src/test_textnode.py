import unittest

from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node, LeafNode
from conversions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_empty_split_images(self):
        node = TextNode(
            "This is text with no images!",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with no images!",
                    TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_empty_split_links(self):
        node = TextNode(
            "This is text with no links!",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with no links!",
                    TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_1(self):
        text = "This is just a normal text node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just a normal text node!",
                    TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_2(self):
        text = "This is just a **bold** text node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just a ",
                    TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_2(self):
        text = "This is just an _italic_ text node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just an ",
                    TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_3(self):
        text = "This is just a `code` text node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just a ",
                    TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" text node!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_4(self):
        text = "This is just an ![image](https://www.shutterstock.com/image-photo/happy-old-man-135438581) image node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just an ",
                    TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://www.shutterstock.com/image-photo/happy-old-man-135438581"),
                TextNode(" image node!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_5(self):
        text = "This is just a [google](https://www.google.com) link node!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is just a ",
                    TextType.NORMAL),
                TextNode("google", TextType.LINK, "https://www.google.com"),
                TextNode(" link node!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_6(self):
        text = "This one has **bold** and _italic_ text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has ",
                    TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text!", TextType.NORMAL)
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes_7(self):
        text = "This one has `code` and **bold** text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has ",
                    TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text!", TextType.NORMAL)
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes_8(self):
        text = "This one has _italic_, **bold**, and `code` text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has ",
                    TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(", and ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" text!", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_9(self):
        text = "This one has ![image](https://i.imgur.com/fJRm4Vk.jpeg) an image and a link to [youtube](https://www.youtube.com)!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has ",
                    TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" an image and a link to ", TextType.NORMAL),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode("!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_10(self):
        text = "This one has ![image](https://i.imgur.com/fJRm4Vk.jpeg) an image, **bold**, and `code` text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has ",
                    TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" an image, ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(", and ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" text!", TextType.NORMAL)
            ],
            new_nodes,
        )

    def test_text_to_textnodes_11(self):
        text = "This one has it all! `Code`, ![images...](https://i.imgur.com/fJRm4Vk.jpeg)images, **bold**, [links](https://www.youtube.com), and _italic_ text!"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This one has it all! ",
                    TextType.NORMAL),
                TextNode("Code", TextType.CODE),
                TextNode(", ", TextType.NORMAL),
                TextNode("images...", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("images, ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.NORMAL),
                TextNode("links", TextType.LINK, "https://www.youtube.com"),
                TextNode(", and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text!", TextType.NORMAL)
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()