import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        delimiter_start_location = node.text.find(delimiter)
        if delimiter_start_location == -1:
            raise Exception("delimiter not found in node")
        delimiter_end_location = node.text.find(delimiter, delimiter_start_location+len(delimiter))
        if delimiter_end_location == -1:
            raise Exception("closing delimiter not found in node")
        
        beginning_node = TextNode(node.text[:delimiter_start_location], TextType.NORMAL)
        middle_node = TextNode(node.text[delimiter_start_location+len(delimiter):delimiter_end_location], text_type)
        end_node = TextNode(node.text[delimiter_end_location+len(delimiter):], TextType.NORMAL)
        new_nodes.append(beginning_node)
        new_nodes.append(middle_node)
        new_nodes.append(end_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        # TODO
    return new_nodes