import requests
import json
import os
import re

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# Your API key for Google AI Studio
API_KEY = 'AIzaSyBl3ta-PemziIa1DdlRjrvA2rGsQDMVkfQ'  # Consider using environment variables in production

class TensorFunc:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key else API_KEY
        self.api_url = GEMINI_API_URL

    def _process_file_references(self, user_input):
        """
        Parses @<filepath> tags or @filepath, reads the files, and appends content to the prompt.
        """
        # Match @ followed by non-whitespace characters
        pattern = r"@(\S+)"
        matches = re.findall(pattern, user_input)
        
        if not matches:
            return user_input

        # Remove the tags from the input
        clean_input = re.sub(pattern, "", user_input).strip()
        
        appended_content = []
        
        for file_path in matches:
            try:
                # Remove < and > if the user used the @<file> syntax
                clean_path = file_path.strip("<>")
                
                if os.path.exists(clean_path) and os.path.isfile(clean_path):
                    with open(clean_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        appended_content.append(f"\n{clean_path}:\n{content}")
                else:
                    print(f"\nWarning: File not found: {clean_path}")
            except Exception as e:
                print(f"\nError reading file {file_path}: {e}")
                
        if appended_content:
            # If clean_input is empty, just return the content
            if not clean_input:
                return "\n".join(appended_content)
            return f"{clean_input}\n" + "\n".join(appended_content)
        
        return clean_input

    def _get_gemini_response(self, prompt):
        """
        Send a prompt to the Gemini API and return the response.
        """
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 50000,
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=data
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Error: No response generated. Please try again."
                
        except requests.exceptions.RequestException as e:
            return f"Error making API request: {str(e)}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return f"Error processing API response: {str(e)}"

    def perform(self, query, output_file=None):
        """
        Process the query (including file references), get response from Gemini,
        and optionally save to a file.
        
        Args:
            query (str): The prompt/query.
            output_file (str, optional): Path to save the output.
            
        Returns:
            str: The response from Gemini.
        """
        prompt = self._process_file_references(query)
        response = self._get_gemini_response(prompt)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                print(f"Output saved to {output_file}")
            except Exception as e:
                print(f"Error saving to file {output_file}: {e}")
        else:
            print(response)
            
        return response

def list_files():
    """Lists all local files in the current directory, excluding common ignore dirs."""
    print("\nLocal files:")
    for root, dirs, files in os.walk("."):
        # Skip common ignore directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'env', 'venv', 'node_modules', '.ipynb_checkpoints']]
        
        for file in files:
            # Get relative path
            rel_path = os.path.relpath(os.path.join(root, file), ".")
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            print(f"- {rel_path}")

def main():
    agent = TensorFunc()
    
    print("Tensor Input/Output (type 'exit' to quit)")
    print("Commands:")
    print("  listFiles() - List all local files")
    print("  @<filename> - Include file content in your query")
    print("-" * 40)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
            
        # Check for exit command
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
            
        # Check for listFiles() command
        if user_input.strip() == "listFiles()":
            list_files()
            continue
            
        # Process file references
        # We use the internal method here to show the prompt confirmation flow
        # which is specific to the interactive CLI, not the generic perform() method
        prompt = agent._process_file_references(user_input)
        
        proceed = input("\nProceed? (y/n): ")
        
        if proceed.lower() in ['y', 'yes']:
            response = agent._get_gemini_response(prompt)
            print("Output:", response)
        else:
            print("\nSkipping.")

if __name__ == "__main__":
    main()