from run import classify_action
import matplotlib.pyplot as plt
# %matplotlib inline
import cv2
import traceback
import run
from queries import Queries
from db_utils.db_executor import MYSQL_ADAPTER
from ipywidgets import widgets
from IPython.display import display,clear_output

def main():
    
    try:
        selected_team = team_dropdown.value
        selected_service = service_dropdown.value
        print("Selected Team: ", selected_team)
        print("Selected Service: ", selected_service)
        team_id=mysql_adapter.execute_query(Queries.teams_id_schema.format(user_email="vatsals@quinnox.com",team_name=team_dropdown.value))
        team_id_value=team_id['uuid'].to_list()
        print("Team uuid:",team_id_value)
        
        
        function_name, function_args = classify_action(input("What do you want to know?"))
        print("Func name ", function_name)
        print("Func args ", function_args)

        function_name = function_name.split("functions.")[-1] if 'functions.' in function_name else function_name
        print(" In app.py func_name after splitting",function_name)
        fun_obj = getattr(run, function_name)
        response = fun_obj(function_args,selected_team)

        if function_name == "generateGraph" and response:
            im = cv2.imread(f"results/{response}.png")
            plt.imshow(im)
        elif function_name == "generateReport" and response:
            for i, graph in enumerate(response):
                print(f"graph is ", graph)
                if graph['graph_filename']:
                    plt.figure(i+1)
                    im = cv2.imread(f"results/{graph['graph_filename']}.png")
                    plt.imshow(im)
                    plt.show()
                    print(graph['graph_description'])
                    print(graph['graph_details'])
        else:
            print(response)
    except Exception as e:
        print("EXCEPTION ", traceback.format_exc())
        print("Something went wrong, Please try again ")
        
        
mysql_adapter = MYSQL_ADAPTER()
user_result=mysql_adapter.execute_query(Queries.teams_schema.format(user_email="vatsals@quinnox.com"))
team_names = user_result['team_name'].tolist()
# print("Team result:",team_names)
services = ['Please Select','Web Automation', 'Desktop Testing', 'Mobility Testing']
team_dropdown = widgets.Dropdown(placeholder='Please Select',value=None,options=team_names, description='Teams:')
service_dropdown = widgets.Dropdown(options=services, description='Services:')
display(team_dropdown, service_dropdown)
output = widgets.Output()
display(output)

def on_dropdown_change(change):
    with output:
        clear_output(wait=True)
        selected_team = team_dropdown.value
        selected_service = service_dropdown.value
        print("Selected Team:", selected_team)
        print("Selected Service:", selected_service)

team_dropdown.observe(on_dropdown_change, names='value')
service_dropdown.observe(on_dropdown_change, names='value')
# Wait for user interaction
input("Select values from the dropdowns and press Enter...")