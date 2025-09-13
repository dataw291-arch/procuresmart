import openai
import os

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY", "test-key")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT", "http://localhost")
openai.api_version = "2023-05-15"

def chat_with_ai(messages, deployment="gpt-35-turbo"):
    """Wrapper for OpenAI chat completion. Falls back if no key is set."""
    try:
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_DEPLOYMENT_NAME", deployment),
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Mock Response] {messages[-1]['content'][:200]}... (Error: {str(e)})"
