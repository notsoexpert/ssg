import re

from htmlnode import BlockType
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        delimiter_start_location = node.text.find(delimiter)
        if delimiter_start_location == -1:
            new_nodes.append(node)
            continue
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

def strip_lines(blocks, index):
    block_lines = blocks[index].splitlines()
    i = 0
    while i < len(block_lines):
        block_lines[i] = block_lines[i].strip()
        if len(block_lines[i]) == 0:
            block_lines.pop(i)
            continue
        i += 1
    blocks[index] = '\n'.join(block_lines)

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
    print("***************************")
    print(f"Block length: {len(md)}\nBlock:\n{md}")
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