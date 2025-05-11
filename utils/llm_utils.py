import os
from openai import OpenAI
import yaml

def call_llm(prompt):
    """Call an LLM with the given prompt."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
        
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def extract_topics_from_llm_response(response):
    """Extract structured topic data from LLM YAML response."""
    try:
        # Extract YAML content if wrapped in code blocks
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        elif "```" in response:
            yaml_content = response.split("```")[1].split("```")[0].strip()
        else:
            yaml_content = response.strip()
        
        # Parse YAML
        data = yaml.safe_load(yaml_content)
        
        # Validate expected structure
        if not isinstance(data, dict) or "topics" not in data:
            raise ValueError("Response does not contain expected 'topics' key")
            
        return data["topics"]
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        print(f"Raw response: {response}")
        return []

if __name__ == "__main__":
    # Test the LLM call with a simple prompt
    test_prompt = "In a few words, what is the meaning of life?"
    response = call_llm(test_prompt)
    print(f"LLM Response: {response}") 