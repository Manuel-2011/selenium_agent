import os
import sys
import re

os.chdir('./src')
# setting path
sys.path.append(os.getcwd())

# importing project modules
from openai_utils import compile_messages, format_message,  get_completion_from_messages
from planner_agent.prompts import CREATE_PLAN


def get_raw_plan(goal: str) -> str:
    create_plan_prompt = format_message(CREATE_PLAN.format(goal=goal))
    context = compile_messages(create_plan_prompt)
    plan = get_completion_from_messages(context)
    return plan

def parse_plan(plan: str) -> list[str]:
    # Use regex to find all numbered items in the text
    numbered_items = re.findall(r'\d+\.\s+(.+)', plan)

    return [item.strip() for item in numbered_items]

def get_plan(goal: str) -> list[str]:
    raw_plan = get_raw_plan(goal)
    actions = parse_plan(raw_plan)
    return actions
