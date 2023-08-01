import re
import pprint
import requests
from openai_utils import get_code_from_open_ai
from html_cleaner import get_cleaned_html
from planner_agent.planner_agent import get_plan
from verification_agent.verification_agent import evaluate_task
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
        # print(response_data)
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

    is_task_accomplished = True
    error_message = None
    feedback = None
    while True:
        if is_task_accomplished:
            if actions.empty():
                break
            action = actions.get()

        is_error = input("Is this an error? (y/n): ")
        is_error = is_error.lower() == "y"
        history_messages, message = get_code_from_open_ai(
            action, history_messages, feedback
        )
        pprint.pprint(history_messages)
        response = send_message(message)

        error_message = response['error_msg']

        # Self verification
        is_task_accomplished, feedback = evaluate_task(get_cleaned_html(response['state']), task=action, action=message, execution_error=error_message)
        print(f"Task completed: {is_task_accomplished}")
        print(f"Feedback: {feedback}")

if __name__ == "__main__":
    main()
