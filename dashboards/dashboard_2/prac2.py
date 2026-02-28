# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair>=6.0.0",
#     "marimo>=0.19.10",
#     "pandas>=3.0.1",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt

    alt.data_transformers.disable_max_rows()
    return alt, mo, pd


@app.cell
def _(cars):
    # 1. Import Plotly (Marimo usually has this pre-installed, or you might need to pip install plotly)
    import plotly.express as px

    # 2. Create the 3D Scatter Plot
    fig_3d = px.scatter_3d(
        cars, # We use the same 'cars' dataset!
        x='Horsepower',
        y='Weight_in_lbs',
        z='Miles_per_Gallon',
        color='Origin',
        title="3D View: Power vs. Weight vs. Efficiency"
    )

    # 3. Just type the variable name to display it in Marimo
    fig_3d
    return (px,)


@app.cell
def _(cars, px):

    fig_bubble = px.scatter_3d(
        cars, x='Horsepower', y='Weight_in_lbs', z='Miles_per_Gallon',
        color='Origin', 
        size='Displacement', # This turns it into a bubble chart!
        size_max=18
    )
    fig_bubble
    return


@app.cell
def _():
    import plotly.graph_objects as go
    import numpy as np

    # 1. Create a grid of X and Y coordinates (from -5 to 5)
    x_values = np.linspace(-5, 5, 50)
    y_values = np.linspace(-5, 5, 50)
    x_grid, y_grid = np.meshgrid(x_values, y_values)

    # 2. Create the missing 'my_z_matrix' using a math formula
    my_z_matrix = np.sin(np.sqrt(x_grid**2 + y_grid**2))

    # 3. Draw the Surface
    fig_surface = go.Figure(data=[go.Surface(z=my_z_matrix, x=x_values, y=y_values)])
    fig_surface.update_layout(title="Mathematical 3D Surface")

    fig_surface
    return


@app.cell
def _(cars, px):

    # 1. Create the missing variable: filter for Ford and sort by Year
    # We use .str.contains() to find any name that includes 'ford'
    ford_cars = cars[cars['Name'].str.contains('ford', case=False, na=False)]
    ford_cars_sorted_by_year = ford_cars.sort_values(by='Year')

    # 2. Draw the 3D Line
    fig_line = px.line_3d(
        ford_cars_sorted_by_year, 
        x='Horsepower', 
        y='Weight_in_lbs', 
        z='Miles_per_Gallon',
        color='Name',
        title="3D Trajectory of Ford Cars Over Time"
    )

    fig_line
    return


@app.cell
def _(pd):
    url = "https://raw.githubusercontent.com/vega/vega-datasets/master/data/flights-200k.json"
    df = pd.read_json(url)
    df
    return


@app.cell
def _(pd):
    cars = pd.read_json("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/cars.json")

    # Look at the first 5 rows
    cars.head()
    return (cars,)


@app.cell
def _(cars):
    cars.shape
    return


@app.cell
def _(cars):
    cars.describe()
    return


@app.cell
def _(alt, cars):
    professional_chart = alt.Chart(cars).mark_circle().encode(

        # 1. Position Encodings
        x='Horsepower',
        y='Miles_per_Gallon',

        # 2. Detail Encodings
        color='Origin',                  # Different colors for USA, Europe, Japan
        size='Cylinders',                # Bigger circles for more cylinders

        # 3. Interactive Encoding
        opacity='Weight_in_lbs', 
        tooltip=['Name', 'Horsepower', 'Weight_in_lbs']  # Shows text when you hover with the mouse!
    )

    # Show the chart
    professional_chart
    return


@app.cell
def _(alt, cars):
    # A professional summary chart
    summary_chart = alt.Chart(cars).mark_bar().encode(
        # X-axis shows the categories
        x='Origin',
        # Y-axis calculates the average automatically!
        y='mean(Horsepower)',
        # Color makes it easy to distinguish
        color='Origin',
        tooltip=['Origin', 'mean(Horsepower)']
    )

    summary_chart
    return


@app.cell
def _(alt, cars):
    # Trend of Miles per Gallon over the years
    line_chart = alt.Chart(cars).mark_line(point=True).encode(
        x='Year:T',  # :T tells Altair this is Time data
        y='mean(Miles_per_Gallon)',
        color='Origin'
    )
    line_chart
    return


@app.cell
def _(alt, cars):
    # Cumulative Horsepower by Region over time
    area_chart = alt.Chart(cars).mark_area().encode(
        x='Year:T',
        y='mean(Miles_per_Gallon)',
        color='Origin'
    )
    area_chart
    return


@app.cell
def _():
    return


@app.cell
def _(alt, cars):
    #now i will create dynamic charts using altair's interactive features
    # Create a dropdown menu for selecting the origin
    dropdown = alt.binding_select(options=cars['Origin'].unique().tolist(), name='Select Origin: ')
    selection = alt.selection_single(fields=['Origin'], bind=dropdown)  
    # Create a chart that updates based on the dropdown selection
    interactive_chart = alt.Chart(cars).mark_circle().encode(
        x='Horsepower',
        y='Miles_per_Gallon',
        color='Origin',
        tooltip=['Name', 'Horsepower', 'Miles_per_Gallon']
    ).add_selection(selection).transform_filter(selection)
    interactive_chart   
    return


@app.cell
def _(alt, cars):
    # Concentration of car types
    heatmap = alt.Chart(cars).mark_rect().encode(
        x='Cylinders:O', # :O tells Altair this is Ordinal (ranked numbers)
        y='Origin:N',    # :N tells Altair this is Nominal (names/categories)
        color='count()'
    )
    heatmap
    return


@app.cell
def _(alt, cars):
    # Spread of Horsepower by Origin
    box_plot = alt.Chart(cars).mark_boxplot().encode(
        x='Origin',
        y='Horsepower'
    )
    box_plot
    return


@app.cell
def _(points):
    points
    return


@app.cell
def _(alt, cars):
    # 1. Create the points (individual cars)
    points = alt.Chart(cars).mark_circle(opacity=0.4).encode(
        x='Year:T',
        y='Weight_in_lbs:Q',
        color='Origin:N',
        tooltip=['Name', 'Horsepower', 'Weight_in_lbs']
    )

    # 2. Create the line (the average trend)
    average_line = alt.Chart(cars).mark_line(size=4).encode(
        x='Year:T',
        y='mean(Weight_in_lbs):Q',
        color='Origin:N'
    )

    # 3. Layer them together!
    layered_chart = points + average_line

    layered_chart.properties(width=600, title="Car Weight Trends: Individual vs. Average")
    return (points,)


@app.cell
def _(alt, cars):
    histogram = alt.Chart(cars).mark_bar().encode(
        # 'bin=True' groups the numbers into ranges automatically
        x=alt.X('Horsepower:Q', bin=True),
        # 'count()' tells us how many cars are in each range
        y='count()',
        # Coloring by Origin shows the distribution for each region
        color='Origin:N'
    )

    histogram.properties(title="Distribution of Horsepower across Regions")
    return


@app.cell
def _(alt, cars):
    # STEP 1: Define the 'Radio' (Choose a column to click on)
    picker = alt.selection_point(fields=['Origin']) 

    # STEP 2: The Chart
    my_test_chart = alt.Chart(cars).mark_bar().encode(
        x='Origin',
        y='count()',
        # STEP 3: The 'Condition' (If picked, show color. If not, show lightgray)
        color=alt.condition(picker, 'Origin', alt.value('lightgray'))
    ).add_params(
        picker # Put the 'Radio' variable name here
    )

    my_test_chart
    return (picker,)


@app.cell
def _(alt, cars, picker):
    # This is the chart you just built!
    bars = alt.Chart(cars).mark_bar().encode(
        x='Origin',
        y='count()',
        color=alt.condition(picker, 'Origin', alt.value('lightgray'))
    ).add_params(picker)

    # This is a NEW chart that 'listens' to the picker
    scatter = alt.Chart(cars).mark_circle().encode(
        x='Horsepower',
        y='Miles_per_Gallon',
        color='Origin',
        tooltip='Name'
    ).transform_filter(
        picker # <--- This is the magic listener!
    )

    # Put them side-by-side
    bars | scatter
    return


@app.cell
def _(mo):
    name_input = mo.ui.text(label="Enter your name:")
    name_input
    return (name_input,)


@app.cell
def _(name_input):
    # This cell 'watches' Cell 1. 
    # It will run automatically the moment you type!
    greeting = f"Hello, {name_input.value}! Welcome to Marimo."
    return (greeting,)


@app.cell
def _(greeting, mo):
    mo.md(f"""
    ## {greeting}
    """)
    return


@app.cell
def _(mo):
    # A simple slider to choose a horsepower threshold
    hp_limit = mo.ui.slider(start=50, stop=250, step=10, label="Min Horsepower:")
    hp_limit
    return (hp_limit,)


@app.cell
def _(cars, hp_limit):
    # This cell automatically filters the data whenever the slider moves
    high_power_cars = cars[cars['Horsepower'] >= hp_limit.value]
    return (high_power_cars,)


@app.cell
def _(high_power_cars, hp_limit, mo):
    # This cell automatically redraws the count whenever the filtering changes
    mo.md(f"### There are **{len(high_power_cars)}** cars with at least {hp_limit.value} HP.")
    return


@app.cell
def _(mo):
    # Create both sliders together
    hp_slider = mo.ui.slider(start=40, stop=230, value=100, label="Min HP")
    weight_slider = mo.ui.slider(start=1600, stop=5200, value=3000, label="Max Weight")

    # Display them side-by-side
    mo.hstack([hp_slider, weight_slider])
    return hp_slider, weight_slider


@app.cell
def _(cars, hp_slider, weight_slider):
    # Our engine - it updates every time you move the slider
    # It filters the original 'cars' data
    filtered_data = cars[
        (cars['Horsepower'] >= hp_slider.value) & 
        (cars['Weight_in_lbs'] >= weight_slider.value)]
    return (filtered_data,)


@app.cell
def _(alt, filtered_data):
    # Our output - it draws whatever is inside 'filtered_data'
    chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color='Origin:N',
        tooltip=['Name','Horsepower', 'Weight_in_lbs']
    ).properties(width=500, height=300)

    chart
    return (chart,)


@app.cell
def _(filtered_data, mo):
    mo.md(f"""
    ### There are **{len(filtered_data)}**
    """)
    return


@app.cell
def _(chart, filtered_data, hp_slider, mo, weight_slider):
    # Create a nice layout
    dashboard_view = mo.vstack([
        mo.md("# 🏎️ Car Performance Explorer"),

        # Put sliders and counter side-by-side
        mo.hstack([
            hp_slider, 
            weight_slider, 
            mo.stat(value=len(filtered_data), label="Cars Found", caption="matching your filters")
        ], justify="start", align="center"),

        # Show the chart
        chart
    ])

    dashboard_view
    return


@app.cell
def _(chart, mo):
    mo.vstack([
        mo.stat("# Top Title", bordered=True),
        mo.stat("Middle Description", bordered=True),
        chart
    ])
    return


@app.cell
def _(mo):
    slider_one = mo.ui.slider(1, 100)
    slider_one
    return (slider_one,)


@app.cell
def _(mo):
    slider_two = mo.ui.slider(10, 200, 20)
    slider_two
    return (slider_two,)


@app.cell
def _(mo):
    dropdown_menu = mo.ui.dropdown(options=["a", "b", "c"], value="a", label="choose one")
    return (dropdown_menu,)


@app.cell
def _(dropdown_menu, mo, slider_one, slider_two):
    mo.hstack([
        slider_one,
        slider_two,
        dropdown_menu
    ])
    return


@app.cell
def _(chart, filtered_data, hp_slider, mo, weight_slider):
    # Create the dashboard layout
    my_dashboard = mo.vstack([
        # 1. The Header (Top Floor)
        mo.md("# 🏎️ Car Data Explorer"),

        # 2. The Control Bar (Middle Floor - Rooms side-by-side)
        mo.hstack([
            hp_slider, 
            weight_slider,
            # A nice 'Stat' box for your counter
            mo.stat(value=len(filtered_data), label="Cars Matched")
        ], justify="start", align="center", gap=1), # 'gap' adds nice space between them

        # 3. The Main Chart (Bottom Floor)
        chart
    ])

    # Display the whole thing
    my_dashboard
    return


@app.cell
def _(chart, filtered_data, hp_slider, mo, weight_slider):
    # Create the 'Stat' widget
    car_counter = mo.stat(
        value=str(len(filtered_data)), 
        label="Total Cars", 
        caption="matching filters",
        bordered=True
    )

    # Put it in your dashboard
    dashboard = mo.vstack([
        mo.md("# 🏎️ Car Finder"),
        mo.hstack([
            hp_slider, 
            weight_slider, 
            car_counter
        ], justify="start", align="center"),
        chart
    ])

    dashboard
    return (car_counter,)


@app.cell
def _(car_counter, chart, filtered_data, hp_slider, mo, weight_slider):


    # Using our 'Hover' fix from before
    hover_stat = mo.Html(f'<div title="This updates live with the sliders!">{car_counter}</div>')

    # 2. Build the Layout using Nesting
    # We use vstack for the floors, hstack for the rooms
    professional_app = mo.vstack([
        # Floor 1: Title and context
        mo.md("# 🏎️ Car Market Intelligence Tool"),
        mo.md("Adjust the filters below to find cars that meet specific performance criteria."),

        # Floor 2: The Control Bar (Horizontal)
        mo.hstack([
            hp_slider, 
            weight_slider, 
            hover_stat
        ], justify="start", align="center", gap=2),

        # Floor 3: The Visualization (The "Story")
        mo.md("### Horsepower vs. Fuel Efficiency"),
        chart,

        # Floor 4: The Details (The "Raw Data")
        mo.md("---"),
        mo.md("### Inventory Details"),
        mo.ui.table(filtered_data, pagination=True)
    ])

    # 3. Final display
    professional_app
    return


@app.cell
def _(alt, filtered_data):
    # 1. The original scatter plot (the dots)
    points2 = alt.Chart(filtered_data).mark_circle(size=100).encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color='Origin:N',
        tooltip=['Name', 'Horsepower']
    )

    # 2. The Regression Line (The "Prediction")
    # .transform_regression calculates the line automatically!
    regression_line = points2.transform_regression(
        'Horsepower', 'Miles_per_Gallon'
    ).mark_line(color='black', size=3)

    # 3. Layer them
    # The '+' symbol puts the line on top of the dots
    final_chart = points2 + regression_line

    final_chart
    return


@app.cell
def _():
    return


@app.cell
def _():
    # Create a fixed left menu
    #my_sidebar = mo.sidebar(
     #   mo.vstack([
      #      mo.md("### ⚙️ Dashboard Menu"),
       #     mo.md("---"),
        #    mo.md("[📊 Main Chart](#)"),
         #   mo.md("[📋 Data Table](#)"),
          #  mo.md("[👥 Project Team](#)")
        #])
    #)

    # You just display it, and Marimo automatically pins it to the left!
    #my_sidebar
    return


@app.cell
def _(mo):
    # A professional team credits section
    team_credits = mo.md(
        f"""
        ---
        ### 👥 Project Team
        **Dashboard and Analysis:** Muratbek Nurmatov  <br>
        **Analysis:** [Member Name]  <br>
        **Conclusion:** [Member Name]  <br>
        **Review:** [Member Name]<br>
        **Text:** [Member Name]<br>

        *Developed by students of Management & Data Science Program at Leuphana University.*

        *Course: Applied statistical data analysis*
        """
    ).style(textAlign="center", padding="20px", borderRadius="10px")
    team_credits
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
