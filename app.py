from run import classify_action
import matplotlib.pyplot as plt
# %matplotlib inline
import cv2
import traceback
import run

def main():
    try:
        function_name, function_args = classify_action(input("What do you want to know?"))
        print("Func name ", function_name)
        print("Func args ", function_args)

        function_name = function_name.split("functions.")[-1] if 'functions.' in function_name else function_name
        print(" In app.py func_name after splitting",function_name)
        fun_obj = getattr(run, function_name)
        print("\033[46m In app.py getattr after splitting \033[0m",fun_obj)
        response = fun_obj(function_args)
        print("\033[46m In app.py response after splitting \033[0m",response)

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