from fastapi import FastAPI
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

# uvicorn web_agent:app --reload

# Create a FastAPI instance
app = FastAPI()
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get("https://www.google.com")


def run_function_from_string(function_string, *args):
    # Use regular expressions to find the function definition and extract the function name
    try:
        function_match = re.search(r"def\s+(\w+)\s*\(", function_string)
        if function_match:
            function_name = function_match.group(1)
        else:
            raise ValueError("Function definition not found in the string.")

        # Compile the function_string into a code object
        code_obj = compile(function_string, "<string>", "exec")

        # Create a new local namespace for the function
        local_namespace = {}

        # Execute the compiled code in the new namespace
        exec(code_obj, globals(), local_namespace)
        # Extract the function from the namespace
        if function_name in local_namespace:
            function = local_namespace[function_name]
            # Call the function with the provided arguments
            return function(*args), False, None

        else:
            raise ValueError(f"Function '{function_name}' not found in the string.")
    except Exception as e:
        print(e)
        return driver.page_source, True, str(e)


# Define a route for the root endpoint
@app.post("/")
def read_root(data: dict):
    global driver
    print(data)
    response, is_error, error_msg = run_function_from_string(data["code"], driver)
    return {"is_error": is_error, "state": response, "error_msg": error_msg}
