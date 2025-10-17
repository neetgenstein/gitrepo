import requests
import json

# Google AI Studio API endpoint for Gemini 1.5 Pro
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# Your API key for Google AI Studio
API_KEY = 'AIzaSyC8dnV15iSJJ7HlGERiQORaCiXVV5GGfoI'  # Consider using environment variables in production

def get_gemini_response(prompt):
    """
    Send a prompt to the Gemini API and return the response.
    
    Args:
        prompt (str): The user's query or prompt
        
    Returns:
        str: The generated response from Gemini
    """
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Prepare the request payload
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
        # Make the API request
        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
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

def main():
    print("Gemini AI Assistant (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit command
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
            
        # Get and display the response
        response = get_gemini_response(user_input)
        print("\nGemini:", response)

if __name__ == "__main__":
    main()