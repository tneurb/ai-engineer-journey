import os
import voyageai
from dotenv import load_dotenv
import anthropic



load_dotenv()
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "calculator",
        "description": "Perform basic math calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression, e.g. '5 * 3'"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "word_counter",
        "description": "Count the number of words in a piece of text",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to count words in"}
            },
            "required": ["text"]
        }
    }
]


def calculator(expression):
    return str(eval(expression))

def word_counter(text):
    return str(len(text.split()))

question = "What is 15 times 8, and how many words are in the sentence 'The quick brown fox jumps over the lazy dog'?"

messages = [{"role": "user", "content": question}]

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

messages = [{"role": "user", "content": question}]

for step in range(5):  # hard limit — never loop forever
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    if message.stop_reason == "tool_use":
        # find the tool_use block in message.content
        tool_use_block = next(b for b in message.content if b.type == "tool_use")

        print(f"Claude wants to use: {tool_use_block.name} with input {tool_use_block.input}")

        # run the ACTUAL tool
        if tool_use_block.name == "calculator":
            result = calculator(tool_use_block.input["expression"])
        elif tool_use_block.name == "word_counter":
            result = word_counter(tool_use_block.input["text"])

        # add Claude's tool request AND your tool result to the conversation
        messages.append({"role": "assistant", "content": message.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": result
            }]
        })
        # loop continues — Claude sees the result and decides what to do next

    else:
        # Claude has a final text answer — no more tools needed
        print("Final answer:", message.content[0].text)
        break