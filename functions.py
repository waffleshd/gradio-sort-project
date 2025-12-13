import gradio as gr
import pandas as pd
import random
import time

class Recorder():

    '''
    Class to record the taken steps by bubble_sort()
    '''

    def __init__(self):
        self.steps = []

    def record_states(self,arr : list, comparing: tuple, swapped: bool, n : int, description: str = ""):
        '''
        Records the steps that bubble_sort() takes
        '''

        self.steps.append(
            {
                'array' : tuple(arr),
                'comparing' : comparing,
                'swapped' : swapped,
                'n' : n,
                'description' : description
            }
        )
    
class Main():

    def bubble_sort(self,arr: list) -> tuple[str, list[int]]:
        '''
        Sort the given array. Uses record_states() to record each step taken during the sort. \n
        str returns the sorted array \n
        list[int] returns the list of states
        '''
        arr = list(arr)  # AI CHANGE: work on a copy so original list isn't mutated
        recorder = Recorder() # init the recorder
        n = len(arr)
        swapped = True

        recorder.record_states(arr,(0,0),swapped, n,"Initial State")      # record initial state

        while swapped:
            swapped = False
            i = 1
            while i < n:
                recorder.record_states(arr,(i-1,i), swapped, n, f"Comparing {arr[i]} and {arr[i-1]}.") # record that we are comparing two values
                if arr[i] < arr[i-1]:
                    recorder.record_states(arr,(i-1,i), swapped, n, f"{arr[i-1]} is bigger than {arr[i]} - swap")
                    arr[i],arr[i-1] = arr[i-1],arr[i]
                    swapped = True
                    recorder.record_states(arr,(i-1,i),swapped, n,f"Swapped {arr[i]} and {arr[i-1]}.") # record that we have swapped the values
                i += 1
            n -= 1
        
        recorder.record_states(arr,None,swapped, n,"Sorting done") #record final state

        return str(arr), recorder.steps

    def custom_list(self, input_text : str) -> tuple[list,list]:
        '''
        Transcribes string to a list
        '''

        ret_list = []
        store = "" 
        sign = 1

        for char in input_text:
            if char == "," and store:     # if we encounter a comma, we have reached the end of the number, so we may append it to the list
                ret_list.append(int(store)*sign)
                print(store)
                store = ""  # reset the storage string
                sign = 1
            elif char == "-":
                sign = -1
            elif char.isdigit():
                store += char   # if we encounter a digit, add it to the storage
                print(store)

        if store != "":
            print(store)
            ret_list.append(int(store)*sign) # append the last number to the list
            
        
        return ret_list, ret_list

    def print_states(self, steps : list[dict], speed : int):
        '''
        Yields the text and  panda dataframe necessary to display on the front-end
        '''
        delay = (101-int(int(speed))) / 100    # calculate the delay based on the speed

        if not steps:
            return "", []

        for i, step in enumerate(steps):    # for each recorded step, we generate some text
            out_txt = ""
            out_txt += f"Step {i}: {step['description']} \n"
            out_txt += f"  Swapped: {step['swapped']} \n"
            if step['comparing']:
                out_txt += f"  Comparing indices: {step['comparing']}"

            out_arr = self.construct_pd(step['array'],step['comparing'] if step['comparing'] else None, step['n']) # generate this step's dataframe

            yield out_txt, out_arr
            time.sleep(delay)       

    def construct_pd(self, arr : list, comparing : tuple, n : int) -> pd.DataFrame:
        '''
        Construct a panda dataframe from the step's frame.
        '''

        d = {'x' : range(len(arr)), # generate x values from 1 -> len(arr)
             'y' : arr, # use arr values for y values
             'highlighted' : ['not comparing']*len(arr)}    # start by making all values not highlighted
        
        df = pd.DataFrame(data=d)   # construct panda dataframe


        for i in range(n,len(arr)):
            df.loc[i,'highlighted'] = 'sorted'

        if comparing is not None:   # if we have a comparison, then we will label the compared values as "comparing"
            for i in comparing:
                if 0 <= i < len(arr):
                    df.loc[i, 'highlighted'] = 'comparing'
        else:
            df['highlighted'] = 'comparing' # this only occurs when we are at the end of the sorting sequence, so we set all values to "comparing" to show that we are done sorting
        
        return df
    
    def gen_random_array(self, size : int, min : int, max : int) -> tuple[list,list]:
        '''
        Generate a randomized array based on the input variables
        '''

        arr = []

        for _ in range(int(size)):
            arr.append(random.randint(int(min),int(max)))

        return arr, arr

class PlotFixer():
    '''
    Gradio plots are weird when dealing with color maps. Using this as a duct-tape fix
    '''

    def reset_plot(self):
        yield pd.DataFrame({'x': [0,1,2], 'y': [0,0,0], 'highlighted': ['comparing','not comparing','sorted']})
        return gr.update(visible=False)

    def show_plot(self):
        return gr.update(visible=True)

