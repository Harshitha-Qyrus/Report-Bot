from completion import Completion, FunctionCall
from promts import GET_ACTION_PROMPT
from schemas.function_schemas import AnswerQuestionSchema, GenerateGraphAndInsights

class ClassifyAction:
    def __init__(self):
        print("\033[91m I came first \033[0m")
        self.completion = Completion()
        print("\033[91m I came after completion \033[0m")
        self.function_call = FunctionCall()
        print("\033[91m I came after function call in init \033[0m")

    def __call__(self, user_desc):

        messages = [{
            "role": "system",
            "content": GET_ACTION_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GET_ACTION_PROMPT.user_prompt.format(user_description=user_desc)
        }]
        print("\033[93m This is classification messages: \033[0m",messages)

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
        
        print("\033[93m This is functions: \033[0m",functions)

        function_name, function_args = self.function_call(messages=messages, model_name='gpt-4-32k', functions=functions, call_first=False)
        return function_name, function_args