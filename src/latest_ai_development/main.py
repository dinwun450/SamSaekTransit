#!/usr/bin/env python
import sys
import warnings
import os
from latest_ai_development.crew import LatestAiDevelopmentCrew
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with the provided inputs.
    """
    prompter = input("Enter something... ")
    inputs = {
        "role": "user",
        "content": prompter,
        "exa_search_results": False, # Set to True if you want to display Exa search results
        "needs_nearby_transit": False,  # Set to True if you want to find nearby transit options
    }
    try:
        # Initialize the crew and run it with the inputs
        crew = LatestAiDevelopmentCrew()
        result = crew.crew().kickoff(inputs)
        print("Crew execution completed successfully.")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    prompter = input("Enter something... ")
    inputs = {
        "role": "user",
        "content": prompter,
    }
    try:
        LatestAiDevelopmentCrew().crew().train(inputs=inputs, n_iterations=5, filename="crew_training_results.json")

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopmentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """

    inputs = {
        "option": "routes",          # Specify the type of data to fetch (e.g., routes, stops)
        "route_type": 1,             # Example route type
        "search": "Berryessa",  # Example search query
    }
    
    try:
        LatestAiDevelopmentCrew().crew().test(inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
