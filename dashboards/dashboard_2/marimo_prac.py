import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt


    return alt, mo, pd


@app.cell
def _(dropdown_country, dropdown_cylinder, dropdown_name, mo):
    # Create the fixed sidebar
    my_sidebar = mo.sidebar(
        mo.vstack([
            mo.md("### ⚙️ Dashboard Controls"),
            dropdown_country,
            dropdown_name, 
            dropdown_cylinder
        ])
    )

    # Display it
    my_sidebar
    return


@app.cell
def _(pd):
    df = pd.read_json("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/cars.json")
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df, mo):
    dropdown_country = mo.ui.dropdown(
        options=list(df['Origin'].unique()),
        value='USA',
        label="Select Region"
    )

    return (dropdown_country,)


@app.cell
def _():
    #dropdown_name = mo.ui.dropdown(
     #   options=list(df['Name'].unique()),
      #  value='audi fox',
       # label="Select model"
    #)

    return


@app.cell
def _():
    return


@app.cell
def _(df, dropdown_country, dropdown_cylinder, dropdown_name):
    filtered_df= df[
        (df['Origin']==dropdown_country.value) & 
        (df['Name']==dropdown_name.value) & 
        (df['Cylinders']==dropdown_cylinder.value)
    ]
    return (filtered_df,)


@app.cell
def _(df, dropdown_country):
    regional_cars = df[df['Origin'] == dropdown_country.value]
    return (regional_cars,)


@app.cell
def _(dropdown_name, regional_cars):
    model_cars = regional_cars[regional_cars['Name'] == dropdown_name.value]
    return (model_cars,)


@app.cell
def _(mo, regional_cars):
    dropdown_name = mo.ui.dropdown(
        options=list(regional_cars['Name'].unique()),
        # We set the default value to the first car in the new list
        value=list(regional_cars['Name'].unique())[0], 
        label="Select model"
    )
    return (dropdown_name,)


@app.cell
def _(mo, model_cars):
    dropdown_cylinder = mo.ui.dropdown(
        options=(model_cars['Cylinders'].unique()).tolist(),
        value=(model_cars['Cylinders'].unique())[0].tolist(),
        label="Number of Cylinders"
    )
    return (dropdown_cylinder,)


@app.cell
def _(alt, filtered_df):
    car_chart = (
        alt.Chart(filtered_df)
        .mark_circle(size=100)
        .encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin'
        )
    )
    car_chart
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
