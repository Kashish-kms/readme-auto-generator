import os
from datetime import datetime

def export_to_markdown(content, filename, output_dir):
    """
    Export README content to markdown file
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Add .md extension if not present
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        # Create filepath
        filepath = os.path.join(output_dir, filename)
        
        # Add timestamp comment at the bottom
        footer = f"\n\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using README Auto-Generator*"
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            f.write(footer)
        
        return filepath
    
    except Exception as e:
        raise Exception(f"Error exporting to markdown: {str(e)}")

def validate_markdown(content):
    """
    Validate markdown content
    """
    required_elements = ['#', '-', '*']
    
    has_headers = any(line.startswith('#') for line in content.split('\n'))
    
    return has_headers

def format_markdown(content):
    """
    Format and clean markdown content
    """
    lines = content.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Remove extra whitespace
        line = line.rstrip()
        formatted_lines.append(line)
    
    # Remove extra blank lines (more than 2 consecutive)
    result = []
    blank_count = 0
    
    for line in formatted_lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    
    return '\n'.join(result)