from db_utils.db_executor import MYSQL_ADAPTER
from db_utils.db_converter import SQL_CONVERTER, DB_SCHEMA_GENERATOR, CorrectQuery
from classify_action import ClassifyAction
from format_answer import FORMAT_RESPONSE
from numbered_card_answer import NUMBER_RESPONSE
from generate_graphs_and_insights import GenerateGraphs, CorrectCode
from generate_report_layout import GenerateReportLayout
from generate_report_lists import GenerateReportList
from io import StringIO
import pandas as pd
import asyncio
import textwrap
import concurrent.futures
import uuid
import tqdm
from typing import List


def classify_action(user_description):
    """
    Classifies the user_description to a function
    """
    classify_action = ClassifyAction()
    function_name, function_args = classify_action(user_desc=user_description)
    # print("returning in run.py fun_name,func_args:\n",function_name,function_args)

    if function_name and function_args:
        return function_name, function_args

    else:
        if function_name:
            return function_name, {"user_description": user_description}
        return None, None


async def answerQuestion(user_description: str, selected_team: str):
    queried_data_str = await __get_data__(user_description=user_description,
                                          selected_team=selected_team)
    # print("\033[43m Raw answer:\033[0m",queried_data_str)
    formatted_answer =await __format_answer__(question=user_description,
                                         answer=queried_data_str)
    print("\033[43m Formatted Answer:\033[0m", formatted_answer)
    return formatted_answer


async def __format_answer__(question, answer):
    format_response = FORMAT_RESPONSE()
    formatted_answer = format_response(question=question, answer=answer)
    formatted_answer = formatted_answer.get('formatted_answer')
    if formatted_answer:
        return formatted_answer
    else:
        return None


async def numberedcard(user_description: List[str], db_schema, team_id):
    queried_data_str = await __get_data_without_db(
        user_description=user_description,
        db_schema=db_schema,
        team_id=team_id)
    # print("\033[43m Raw answer:\033[0m", queried_data_str)
    final_answer = _format_numberd_card(question=user_description,
                                        answer=queried_data_str)
    # print("\033[43m Formatted Answer:\033[0m",final_answer)
    return final_answer


def _format_numberd_card(question, answer):
    abstract_answers = NUMBER_RESPONSE()
    get_numbers = abstract_answers(question=question, answer=answer)
    extracted_number = get_numbers['formatted_answers']
    if extracted_number:
        return extracted_number
    else:
        return None


async def generateGraph(user_description: str, selected_team: str):
    print("Generating Graph......")
    queried_data_str = await __get_data__(user_description=user_description,
                                          selected_team=selected_team)
    graph_filename = await __generate_graphs_and_insights__(
        user_description=user_description, queried_data_str=queried_data_str)
    # print("Graph generated in ", graph_filename)
    return graph_filename


async def generateGraph_Report(user_description:list[str],db_schema,team_id):
    print("Generating Graph for Reports......")
    queried_data_list = await __get_data_without_db(user_description=user_description,
                                          db_schema=db_schema,team_id=team_id)
    print("Checking quried data", queried_data_list)
    graph_filename =await __generate_graphs_and_insights_for_report(
        user_description=user_description, queried_data_list=queried_data_list)
    # print("Graph generated in ", graph_filename)
    return graph_filename


async def __generate_graphs_and_insights_for_report(user_description,
                                                    queried_data_list):
    generate_graphs = GenerateGraphs()
    data_frames = [pd.read_csv(StringIO(data)) for data in queried_data_list]
    selected_rows_data_frames = [df.head(2) for df in data_frames]
    graph_args = await generate_graphs(
        user_description=user_description,
        sample_data=selected_rows_data_frames)

    print("Graph_args:", graph_args)
    length=len(graph_args)
    print("LENGTH IS:",length)
    filenames = []
    counts=0
    for single_graph, single_df_from_str in zip(graph_args, data_frames):
        graph_uuids = str(uuid.uuid4())
        filename = __run_code__report(graph_code=(f"""{single_graph}"""),
                                      filename=graph_uuids,
                                      df_from_str=single_df_from_str)
        print("Image saved in ", filename)
        counts+=counts
        filenames.append(filename)
    
    # if (length == counts):
    #     print("Filenames are:",filenames)
    #     counts=0
    return filenames


def __run_code__report(graph_code, filename, df_from_str, attempt=0):
    if graph_code:
        global_vars = globals()
        try:
            print("Trying to execute... ")
            exec(graph_code, global_vars)
            # filename = str(uuid.uuid4())
            plot_graph(data=df_from_str, save_filename=filename)
            print("Executed")
            return filename
        except Exception as e:
            if attempt > 5:
                return None
            correct_code = CorrectCode()

            graph_args = correct_code(graph_code, str(e))
            # print("\033[94m Corrected code in graph report\033[0m", graph_args)
            graph_code_str = graph_args.get("graph_code")
            print("CORRECTING CODE")
            return __run_code__report(graph_code=graph_code_str,
                                      filename=filename,
                                      df_from_str=df_from_str,
                                      attempt=attempt + 1)

    else:
        return None


async def __generate_graphs_and_insights__(user_description, queried_data_str):
    generate_graphs = GenerateGraphs()
    csv_buffer = StringIO(queried_data_str)
    df_from_str = pd.read_csv(csv_buffer)
    data_frames = [pd.read_csv(StringIO(queried_data_str))]
    selected_rows_data_frames = [data_frames[:2]]
    df_from_str.to_csv("complete_data.csv", index=False)
    graph_args = await generate_graphs(
        user_description=user_description,
        sample_data=selected_rows_data_frames)
    # graph_code = graph_args.get("graph_code")

    graph_code = '\n'.join(graph_args)
    filename = __run_code__(graph_code=graph_code, df_from_str=df_from_str)
    print("Image saved in ", filename)
    return filename


def __run_code__(graph_code: str, df_from_str, attempt=0):
    if graph_code:
        global_vars = globals()
        try:
            exec(graph_code, global_vars)

            filename = str(uuid.uuid4())
            plot_graph(data=df_from_str, save_filename=filename)
            print("EXECUTED:", filename)
            return filename
        except Exception as e:
            if attempt > 5:
                return None
            correct_code = CorrectCode()
            graph_args = correct_code(graph_code, str(e))
            print("\033[41m Corrected code \033[0m", graph_args)
            graph_code_str = graph_args.get("graph_code")
            print("\033[41m Corrected code in graph args \033[0m",
                  graph_code_str)
            print("CORRECTING CODE")
            return __run_code__(graph_code=graph_code_str,
                                df_from_str=df_from_str,
                                attempt=attempt + 1)

    else:
        return None


async def __get_data__(user_description: str, selected_team: str):
    sql_converter = SQL_CONVERTER()
    schema_generator = DB_SCHEMA_GENERATOR(selected_team=selected_team)

    db_schema, team_id = schema_generator()
    args = await sql_converter(user_description, db_schema, team_id)
    # print("\033[32m QUERY predicted is \033[0m", args)
    # results = list(map(lambda arg: __execute_query__(arg, db_schema), args))
    results = __execute_query__(args, db_schema)
    return results

    #TODO LINT SQL
    # print("\033[32m QUERY predicted is \033[0m", query)


async def __get_data_without_db(user_description, db_schema,team_id):
    sql_converter = SQL_CONVERTER()
    args = await sql_converter(user_description, db_schema, team_id
                               )
    # print("\033[32m QUERY predicted is \033[0m",args)
    results =list(__execute_query_for_list(args, db_schema))
    return results


def __execute_query_for_list(query_list, db_schema):
    mysql_adapter = MYSQL_ADAPTER()
    for query in query_list:
        if query:
            try:
                result = mysql_adapter.execute_query(query)
                # print("\033[32m RESULT IS \033[0;32m ", result)
            except Exception as e:
                correct_query = CorrectQuery()
                args = correct_query(query, str(e), db_schema)
                query = args.get('mysql_command')
                # print("\033[32m QUERY predicted is \033[0;32m ", query)
                return __execute_query__(query, db_schema)

            yield result.to_csv(index=False)
        else:
            yield None


def __execute_query__(query, db_schema):
    mysql_adapter = MYSQL_ADAPTER()
    if query:
        try:
            result = mysql_adapter.execute_query(query)
            # print("\033[32m RESULT IS \033[0;32m ", result)
        except Exception as e:
            correct_query = CorrectQuery()
            args = correct_query(query, str(e), db_schema)
            query = args.get('mysql_command')
            # print("\033[32m QUERY predicted is \033[0;32m ", query)
            return __execute_query__(query, db_schema)

        return result.to_csv(index=False)
    else:
        return None


async def generateReport(user_description: str, selected_team: str):
    """
    1. gets the schema
    2. analyzes schema and user description and comes up with a list of graphs and content that can be on the report
    3. For each point, generate graph code and content
    4. Generates an HTML out of it
    """
    #Get schema
    schema_generator = DB_SCHEMA_GENERATOR(selected_team=selected_team)
    db_schema, team_id = schema_generator()

    #analyze schema and generate ideas
    graph_ideas = __generate_graph_ideas__(db_schema=db_schema,
                                           user_description=user_description)
    # print("Printing graph ideas", graph_ideas)
    
    # insight_ideas
    insight_ideas = __generate_insight_ideas__(
        db_schema=db_schema, user_description=user_description)

    graphs = []
    response = []
    questions_list = []
    only_question = []
    counter = 1

    for question in tqdm.tqdm(insight_ideas):
        name_of_question = question.get("questions")
        details_on_question = question.get("detail")
        only_question.append(f"{counter}.{name_of_question}")
        counter += 1
        question_str = f" [Generate a solution for the following details: Question:{name_of_question}, details:{details_on_question}]"
        questions_list.append(question_str)
    # print("All Questions in One List:", questions_list)
    responses = await numberedcard(user_description=questions_list,
                                   db_schema=db_schema,team_id=team_id)
    print("\033[93m QUESTIONS::\033[0m")
    for question in only_question:
        print(question)
    print("\033[93m This is response:\033[0m",responses)

    graph_questions_list=[]
    result_list=[]
    for graph_idea in tqdm.tqdm(graph_ideas):
        graph_description = graph_idea.get("graph_description")
        graph_details = graph_idea.get("graph_details")
        graph_question_str = f" [Generate graph for following details. graph_description:: Question:{graph_description}, details:{graph_details}]"
        graph_questions_list.append(graph_question_str)
    graph_filenames=await generateGraph_Report(user_description=graph_questions_list,
                                   db_schema=db_schema,team_id=team_id)
    print("Graph file names at the end:",graph_filenames)
    
    for idea, filename in zip(graph_ideas, graph_filenames):
        new_dict = {
            'graph_description': idea['graph_description'],
            'graph_details': idea['graph_details'],
            'graph_filename': filename
            }
        result_list.append(new_dict)
        
    # for result in result_list:
    #     print(result)   
    return result_list


def __generate_graph_ideas__(db_schema, user_description):
    """gets the db_schema and user_description and gives it to gpt, and ask it to generate the list of graph description and graph content that can be generated to create the report"""
    generate_report_layout = GenerateReportLayout()
    args = generate_report_layout(db_schema=db_schema,
                                  user_description=user_description)
    graph_ideas = args.get("graphs")
    return graph_ideas


def __generate_insight_ideas__(db_schema, user_description):
    """gets the db_schema and user_description and gives it to gpt, and ask it to generate the list of insight description and insight content that can be generated to create the report"""
    generate_report_lists = GenerateReportList()
    args = generate_report_lists(db_schema=db_schema,
                                 user_description=user_description)
    questions_list = args.get("insight")
    return questions_list
