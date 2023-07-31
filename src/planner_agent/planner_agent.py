import os
import sys
import re

os.chdir('./src')
# setting path
sys.path.append(os.getcwd())

# importing project modules
from openai_utils import compile_messages, format_message,  get_completion_from_messages
from planner_agent.prompts import CREATE_PLAN
from planner_agent.constants import DEFAULT_RAW_PLAN


def get_raw_plan(goal: str) -> str:
    create_plan_prompt = format_message(CREATE_PLAN.format(goal=goal))
    context = compile_messages(create_plan_prompt)
    plan = get_completion_from_messages(context)
    return plan, context

def parse_plan(plan: str) -> list[str]:
    # Use regex to find all numbered items in the text
    numbered_items = re.findall(r'\d+\.\s+(.+)', plan)

    # Get rid of the first item, which is open the web browser
    numbered_items = numbered_items[1:]

    return [item.strip() for item in numbered_items]

def get_plan(goal: str, test_mode = False) -> list[str]:
    if test_mode:
        raw_plan = DEFAULT_RAW_PLAN
        print(raw_plan)
    else:
        raw_plan, context = get_raw_plan(goal)

    # Get user feedback on the plan
    while True and not test_mode:
        print("Here is the plan:")
        print(raw_plan)
        print("Does this plan look good?")
        user_feedback = input("Press enter to continue with the plan or provide some feedback: ")
        if user_feedback == "":
            break
        else:
            # Improve the plan based on the user feedback
            context.append(format_message(raw_plan, role="assistant"))
            context.append(format_message(user_feedback))
            raw_plan = get_completion_from_messages(context)

    actions = parse_plan(raw_plan)
    return actions
