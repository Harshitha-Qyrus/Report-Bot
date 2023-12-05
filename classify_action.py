from completion import Completion, FunctionCall
from promts import GET_ACTION_PROMPT
from schemas.function_schemas import AnswerQuestionSchema, GenerateGraphAndInsights

class ClassifyAction:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, user_desc):

        messages = [{
            "role": "system",
            "content": GET_ACTION_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GET_ACTION_PROMPT.user_prompt.format(user_description=user_desc)
        }]

        functions = [{
            "name": "answerQuestion",
            "description":
            """This answers user's question.
                """,
            "parameters": AnswerQuestionSchema.schema()
        }, 
        {
            "name": "generateGraph",
            "description":
            """This generates graph.
                """,
            "parameters": GenerateGraphAndInsights.schema()
        },
        {
            "name": "generateReport",
            "description":
            """This generates graph and insights.
                """,
            "parameters": GenerateGraphAndInsights.schema()
        }]
        

        function_name, function_args = self.function_call(messages=messages, model_name='gpt-4-32k', functions=functions, call_first=False)
        return function_name, function_args