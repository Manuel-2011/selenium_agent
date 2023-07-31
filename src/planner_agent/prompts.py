PLAN_FORMAT = """Give me your answer only in the following format:
To achieve the goal I will need to perform the following actions:
1. Open the web browser
2. ... """

CREATE_PLAN = """Given that you are an AI agent using selenium to navigate a web browser. What are the high level actions you would need to take to achieve the goal "{goal}"?""" + PLAN_FORMAT