import os
from pathlib import Path
from pathlib import PurePath
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
# from IPython.display import display_markdown


def main():

    generated_code = generate_code(
            """Write Python code to generate a 800x600 image with alternating
            yellow, purple and green bars of height 10 going across.
            Then draw a white circle with a radius of 50
            in the center of the image. Then draw yellow lines of height 10
            going across the image with a gap of 20 between every two lines.
            Use PIL to render it"""
        )
    with open("generated_code.py", "w") as file:
        file.write(generated_code)


def get_path_for_environment_file():
    find_path = Path(__file__)
    path_to_root = PurePath(find_path).parents[0]
    path_to_env = path_to_root.joinpath('env', '.env')
    return path_to_env

def generate_code(prompt):
    path_for_environment_file = get_path_for_environment_file()
    load_dotenv(path_for_environment_file)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm_model = "gpt-4o-mini"
    llm = ChatOpenAI(model=llm_model, temperature=0.0, n=1)

    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. "
                "You write reliable python program code. "
                "You always include the prompt used in a multi-line Python"
                " comment string at the beginning and prefix it with "
                "Prompt:. Also include the model name and version used "
                "in a comment string at the beginning of the code "
                "and prefix it with Model:"
            )
        ),
        HumanMessage(content=prompt),
    ]
    output = llm.invoke(messages)
    return output.content


if __name__ == '__main__':
    main()
