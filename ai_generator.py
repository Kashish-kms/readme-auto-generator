import openai
from prompt_templates import get_readme_prompt
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_readme(project_name, description, features, installation_steps, project_structure):
    """
    Generate README content using OpenAI API
    """
    try:
        # Create prompt using template
        prompt = get_readme_prompt(
            project_name=project_name,
            description=description,
            features=features,
            installation_steps=installation_steps,
            project_structure=project_structure
        )
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional technical writer specializing in creating clear, comprehensive README files."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract and return generated content
        readme_content = response.choices[0].message.content
        return readme_content
    
    except openai.error.AuthenticationError:
        raise Exception("Invalid OpenAI API key. Please check your .env file.")
    except openai.error.RateLimitError:
        raise Exception("Rate limit reached. Please try again later.")
    except Exception as e:
        raise Exception(f"Error generating README: {str(e)}")

def generate_readme_section(section_type, content):
    """
    Generate specific README sections
    """
    try:
        prompt = f"""
        Generate a professional {section_type} section for a README file.
        Content: {content}
        
        Format it nicely with proper markdown syntax.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"Error generating section: {str(e)}")