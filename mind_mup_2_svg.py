import json
import logging
import os
import sys

import pydot


def main(folder_path):
    """
    Main function to process all JSON files in a folder and generate Mermaid diagrams.

    Args:
        folder_path (str): The path to the folder containing JSON files.
    """
    if not os.path.isdir(folder_path):
        logging.info(f"Error: The provided path '{folder_path}' is not a valid directory.")
        return
    
    # Process each file in the directory
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        logging.info(f"processing: {file_path}")

        try:
            with open(file_path, "r") as file_:
                mindmup = json.load(file_)
        except json.JSONDecodeError:
            logging.info(f"could not decode {file_name}")
            continue

        try:
            graph = generate_graph(mindmup)
            output_file_name = f"{os.path.splitext(file_name)[0]}_mermaid.svg"
            output_path = os.path.join(folder_path, output_file_name)
            graph.write_svg(output_path)
        except Exception:
            logging.exception(f"could not process {file_name}")
            continue
            
            

def generate_graph(mindmup):
    graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="yellow")

    # Use a stack to make a Deep First Search of the tree
    stack = []

    # Add the root nodes
    root_nodes = mindmup['ideas']
    for root_node in root_nodes.values():
        root_id = root_node['id']
        root_text = root_node['title']
        graph.add_node(pydot.Node(root_id, label=root_text))
        stack.append(root_node)

    # Iterate the stack to make a Deep First Search of the tree
    while stack:
        parent_node = stack.pop()
        parent_doesnt_have_children = 'ideas' not in parent_node
        if parent_doesnt_have_children:
            continue
        parent_id = parent_node['id']
        children_nodes = parent_node['ideas']
        for children_node in children_nodes.values():
            children_id = children_node['id']
            children_text = children_node['title']
            graph.add_node(pydot.Node(children_id, label=children_text))
            graph.add_edge(pydot.Edge(parent_id, children_id))
            stack.append(children_node)
    return graph

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.info("Usage: python your_script_name.py <folder_path>")
    else:
        main(sys.argv[1])