import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


    
if __name__ == "__main__":
    unittest.main()