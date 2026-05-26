def get_readme_prompt(project_name, description, features, installation_steps, project_structure):
    """
    Create a comprehensive prompt for README generation
    """
    
    features_text = "\n".join([f"- {feature}" for feature in features]) if features else "- No features provided"
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(installation_steps)]) if installation_steps else "1. No installation steps provided"
    
    prompt = f"""
    Generate a professional and comprehensive README.md file for the following project:
    
    **Project Name:** {project_name}
    
    **Description:** {description}
    
    **Features:**
    {features_text}
    
    **Installation Steps:**
    {steps_text}
    
    **Project Structure:**
    {project_structure}
    
    Please generate a complete README with the following sections:
    1. Project Title and Badge
    2. Description (2-3 lines)
    3. Features (bullet points)
    4. Installation Instructions (step-by-step)
    5. Usage/Getting Started
    6. Project Structure
    7. Technologies Used
    8. Contributing Guidelines
    9. License
    10. Contact/Support
    
    Format it with proper markdown syntax including:
    - Headers (# ## ###)
    - Bold text for emphasis
    - Code blocks for commands and code
    - Lists and bullet points
    - Links where appropriate
    
    Make it professional, clear, and easy to follow.
    """
    
    return prompt

def get_section_prompt(section_name, content):
    """
    Get prompt for specific section generation
    """
    prompts = {
        'installation': f"""
            Create a clear and concise Installation section for a README.
            Content: {content}
            Include:
            - Prerequisites
            - Step-by-step installation
            - Verification steps
        """,
        'usage': f"""
            Create a Usage/Getting Started section for a README.
            Content: {content}
            Include:
            - Basic examples
            - Common use cases
            - Tips and tricks
        """,
        'features': f"""
            Create a Features section for a README.
            Content: {content}
            Format as bullet points with descriptions.
        """,
        'contributing': """
            Create a professional Contributing Guidelines section for a README.
            Include:
            - How to contribute
            - Code style guidelines
            - Pull request process
            - Reporting bugs
        """
    }
    
    return prompts.get(section_name, f"Generate a {section_name} section: {content}")