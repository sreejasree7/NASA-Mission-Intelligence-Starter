from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    # TODO: Set context in messages
    # TODO: Add chat history
    # TODO: Creaet OpenAI Client
    # TODO: Send request to OpenAI
    # TODO: Return response
    os.environ["OPENAI_API_KEY"] = 'voc-24227570112667751079586a294ed553e4b8.93172022'
     
    openai_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
            base_url="https://openai.vocareum.com/v1",
            api_key=api_key
        )
    system_prompt = f"""
You are an expert NASA mission assistant.

Answer the user's questions using ONLY the supplied context whenever possible.

Instructions:
- Base your answer on the retrieved NASA documents.
- If the answer is not contained in the context, clearly state that the information
  is not available in the retrieved documents.
- Do not invent facts.
- Be clear, concise and technically accurate.

Retrieved Context:
{context}
"""

    # Initialize messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add conversation history
    if conversation_history:
        messages.extend(conversation_history)

    # Add current user question
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    try:
        # Send request
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=800
        )

        # Return assistant response
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"
