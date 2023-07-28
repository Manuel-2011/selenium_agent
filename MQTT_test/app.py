from suscriber import Suscriber
from publisher import Publisher
import time
import threading
import os

# Function to be executed in the first thread
def thread_one_function():
  Suscriber()

# Function to be executed in the second thread
def thread_two_function():
  publisher = Publisher()
  publisher.send_message("Hello World!")

def main():
  # Create thread objects
  thread_one = threading.Thread(target=thread_one_function)
  thread_two = threading.Thread(target=thread_two_function)
  
  # Start the threads
  thread_one.start()
  time.sleep(5)
  thread_two.start()


if __name__ == "__main__":
  main()