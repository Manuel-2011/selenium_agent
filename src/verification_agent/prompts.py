EVALUATE_TASK = """Browser content: {state}

The task: {task}

Function called: {action}

The code execution error: {execution_error}

Given the current state of the webpage, the task, the code executed (function called), and the code execution error, evaluate whether the task has been completed and provide useful yet short feedback in natural language to help the agent achieve its task in the next trial if needed.\nYour answer must be in the following format:\nReasoning of the evaluation of the task: <What is the current state of the page? What is the task asking me to do? How I would know if the task was completed?>\nFeedback: ...\nWas the task completed? <True/False>"""