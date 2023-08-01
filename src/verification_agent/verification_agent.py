import os
import sys
import re

# importing project modules
from openai_utils import compile_messages, format_message,  get_completion_from_messages
from verification_agent.prompts import EVALUATE_TASK

def parse_evaluation(evaluation: str) -> tuple[bool, str]:
    try:
        is_task_complete = re.search(r'Was the task completed\?\s+(.+)', evaluation).group(1) == 'True'
    except:
        is_task_complete = False
    
    try:
        feedback = re.search(r'Feedback:\s+(.+)', evaluation).group(1)
        return is_task_complete, feedback
    except:
        return is_task_complete, ''

def evaluate_task(state: str, task: str, action: str, execution_error: str = None) -> tuple[bool, str]:
    """
    Evaluates whether the task has been completed.
    """

    completion_prompt = format_message(
        EVALUATE_TASK.format(state=state, task=task, action=action, execution_error=execution_error)
    )
    print("Evaluation prompt:", completion_prompt)
    context = compile_messages(completion_prompt)
    completion = get_completion_from_messages(context, model="gpt-3.5-turbo-16k", temperature=1.5)
    print("Evaluation completion:", completion)
    # completion = get_completion_from_messages(context, model="gpt-3.5-turbo-16k")
    return parse_evaluation(completion)