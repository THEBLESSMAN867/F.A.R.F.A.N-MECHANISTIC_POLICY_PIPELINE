#!/usr/bin/env python3
"""
Refactorización automática de imports relativos a absolutos.
Transforma todos los imports de farfan_core a farfan_pipeline.
"""
import ast
import os
import re
from pathlib import Path
from typing import List, Tuple

# Configuración
OLD_PACKAGE = "farfan_core"
NEW_PACKAGE = "farfan_pipeline"
SRC_DIR = Path("src/farfan_pipeline")

def fix_relative_imports(content: str, module_path: Path) -> str:
    """
    Convierte imports relativos a absolutos.
    """
    # Calculate module name from file path
    rel_path = module_path.relative_to(SRC_DIR)
    parts = list(rel_path.parts[:-1])  # Remove filename
    current_module = ".".join(parts) if parts else ""
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Match: from . import X or from .. import X
        match = re.match(r'^from (\.+)(\w+)? import (.+)$', stripped)
        if match:
            dots = match.group(1)
            module = match.group(2) or ''
            names = match.group(3)
            
            level = len(dots)
            
            # Calculate absolute module path
            if level == 1:
                # from .module import X -> from farfan_pipeline.current.module import X
                if module:
                    if current_module:
                        abs_module = f"{NEW_PACKAGE}.{current_module}.{module}"
                    else:
                        abs_module = f"{NEW_PACKAGE}.{module}"
                else:
                    # from . import X (same package)
                    if current_module:
                        abs_module = f"{NEW_PACKAGE}.{current_module}"
                    else:
                        abs_module = NEW_PACKAGE
            else:
                # Multiple levels up
                if current_module:
                    parts_list = current_module.split('.')
                    up_levels = level - 1
                    if up_levels >= len(parts_list):
                        parent_module = NEW_PACKAGE
                    else:
                        parent_module = f"{NEW_PACKAGE}.{'.'.join(parts_list[:-up_levels])}"
                else:
                    parent_module = NEW_PACKAGE
                
                if module:
                    abs_module = f"{parent_module}.{module}"
                else:
                    abs_module = parent_module
            
            # Replace line
            indent = line[:len(line) - len(line.lstrip())]
            new_line = f"{indent}from {abs_module} import {names}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_old_package_imports(content: str) -> str:
    """
    Reemplaza referencias al paquete antiguo con el nuevo.
    """
    # Replace farfan_core.X with farfan_pipeline.X
    content = re.sub(
        r'\bfarfan_core\.',
        f'{NEW_PACKAGE}.',
        content
    )
    
    # Replace "farfan_core" string references
    content = re.sub(
        r'["\']farfan_core["\']',
        f'"{NEW_PACKAGE}"',
        content
    )
    
    return content

def process_file(filepath: Path) -> Tuple[bool, str]:
    """Process a single Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        # Step 1: Fix relative imports
        modified = fix_relative_imports(original, filepath)
        
        # Step 2: Fix old package name
        modified = fix_old_package_imports(modified)
        
        if modified != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)
            return True, "modified"
        else:
            return False, "unchanged"
            
    except Exception as e:
        return False, f"error: {e}"

def main():
    """Main refactoring process."""
    print(f"Refactorizando imports en {SRC_DIR}")
    print("=" * 80)
    
    files_processed = 0
    files_modified = 0
    files_error = 0
    
    for root, dirs, files in os.walk(SRC_DIR):
        # Skip __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for filename in files:
            if filename.endswith('.py'):
                filepath = Path(root) / filename
                files_processed += 1
                
                modified, status = process_file(filepath)
                
                if modified:
                    files_modified += 1
                    print(f"✓ {filepath.relative_to(SRC_DIR)}")
                elif "error" in status:
                    files_error += 1
                    print(f"✗ {filepath.relative_to(SRC_DIR)}: {status}")
    
    print("=" * 80)
    print(f"Archivos procesados: {files_processed}")
    print(f"Archivos modificados: {files_modified}")
    print(f"Archivos con errores: {files_error}")
    print()
    
    if files_modified > 0:
        print("✓ Refactorización completada exitosamente")
        return 0
    else:
        print("⚠ No se realizaron cambios")
        return 1

if __name__ == "__main__":
    exit(main())
