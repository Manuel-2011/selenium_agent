import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

CONTEXT_MESSAGES_INIT = [
    {
        "role": "system",
        "content": "You are an AI that generates code based on a description of what the code should do. You should never give explanations in your responses. You always give the responses in plain text",
    },
]

CREATION_MESSAGE = {
    "role": "user",
    "content": """Create a function that {action} using selenium.
    - The parameter should be the driver. 
    - Don't include any explanations in your responses. Dont include imports.
    - The return should be an html""",
}

ERROR_MESSAGE = {
    "role": "user",
    "content": """There was the following error: {action}. Try again. don't include any explanations in your responses. Dont include imports.""",
}

RESPONSE_MESSAGE = {
    "role": "assistant",
    "content": """{response}""",
}


def replace_action_in_message(message, action):
    new_message = message.copy()
    new_message["content"] = new_message["content"].format(action=action)
    return new_message


def replace_response_in_message(response):
    new_response_message = RESPONSE_MESSAGE.copy()
    new_response_message["content"] = new_response_message["content"].format(
        response=response
    )
    return new_response_message


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_code_from_open_ai(action, messages, is_error=False):
    context_messages = messages if messages else CONTEXT_MESSAGES_INIT
    new_message = ERROR_MESSAGE if is_error else CREATION_MESSAGE
    new_message = replace_action_in_message(new_message, action)
    context_messages.append(new_message)
    response = get_completion_from_messages(context_messages)
    context_messages.append(replace_response_in_message(response))
    return context_messages, response
