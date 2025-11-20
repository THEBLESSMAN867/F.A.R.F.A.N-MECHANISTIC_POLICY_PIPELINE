
import ast
import sys
import os

def get_imports_from_file(file_path):
    """
    Parses a Python file and returns a set of imported module names.
    """
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read file {file_path}: {e}", file=sys.stderr)
        return imports

    try:
        tree = ast.parse(content, filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Get the top-level module (e.g., 'a' in 'import a.b.c')
                    top_level_module = alias.name.split('.')[0]
                    imports.add(top_level_module)
            elif isinstance(node, ast.ImportFrom):
                # For 'from . import b' or 'from ..a import b', level > 0
                # We are interested in external packages, so we check level == 0
                if node.level == 0 and node.module:
                    # Get the top-level module (e.g., 'a' in 'from a.b import c')
                    top_level_module = node.module.split('.')[0]
                    imports.add(top_level_module)
    except (SyntaxError, ValueError) as e:
        print(f"Warning: Could not parse file {file_path}: {e}", file=sys.stderr)

    return imports

def main():
    """
    Main function to process a list of files from stdin
    and print all unique top-level imports.
    """
    all_imports = set()
    for file_path in sys.stdin:
        file_path = file_path.strip()
        if os.path.isfile(file_path):
            file_imports = get_imports_from_file(file_path)
            all_imports.update(file_imports)

    for imp in sorted(list(all_imports)):
        print(imp)

if __name__ == "__main__":
    main()
