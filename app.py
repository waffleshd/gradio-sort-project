import gradio as gr
import pandas as pd
import random
import time


class BubbleSort():
    def __init__(self):
        self.steps = []

    def record_states(self,arr : list, comparing: tuple, swapped: bool, description: str = ""):
        self.steps.append(
            {
                'array' : arr,
                'comparing' : comparing,
                'swapped' : swapped,
                'description' : description
            }
        )


    

def bubble_sort(arr: list):
    Bubble = BubbleSort()
    n = len(arr)
    swapped = True

    Bubble.record_states(arr,None,swapped,"Initial State")

    while swapped:
        swapped = False
        i = 1
        while i < n:
            Bubble.record_states(arr,(i-1,i), swapped, f"Comparing {arr[i]} and {arr[i-1]}.")
            if arr[i] < arr[i-1]:
                arr[i],arr[i-1] = arr[i-1],arr[i]
                swapped = True
                Bubble.record_states(arr,None,swapped,f"Swapped {arr[i]} and {arr[i-1]}.")
            i += 1
        n -= 1
    
    Bubble.record_states(arr,None,swapped,"Sorting done")

    return str(arr), Bubble.steps

def custom_list(input_text : str) -> list:
    ret_list = []
    store = ""
    for char in input_text:
        if char == ",": 
            ret_list.append(int(store))
            store = ""
        elif char.isdigit():
            store += char
        else: print("invalid input")
    if store != "":
        ret_list.append(int(store))
    
    return ret_list, ret_list

def print_states(steps):
    for i, step in enumerate(steps):
        out_txt = ""
        out_txt += f"Step {i}: {step['description']} \n"
        out_txt += f"  Array: {step['array']} \n"
        if step['comparing']:
            out_txt += f"  Comparing indices: {step['comparing']}"

        yield out_txt
        time.sleep(1)       

with gr.Blocks(title="Binary Sorting") as demo: #TODO : Change to app instead of demo when done
    with gr.Row():
        ret_list = gr.State()
        steps_state = gr.State()
        input_tb = gr.Textbox(placeholder="Input custom list, separating indexes with commas.")
        newlist = gr.Button()
    with gr.Row():
        output_tb = gr.Textbox(placeholder="Output array")
        sort = gr.Button("Sort")
        display = gr.Button("Display")

    with gr.Row():
        states_tb = gr.TextArea(lines=3,placeholder="Displays the steps of bubble sort")


    newlist.click(fn=custom_list,inputs=input_tb, outputs=[output_tb,ret_list])
    sort.click(fn=bubble_sort,inputs=[ret_list],outputs=[output_tb,steps_state])
    display.click(fn=print_states,inputs=steps_state,outputs=states_tb)

if __name__ == "__main__":
    demo.launch()
    