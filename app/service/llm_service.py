import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.service.memory_service import get_guest_history, append_guest_dialogue
load_dotenv()

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    raise ValueError("Api key not found")

client = AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

async def llmService(guest_id:str ,user_prompt:str):
    dialogue_history = list(get_guest_history(guest_id))
    
    current_history = dialogue_history + [{'role':"user", "content":user_prompt}]
    full_response = ""
    stream = await client.responses.create(
        model="gpt-4o-mini",
        input=current_history,
        instructions="You are the witty, helpful assistant inside the Chap Chat application.",
        temperature=1.5,
        stream=True   
    )
    async for event in stream:
        if event.type == "response.output_text.delta":
            full_response +=event.delta
            yield event.delta
    if full_response:
        append_guest_dialogue(guest_id,user_prompt,full_response)
    