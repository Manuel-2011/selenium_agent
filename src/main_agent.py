import re
import pprint
import requests
from openai_utils import get_code_from_open_ai
from html_cleaner import get_cleaned_html
from planner_agent.planner_agent import get_plan
import queue
import os


def send_message(message):
    api_url = "http://127.0.0.1:8000/"
    json_payload = {"code": message}
    response = requests.post(api_url, json=json_payload)
    # Check the response status code
    if response.status_code == 200:
        print("Request successful. Response:")
        response_data = response.json()
        print(response_data)
        return response_data
    else:
        print(f"Request failed with status code: {response.status_code}")


def main():
    is_test_mode = os.getenv("TEST_MODE", False)

    history_messages = []

    if is_test_mode:
        goal = "Search a blue car"
    else:
        goal = input("Enter a goal for the web browser agent or exit to quit: ")

    if goal.lower() == "exit":
        return
    
    actions = queue.Queue()
    for action in get_plan(goal, test_mode=is_test_mode):
        actions.put(action)

    while True:
        action = actions.get()
        is_error = input("Is this an error? (y/n): ")
        is_error = is_error.lower() == "y"
        history_messages, message = get_code_from_open_ai(
            action, history_messages, is_error
        )
        pprint.pprint(history_messages)
        response = send_message(message)


if __name__ == "__main__":
    main()
