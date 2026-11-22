import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.service.memory_service import get_guest_history, append_guest_dialogue
from app.tools.tool_schema import TOOL_EXECUTION, TOOL_SCHEMA 
import json
load_dotenv()

api_key = os.getenv("LLM_API_KEY")

if not api_key:
    raise ValueError("Api key not found")

client = AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")


async def LLMResponseService(input:list):
    messages = list(input)
    full_response = ""
    for _ in range(3):
        tool_call = []
        stream = await client.responses.create(
                model="gpt-4o-mini",
                input=messages,
                instructions="You are the witty, helpful assistant inside the Chap Chat application. Use your available tools whenever the user asks for calculations or the current time.",
                tools= TOOL_SCHEMA,
                temperature=1.5,
                stream=True   
        )
        
        async for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta
                elif event.type == "response.output_item.done":
                    if getattr(event.item, "type", None) == "function_call":
                        tool_call.append(event.item)
        if not tool_call:
            break
        for call in tool_call:
            func_name = call.name
            raw_args = json.loads(call.arguments or "{}")
            
            messages.append(
                {
                    "type": "function_call",
                    "call_id": call.call_id,
                    "name": func_name,
                    "arguments": call.arguments,
                }
            )
            executor = TOOL_EXECUTION.get(func_name)
            if executor:
                try:
                    tool_output = await executor(**raw_args)
                except Exception as e:
                    tool_output = json.dumps({"error": f"Tool execution failed :{str(e)}"})
            else:
                tool_output = json.dumps({"error":f"Unknown tools: {func_name}"})
            messages.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": str(tool_output),
                }
            )

async def guestLLMService(guest_id:str ,guest_prompt:str):
    dialogue_history = list(get_guest_history(guest_id))
    
    current_history = dialogue_history + [{'role':"user", "content":guest_prompt}]
    full_response = ""
    try:
        async for chunk in LLMResponseService(current_history):
            full_response +=chunk
            yield chunk
    finally:
        if full_response:
            append_guest_dialogue(guest_id,guest_prompt,full_response)