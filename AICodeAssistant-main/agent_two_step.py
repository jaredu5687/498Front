# from langchain_community.llms import LlamaCpp
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

MODEL_NAME = "codellama:7b"

def process_code(code_content):
    """Process the code using AI agents and return the results"""
    # Initialize the model
    model = Ollama(model=MODEL_NAME)
    
    # Create agents
    classifier = Agent(
        role = "Python code debugger",
        goal = "Accurately locate every error in Python code. classifies each error into one of these types: syntax error, exception, \
        or no errors. Also provide a line number along with it if it is not 'no errors'.",
        backstory = "Your are an AI assistant whose only job is to locate errors in Python code. \
        Don't be afraid to point out any errors that you have noticed.",
        verbose = True,
        allow_delegation = False,
        llm = model    
    )

    fixer = Agent(
        role = "Python code fixer",
        goal = "Locate each errors and its cause by analyzing the definition of the error type provided, \
        and the code around the specified line number. Provide the fixed Python code that has no error. \
        If no error was found, then output 'no fixes were made' without making fixes to the code.",
        backstory = "Your are an AI assistant whose only job is to locate and provide a fix to the error based on the \
        type of the error and its line number. \
        Relate to the code around the line number provided to ensure the error was understand correctly. \
        Both error type and line number will be provided to you by the 'Python code debugger' agent. \
        There is a chance that there are 'no errors', in that case no fixes are required.",
        verbose = True,
        allow_delegation = False,
        llm = model    
    )

    classify_errors = Task(
        description = f"Locate and classfy errors in the Python code '{code_content}'",
        agent = classifier,
        expected_output = "A line number to the error code and one of these options: 'syntax error', 'exception', or 'no errors'.",
    )

    fixes_to_errors = Task(
        description = f"Provide fixes to the errors in Python code '{code_content}' based on the error types and the line numbers \
        of each error provided by the 'classifier' agent.",
        agent = fixer,
        expected_output = "fixes to the Python code based on the error types and the line numbers of each error \
        provided by the 'classifier' agent. If the error types is 'no errors', then output 'no fixes were made'.",
    )

    defect_crew = Crew(
        agents = [classifier, fixer],
        tasks = [classify_errors, fixes_to_errors],
        verbose = 2,
        process = Process.sequential
    )

    return defect_crew.kickoff()

# Only run this if the file is run directly
if __name__ == "__main__":
    # Your test code here
    lines = 'print("hello world")\n;\nprint("Hi")\n;\n'
    output = process_code(lines)
    print(output)