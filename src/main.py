import os
import shutil
import sys

from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode
from conversions import markdown_to_html_node, extract_title

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    preprocess("./static", "./docs")
    generate_pages_recursive(basepath, "./content/", "./template.html", "./docs/")

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    # First, get a list of files and directories in this directory
    dir_contents = os.listdir(dir_path_content)

    # Loop through the list, calling this function on each directory
    # and adding generating each page in the destination
    for content in dir_contents:
        if os.path.isfile(dir_path_content+content):
            # Ignore non-markdown files
            if not content[-3:] == '.md':
                continue
            generate_page(basepath, dir_path_content+content, template_path, dest_dir_path+content.replace('.md', '.html'))
        else:
            generate_pages_recursive(basepath, dir_path_content+content+"/", template_path, dest_dir_path+content+'/')

    

def generate_page(basepath, from_path, template_path, dest_path):
    md_file = open(from_path)
    md = md_file.read()
    md_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(md)
    html_string = html_node.to_html()

    title = extract_title(md)

    dest = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    dest_file = open(dest_path, "w")
    dest_file.write(dest)
    dest_file.close()


def preprocess(static_path, output_path):
    if os.path.exists(output_path):
        shutil.rmtree(output_path, False)
    shutil.copytree(static_path,output_path)

main()