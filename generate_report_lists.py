
from completion import Completion, FunctionCall
from promts import GENERATE_INSIGHT_LIST_PROMPT
from schemas.function_schemas import GenerateReportInsightListsSchema

class GenerateReportList:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, user_description, db_schema):
        messages = [{
            "role": "system",
            "content": GENERATE_INSIGHT_LIST_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GENERATE_INSIGHT_LIST_PROMPT.user_prompt.format(user_description=user_description, db_schema=db_schema)
        }]
        

        functions = [{
            "name": "showListReport",
            "description":
            """This function get the user description and database schema and generates the list of direct entities like insights that can be shown in report.
                """,
            "parameters": GenerateReportInsightListsSchema.schema()
        }]
        

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        # print("\033[47m ARGSSSSS IN REPORT \033[0m", args)
        return args