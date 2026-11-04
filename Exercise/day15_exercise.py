import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API")

def proposal_checker():
    system_prompt = """You are a Proposal Feedback Tool.
    Your task is to provide feedback on proposals submitted by users.
    rules:
    - Provide constructive feedback on the proposal.
    - Highlight strengths and areas for improvement.
    - Use a professional and encouraging tone.
    - Highlight one weakness and one strength of the proposal.
    - Provide a summary of the feedback in 2-3 sentences.
    - Provide a rewritten opening sentence. 
    """
    Question = input("Please enter your proposal for feedback: ")

    if Question is None or Question.strip() == "":
        print("No proposal provided. Please enter a valid proposal.")
        return 
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": Question}
            ],
            max_tokens=512
        )
        feedback = response.choices[0].message.content
        print("Feedback on your proposal:")
        print(feedback)
    except openai.APIConnectionError:
        print("No internet connection. Check your connection and try again.")
    except openai.AuthenticationError:
        print("API key is wrong or expired. Check your .env file.")
    except openai.RateLimitError:
        print("Too many requests. Wait 60 seconds and try again.")


if __name__ == "__main__":
    proposal_checker()