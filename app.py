import gradio as gr
import functions as fn

# AI CHANGE: Added mode switching helper for mutually exclusive input modes
# Any code block tagged with 'AI CHANGE' was introduced or modified by AI.

# UI helper: switch between custom input and random generation modes
def switch_mode(mode: str):  # AI CHANGE
    custom = mode == "Custom"
    random_mode = mode == "Random"
    return (
        gr.update(visible=custom),        # AI CHANGE: show/hide custom textbox
        gr.update(visible=custom),        # AI CHANGE: show/hide load array button
        gr.update(visible=random_mode),   # AI CHANGE: show/hide size slider
        gr.update(visible=random_mode),   # AI CHANGE: show/hide min value input
        gr.update(visible=random_mode),   # AI CHANGE: show/hide max value input
        gr.update(visible=random_mode),   # AI CHANGE: show/hide random generator button
    )

with gr.Blocks(title="Bubble Sort Visualizer") as demo:  # AI CHANGE: improved, uncluttered layout

    recorder = fn.Recorder()
    main = fn.Main()
    fixer = fn.PlotFixer()

    # States
    ret_list = gr.State()
    steps_state = gr.State()

    # Header / description
    gr.Markdown("""### Bubble Sort Visualizer\nProvide a custom array or generate a random one (modes are mutually exclusive). Sort it and watch each comparison. Cannot adjust speed during playback.\n""")  # AI CHANGE: descriptive header

    # Styling block (light subtle customizations) AI CHANGE
    gr.HTML("""
    <style>
    /* AI CHANGE: light styling tweaks */
    .gradio-container {font-family: Inter, system-ui, sans-serif;}
    .gr-button {min-height: 42px;}
    .large-text textarea {font-size: 16px !important;}
    </style>
    """)

    input_accordion = gr.Accordion("Input Mode", open=True)  # AI CHANGE
    with input_accordion:
        mode_radio = gr.Radio(["Custom", "Random"], value="Custom", label="Select Mode")  # AI CHANGE: mode selector
        with gr.Row():
            input_tb = gr.Textbox(label="Custom Array", placeholder="e.g. 5,3,8,1", visible=True)  # AI CHANGE
            newlist = gr.Button("Load Array", visible=True)  # AI CHANGE
        with gr.Row():
            size = gr.Slider(minimum=1, maximum=100, step=1, value=10, label="Size", visible=False)  # AI CHANGE
            min_val = gr.Number(label="Min", value=0, visible=False)  # AI CHANGE
            max_val = gr.Number(label="Max", value=100, visible=False)  # AI CHANGE
            gen_random = gr.Button("Generate Random", visible=False)  # AI CHANGE

    with gr.Row():  # AI CHANGE: action toolbar
        sort = gr.Button("Sort", variant="primary")  # AI CHANGE
        display = gr.Button("Run Animation")  # AI CHANGE
        speed_slider = gr.Slider(minimum=1, maximum=100, value=50, label="Speed")  # AI CHANGE
        reset_btn = gr.Button("Reset Plot")  # AI CHANGE

    with gr.Accordion("Output", open=True):  # AI CHANGE
        output_tb = gr.Textbox(label="Sorted Array", placeholder="Result after sort", interactive=False, lines=3)  # AI CHANGE
        with gr.Row():
            states_tb = gr.TextArea(lines=12, label="Steps", placeholder="Sort steps stream here", interactive=False, elem_classes="large-text", scale=1)  # AI CHANGE
            plot = gr.BarPlot(x='x', y='y', color="highlighted", color_map={'not comparing': 'orange', 'comparing': 'green', 'sorted' : 'gray'}, title="Current Array State", scale=2)  # AI CHANGE


    # Mode switching (mutually exclusive visibility)
    mode_radio.change(fn=switch_mode, inputs=mode_radio, outputs=[input_tb, newlist, size, min_val, max_val, gen_random])  # AI CHANGE

    # Data input events
    newlist.click(fn=main.custom_list, inputs=input_tb, outputs=[output_tb, ret_list])  # AI CHANGE
    gen_random.click(fn=main.gen_random_array, inputs=[size, min_val, max_val], outputs=[output_tb, ret_list])  # AI CHANGE

    # Sorting
    sort.click(fn=main.bubble_sort, inputs=[ret_list], outputs=[output_tb, steps_state])  # AI CHANGE
    
    # Animation
    animate_event = (
        display.click(fn=lambda: gr.Accordion(open=False), outputs=input_accordion)
        .then(fn=fixer.reset_plot, outputs=plot)
        .then(fn=fixer.show_plot, outputs=plot)
        .then(fn=main.print_states, inputs=[steps_state, speed_slider], outputs=[states_tb, plot])
    )  # AI CHANGE

    # Manual plot reset now cancels running animation generator
    reset_btn.click(fn=fixer.reset_plot, outputs=plot, cancels=[animate_event]).then(fn=fixer.show_plot, outputs=plot)  # AI CHANGE: proper cancellation reference

if __name__ == "__main__":
    demo.queue().launch()