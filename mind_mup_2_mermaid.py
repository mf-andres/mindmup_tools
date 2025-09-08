import json
import logging
import os
import sys


def main(folder_path):
    """
    Main function to process all JSON files in a folder and generate Mermaid diagrams.

    Args:
        folder_path (str): The path to the folder containing JSON files.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: The provided path '{folder_path}' is not a valid directory.")
        return
    
    # Process each file in the directory
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        print(file_path)
        try:
            with open(file_path, "r") as file_:
                mindmup = json.load(file_)
        except json.JSONDecodeError:
            print(f"could not decode {file_name}")
            continue

        mermaid_output = generate_mermaid_from_json(mindmup)
            
        if not mermaid_output:
            continue

        output_file_name = f"{os.path.splitext(file_name)[0]}_mermaid.md"
        output_path = os.path.join(folder_path, output_file_name)
            
        with open(output_path, "w") as out_file:
            out_file.write(mermaid_output)
        print(f"Generated Mermaid diagram for '{file_name}' and saved to '{output_path}'.")

def generate_mermaid_from_json(mindmup):
    mermaid_code = Text()
    mermaid_code += "```"
    mermaid_code += "flowchart LR"
    
    # Extract the root nodes
    root_nodes = mindmup['ideas']

    # Use a stack to make a Deep First Search of the tree
    stack = []
    for root_node in root_nodes.values():
        stack.append(root_node)

    # Iterate the stack to make a Deep First Search of the tree
    while stack:
        parent_node = stack.pop()
        if 'ideas' not in parent_node:
            continue
        parent_id = parent_node['id']
        parent_text = parent_node['title']
        children_nodes = parent_node['ideas']
        for children_node in children_nodes.values():
            children_id = children_node['id']
            children_text = children_node['title']
            mermaid_code += f"{parent_id}[{parent_text}] --> {children_id}[{children_text}]"
            stack.append(children_node)

    mermaid_code += "```"
    return mermaid_code.compile_text()

class Text:
    def __init__(self):
        self._lines = []

    def add_line(self, line: str):
        self._lines.append(line)

    def compile_text(self) -> str:
        return "\n".join(self._lines)

    def __iadd__(self, other):
        """Overloads the += operator to add a new line."""
        if isinstance(other, str):
            self.add_line(other)
            return self
        else:
            raise TypeError(f"unsupported operand type(s) for +=: 'Text' and '{type(other).__name__}'")

    def __str__(self) -> str:
        return self.get_text()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_script_name.py <folder_path>")
    else:
        main(sys.argv[1])