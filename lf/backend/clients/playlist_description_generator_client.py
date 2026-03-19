import openai
from openai import AzureOpenAI
import os


class PlaylistDescriptionGeneratorClient:
    def __init__(self):
        base_url = os.getenv("AZURE_OPENAI_BASE_URL")
        self.client = AzureOpenAI(
            api_version="2025-01-01-preview",
            azure_endpoint=base_url,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

    def generate_description(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-5",  
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=10000,
            )

            content = response.choices[0].message.content
            if content is None:
                print("DEBUG: Content is None")
                return None
            description = content.strip()
            return description

        except openai.APIConnectionError as e:
            print("ERROR: The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            return None
        except openai.RateLimitError as e:
            print("ERROR: A 429 status code was received; we should back off a bit.")
            return None
        except openai.APIStatusError as e:
            print("ERROR: Another non-200-range status code was received")
            print(f"Status code: {e.status_code}")
            print(f"Message: {e.message}")
            return None
        except Exception as e:
            print(f"ERROR: Unexpected exception occurred: {type(e).__name__}: {str(e)}")
            return None