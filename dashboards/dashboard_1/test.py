import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    print("Hello, world!")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import random

    # Create some fake data for the dashboard
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'A', 'B', 'C'] * 10,
        'Value': [random.randint(10, 100) for _ in range(60)],
        'Year': [2023, 2024] * 30
    })
    return data, mo


@app.cell
def _(mo):
    x = mo.ui.slider(1,9)
    x
    return


@app.cell
def _(mo):
    # Create a dropdown to select a category
    category_selector = mo.ui.dropdown(
        options=['A', 'B', 'C'], 
        value='A', 
        label="Choose Category"
    )
    category_selector


    return (category_selector,)


@app.cell
def _(mo):
    # Create a slider for filtering values
    value_slider = mo.ui.slider(
        start=0, 
        stop=100, 
        value=10, 
        label="Minimum Value"
    )
    value_slider
    return (value_slider,)


@app.cell
def _(category_selector, data, value_slider):
    # This cell runs automatically when you change the widgets
    filtered_df = data[
        (data['Category'] == category_selector.value) & 
        (data['Value'] >= value_slider.value)
    ]
    filtered_df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
