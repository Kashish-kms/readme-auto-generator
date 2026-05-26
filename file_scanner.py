import os
import json
from pathlib import Path

def scan_project(project_path, max_depth=3, current_depth=0, exclude_dirs=None):
    """
    Scan project directory and return structure
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.env'}
    
    if current_depth > max_depth:
        return None
    
    try:
        structure = {}
        
        if os.path.isfile(project_path):
            return {
                'name': os.path.basename(project_path),
                'type': 'file',
                'size': os.path.getsize(project_path)
            }
        
        if not os.path.isdir(project_path):
            return None
        
        items = []
        
        try:
            entries = os.listdir(project_path)
        except PermissionError:
            return None
        
        for entry in sorted(entries):
            if entry.startswith('.') and entry not in {'.env', '.gitignore', '.github'}:
                continue
            
            if entry in exclude_dirs:
                continue
            
            full_path = os.path.join(project_path, entry)
            
            if os.path.isdir(full_path):
                sub_structure = scan_project(full_path, max_depth, current_depth + 1, exclude_dirs)
                if sub_structure:
                    items.append({
                        'name': entry,
                        'type': 'directory',
                        'children': sub_structure.get('children', [])
                    })
            else:
                items.append({
                    'name': entry,
                    'type': 'file',
                    'size': os.path.getsize(full_path)
                })
        
        structure['name'] = os.path.basename(project_path)
        structure['type'] = 'directory'
        structure['children'] = items
        
        return structure
    
    except Exception as e:
        return {'error': str(e)}

def get_project_structure_text(structure, indent=0):
    """
    Convert project structure to readable text format
    """
    text = ""
    indent_str = "  " * indent
    
    if isinstance(structure, dict):
        if structure.get('type') == 'directory':
            text += f"{indent_str}📁 {structure.get('name', 'root')}/\n"
            for child in structure.get('children', []):
                text += get_project_structure_text(child, indent + 1)
        elif structure.get('type') == 'file':
            icon = get_file_icon(structure.get('name', ''))
            text += f"{indent_str}{icon} {structure.get('name')}\n"
    
    return text

def get_file_icon(filename):
    """
    Get icon/emoji for file type
    """
    icons = {
        '.py': '🐍',
        '.js': '📜',
        '.html': '🌐',
        '.css': '🎨',
        '.json': '📋',
        '.md': '📝',
        '.txt': '📄',
        '.env': '🔐',
        '.yml': '⚙️',
        '.yaml': '⚙️',
        '.sh': '🔧'
    }
    
    _, ext = os.path.splitext(filename)
    return icons.get(ext, '📄')

def extract_file_types(structure):
    """
    Extract all file types in project
    """
    types = set()
    
    def traverse(item):
        if isinstance(item, dict):
            if item.get('type') == 'file':
                _, ext = os.path.splitext(item.get('name', ''))
                if ext:
                    types.add(ext)
            for child in item.get('children', []):
                traverse(child)
    
    traverse(structure)
    return sorted(list(types))