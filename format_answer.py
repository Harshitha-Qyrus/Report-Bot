from completion import Completion, FunctionCall
from promts import ANSWER_FORMAT_PROMPT
from schemas.function_schemas import FORMAT_ANSWER

class FORMAT_RESPONSE:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, question, answer):
        messages = [{
            "role": "system",
            "content": ANSWER_FORMAT_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": ANSWER_FORMAT_PROMPT.user_prompt.format(question=question, answer=answer)
        }]

        functions = [{
            "name": "formatAnswer",
            "description":
            """This formats and explains the answer to the question asked.
                """,
            "parameters": FORMAT_ANSWER.schema()
        }]

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        return args