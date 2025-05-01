import re

from htmlnode import BlockType, ParentNode, LeafNode, HTMLNode
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
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
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        start_index = 0
        for match in matches:
            text_up_to = node.text[start_index:node.text.find(match[0])-2]
            if len(text_up_to) > 0:
                new_nodes.append(TextNode(text_up_to, TextType.NORMAL))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            start_index = node.text.find(match[1])+len(match[1])+1
            text_after = node.text[start_index:]
            if len(text_after) > 0:
                other_matches = extract_markdown_images(text_after)
                if len(other_matches) > 0:
                    continue
                new_nodes.append(TextNode(text_after, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        start_index = 0
        for match in matches:
            text_up_to = node.text[start_index:node.text.find(match[0])-1]
            if len(text_up_to) > 0:
                new_nodes.append(TextNode(text_up_to, TextType.NORMAL))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            start_index = node.text.find(match[1])+len(match[1])+1
            text_after = node.text[start_index:]
            if len(text_after) > 0:
                other_matches = extract_markdown_links(text_after)
                if len(other_matches) > 0:
                    continue
                new_nodes.append(TextNode(text_after, TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("invalid text type")

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    index = 0
    while index < len(blocks):
        blocks[index] = blocks[index].strip()
        if len(blocks[index]) == 0:
            blocks.pop(index)
            continue
        index += 1

    return blocks

def block_to_block_type(md):
    if len(md) == 0:
        raise Exception("empty block has no block type")
    
    match md[0]:
        case '#':
            total_hash = 1
            for i in range(1, len(md)):
                if md[i] == '#':
                    total_hash += 1
                    if total_hash > 6:
                        return BlockType.PARAGRAPH
                    continue
                elif md[i] == ' ':
                    return BlockType.HEADING
                return BlockType.PARAGRAPH
        case '`':
            if len(md) < 6:
                return BlockType.PARAGRAPH
            if md[:3] == '```' and md[-3:] == '```':
                return BlockType.CODE
            return BlockType.PARAGRAPH
        case '>':
            lines = md.splitlines()
            for line in lines:
                if line[0] != '>':
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case '-':
            lines = md.splitlines()
            for line in lines:
                if line[0:2] != '- ':
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case '1':
            lines = md.splitlines()
            tally = 1
            for line in lines:
                if line[0:3] != f"{tally}. ":
                    return BlockType.PARAGRAPH
                tally += 1
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
        
def count_heading(block):
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            return count
        
def block_to_html_node(block, block_type):
    if block_type == BlockType.CODE:
        return ParentNode("pre", [text_node_to_html_node(TextNode(block.strip('`').lstrip('\n'), TextType.CODE))])
    
    match block_type:
        case BlockType.PARAGRAPH:
            block = block.replace('\n', ' ')
            textnodes = text_to_textnodes(block)
            children = list(map(text_node_to_html_node, textnodes))
            return ParentNode("p", children)
        case BlockType.HEADING:
            heading_count = count_heading(block)
            block = block.replace('\n', ' ').lstrip('# ')
            textnodes = text_to_textnodes(block)
            children = list(map(text_node_to_html_node, textnodes))
            return ParentNode(f"h{heading_count}", children)
        case BlockType.QUOTE:
            lines = block.splitlines()
            for i in range(0, len(lines)):
                lines[i] = lines[i].lstrip("> ")
            block = '\n'.join(lines)
            textnodes = text_to_textnodes(block)
            children = list(map(text_node_to_html_node, textnodes))
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            children = []
            lines = block.splitlines()
            for line in lines:
                line = line.lstrip('- ')
                textnodes = text_to_textnodes(line)
                nested_children = list(map(text_node_to_html_node, textnodes))
                children.append(ParentNode('li', nested_children))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = []
            lines = block.splitlines()
            for line in lines:
                line = line.lstrip('0123456789. ')
                textnodes = text_to_textnodes(line)
                nested_children = list(map(text_node_to_html_node, textnodes))
                children.append(ParentNode('li', nested_children))
            return ParentNode("ol", children)
        case _:
            raise Exception("invalid block type")
    
        
def markdown_to_html_node(document):
    blocks = markdown_to_blocks(document)
    new_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        new_nodes.append(block_to_html_node(block, block_type))
    parent = ParentNode("div", new_nodes)
    return parent
    
def extract_title(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            heading_count = count_heading(block)
            if heading_count == 1:
                return block[2:]
    raise Exception("h1 heading / title missing")
    