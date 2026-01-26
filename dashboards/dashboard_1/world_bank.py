import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## World Bank Project
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy.stats as stats
    # Import libraries for running ANOVA and post-hoc test
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    from statsmodels.stats.anova import anova_lm
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    return mo, np, ols, pairwise_tukeyhsd, pd, plt, sm, sns, stats


@app.cell
def _(pd):
    df1=pd.read_csv("../../additional_material/datasets/week5/world_bank_development_indicators.csv")
    df2=pd.read_excel("../../additional_material/datasets/week5/income.xlsx")
    df = pd.merge(df1, df2, left_on='country', right_on='Economy', how="inner")
    return (df,)


@app.cell
def _(df):
    print(df.duplicated().sum())
    return


@app.cell
def _(df):
    print(df.isnull().sum())
    return


@app.cell
def _(df):
    print(df.head())
    return


@app.cell
def _(df):
    # columns in the dataset 
    print("Columns in the dataset:")
    for col in df.columns:
        print(col)
    return


@app.cell
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(df):
    # unique and number of unique values in country and Income group column and years
    print("Number of Unique countries:", df['country'].nunique())
    print("Number of Unique Years:", df['date'].nunique())
    print("Number of  Unique Groups:", df['Income group'].nunique())
    print("Countries:", df['country'].unique())
    print("Groups:", df['Income group'].unique())
    print("Years:", df['date'].unique())
    return


@app.cell
def _(df):
    print(df['Region'].value_counts())
    return


@app.cell
def _(df):
    # Map World Bank regions to continents
    region_to_continent = {
        'Europe & Central Asia': 'Europe',
        'Sub-Saharan Africa': 'Africa',
        'Latin America & Caribbean': 'South America',
        'East Asia & Pacific': 'Asia',
        'Middle East, North Africa, Afghanistan & Pakistan': 'Asia',
        'South Asia': 'Asia',
        'North America': 'North America'
    }

    df['continent'] = df['Region'].map(region_to_continent)
    return


@app.cell
def _(df):
    print(df['continent'].unique())
    print(df['continent'].value_counts())
    return


@app.cell
def _(df):
    # countries names in country column edited to remove leading and trailing spaces
    df['country'] = df['country'].str.strip()
    return


@app.cell
def _(df):
    print(df['country'].unique())
    return


@app.cell
def _(df, np):
    # rename dictionary for standardizing country names
    rename_dict = {
        'Swaziland': 'Eswatini',
        'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
        'Congo, Rep.': 'Republic of the Congo',
        'Russian Federation': 'Russia',
        'Syrian Arab Republic': 'Syria',
        'Iran, Islamic Rep.': 'Iran',
        'Egypt, Arab Rep.': 'Egypt',
        'Bahamas, The': 'Bahamas',
        'Gambia, The': 'Gambia',
        'Venezuela, RB': 'Venezuela',
        "Korea, Dem. People's Rep.": 'North Korea',
        "Korea, Rep.": 'South Korea',
        "Hong Kong SAR, China": 'Hong Kong',
        "Macao SAR, China": 'Macau',
        "Sint Maarten (Dutch part)": 'Sint Maarten',
        "Virgin Islands (U.S.)": 'U.S. Virgin Islands',
        "Lao PDR": 'Laos',
        "Brunei Darussalam": 'Brunei',
        "Slovak Republic": 'Slovakia',
        "Kyrgyz Republic": 'Kyrgyzstan',
        "Micronesia, Fed. Sts.": 'Micronesia',
        "Yemen, Rep.": 'Yemen',
        "St. Kitts and Nevis": "Saint Kitts and Nevis",
        "St. Lucia": "Saint Lucia",
        "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
        "St. Martin (French part)": np.nan,
    }

    # exclude keywords list for filtering out non-country entries
    exclude_keywords = [
        'income', 'ida', 'ibrd', 'small states', 'world', 'euro area', 'oecd',
        'demographic dividend', 'fragile', 'post-', 'pre-', 'early-', 'late-',
        'sub-saharan africa', 'east asia & pacific', 'latin america & caribbean',
        'north america', 'africa eastern', 'africa western',
        'central europe and the baltics', 'europe & central asia',
        'middle east & north africa', 'high income', 'low income',
        'upper middle income', 'lower middle income'
    ]

    non_countries = [
        # Territories / Dependencies
         'American Samoa', 'Aruba', 'Bermuda', 'British Virgin Islands',
        'Cayman Islands', 'Channel Islands', 'Faroe Islands', 'French Polynesia',
        'Gibraltar', 'Greenland', 'Guam', 'Isle of Man', 'Monaco',
        'New Caledonia', 'Northern Mariana Islands', 'Turks and Caicos Islands',
        'U.S. Virgin Islands',

        # Regions (World Bank aggregates)
        'World', 'European Union', 'Arab World', 'South Asia',
        'Middle East & North Africa',
        'Heavily indebted poor countries (HIPC)',
        'Least developed countries: UN classification',
        'Caribbean small states', 'Pacific island small states',
        'IDA & IBRD total', 'IDA total', 'IBRD only'
    ]

    def clean_country(name):
        if not isinstance(name, str):
            return np.nan
        for word in exclude_keywords:
            if word.lower() in name.lower():
                return np.nan
        if name in non_countries:
            return np.nan
        return rename_dict.get(name, name)

    df['country_clean'] = df['country'].apply(clean_country)

    print(df['country_clean'].unique())
    return


@app.cell
def _(df):
    # rename the cleaned country column to country and drop the old country column as well as region column
    df['country'] = df['country_clean']
    df.drop(columns=['country_clean'],inplace=True)
    df.drop(columns=['Region'],inplace=True)
    print(df['country'].unique())
    return


@app.cell
def _(df):
    df['Income group'] = (df['Income group'].str.replace(' income', '').str.replace(' ', '_'))
    return


@app.cell
def _(df):
    # Edit columns names 
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    #change % in column names to _percent
    df.columns = [col.replace('%', '_percent') for col in df.columns]
    print(df.columns)
    return


@app.cell
def _(df, pd):
    # edit the data types of date column, income_group column and continent column
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Convert 'income_group' and 'continent' to categorical
    df['income_group'] = df['income_group'].astype('category')
    df['continent'] = df['continent'].astype('category')

    # Check the data types
    print(df.dtypes)
    return


@app.cell
def _(df, np):
    #we need to have independent samples for ANOVA test so we should have one entry per country
    # Filter years 2015–2019 
    df_filtered = df[(df['date'].dt.year >= 2015) & (df['date'].dt.year <= 2019)]

    #Separate numeric and non-numeric columns 
    numeric_col = df_filtered.select_dtypes(include=np.number).columns.tolist()
    non_numeric_cols = df_filtered.select_dtypes(exclude=np.number).columns.tolist()
    non_numeric_cols = [col for col in non_numeric_cols if col != 'country']

    # Function to take mode (most frequent value) we will use it for non numerical columns
    def mode_or_first(series):
        m = series.mode()
        if not m.empty:
            return m[0]
        else:
            return series.iloc[0]  # fallback if all missing

    #Group by country and aggregate
    # numeric → mean
    agg_dict = {col: 'mean' for col in numeric_col}
    # categorical → mode
    agg_dict.update({col: mode_or_first for col in non_numeric_cols})

    df_filtered = df_filtered.groupby('country', as_index=False).agg(agg_dict)

    print(df_filtered.head())
    return (df_filtered,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Missing Values after cleaning
    """)
    return


@app.cell
def _(mo):
    min_missing_pct = mo.ui.slider(
        start=0,
        stop=24,
        step=5,
        value=0,
        label="Minimum missing percentage"
    )

    min_missing_pct
    return (min_missing_pct,)


@app.cell
def _(df_filtered, min_missing_pct, pd):
    missing_df = pd.DataFrame({
        "Missing Count": df_filtered.isnull().sum(),
        "Missing %": df_filtered.isnull().mean() * 100,
    })

    missing_report = (
        missing_df[missing_df["Missing %"] >= min_missing_pct.value]
        .round(2)
        .sort_values("Missing %", ascending=False)
    )

    missing_report
    return


@app.cell
def _(df_filtered):
    # columns to drop
    cols_to_drop = [
        #missing value >30%
        'electric_power_consumption',                       #99%
        'multidimensional_poverty_headcount_ratio_percent', #77%
        'risk_premium_on_lending',                          #71%
        'time_to_get_operation_license',                    #70%
        'central_goverment_debt_percent',                   #68%
        'gini_index',                                       #50
        'real_interest_rate',                               #48%
        'research_and_development_expenditure_percent'  ,   #45%
        'lending_category',                                 #44%
        'human_capital_index',                              #36%
        'expense_percent',                                  #36%
        'tax_revenue_percent',                              #34%
        'avg_precipitation',                                #31%  

        # irrelevant Indicators
        'date',
        'population_density',
        'rural_population',
        'regulatory_quality_estimate',
        'logistic_performance_index', 
        'other_greenhouse_emisions', 
        'military_expenditure_percent', 
        'code', 
        'statistical_performance_indicators',

        #std columns
        'voice_and_accountability_std',
        'political_stability_std',
        'rule_of_law_std',
        'regulatory_quality_std',
        'goverment_effectiveness_std',
        'control_of_corruption_std',

        #redundant columns
        'economy',  # duplicate of country
        'land_area',
        'birth_rate',# have high correlation with life_expectancy_at_birth                
        'death_rate',# have high correlation with life_expectancy_at_birth
    ]
    df_filtered.drop(columns=cols_to_drop,inplace=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Descriptive statistics
    """)
    return


@app.cell
def _(df_filtered, mo):
    numeric_cols = df_filtered.select_dtypes(include="number").columns.tolist()

    selected_cols = mo.ui.multiselect(
        options=numeric_cols,
        value=numeric_cols[:-1],
        label="Select numeric columns"
    )

    selected_cols
    return (selected_cols,)


@app.cell
def _(df_filtered, selected_cols):
    df_filtered[selected_cols.value].describe().round(2)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Dependent Variables Distribution
    """)
    return


@app.cell
def _(mo):
    group_cols = ["income_group", "continent"]

    selected_group = mo.ui.dropdown(
        options=group_cols,
        value="income_group",
        label="Group countries by"
    )

    selected_group
    return (selected_group,)


@app.cell
def _(df_filtered, selected_group):
    group_counts = df_filtered[selected_group.value].value_counts()
    group_counts
    return (group_counts,)


@app.cell
def _(group_counts, plt, selected_group, sns):
    sns.set_style("whitegrid")
    palette = sns.color_palette("Set3")

    fig = plt.figure(figsize=(7, 5))
    sns.barplot(
        x=group_counts.index,
        y=group_counts.values,
        palette=palette
    )

    plt.title(f"Number of Countries by {selected_group.value.replace('_', ' ').title()}")
    plt.xlabel(selected_group.value.replace("_", " ").title())
    plt.ylabel("Number of Countries")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Research Question 1: Does CO2 emission per capita differ across income groups?
    Variables:

    DV (dependent variable) → co2_emissions

    IV (independent variable / factor) → income_group
    """)
    return


@app.cell
def _(df_filtered):
    df_co2 = df_filtered[['country', 'income_group', 'co2_emisions','population']].copy()
    return (df_co2,)


@app.cell
def _(df_co2):
    print(df_co2['co2_emisions'].isna().sum())
    #Impute missing values by the mean of their income group
    df_co2['co2_emisions'] = df_co2.groupby('income_group')['co2_emisions'].transform(
        lambda x: x.fillna(x.mean())
    )
    #Verify no missing values remain
    print(df_co2['co2_emisions'].isna().sum())
    return


@app.cell
def _(df_co2):
    df_co2.dropna(subset=['co2_emisions'],inplace=True)
    print(df_co2['co2_emisions'].isna().sum())
    return


@app.cell
def _(df_co2):
    print(df_co2['income_group'].value_counts())
    return


@app.cell
def _(df_co2, np):
    df_co2['co2_emisions_log']=np.log(df_co2['co2_emisions']+1)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Normality of the Dependent Variable
    """)
    return


@app.cell
def _(mo):

    plot_options = ["Histogram", "Q-Q Plot"]

    selected_plot = mo.ui.dropdown(
        options=plot_options,
        value="Histogram",
        label="Select the plot to display"
    )

    selected_plot
    return (selected_plot,)


@app.cell
def _(df_co2, plt, selected_plot, sns, stats):
    sns.set_style("whitegrid")

    # Start figure
    fig2 = plt.figure(figsize=(7, 5))

    if selected_plot.value == "Histogram":
        sns.histplot(df_co2['co2_emisions_log'], kde=True, bins=30, color='skyblue')
        plt.title('Distribution of CO2 Emissions (log)')
        plt.xlabel('CO₂ emissions (log)')
        plt.ylabel('Frequency')

    elif selected_plot.value == "Q-Q Plot":
        osm, osr = stats.probplot(df_co2['co2_emisions_log'])[0]
        slope, intercept, *_ = stats.linregress(osm, osr)
        plt.scatter(osm, osr, color='blue')
        plt.plot(osm, intercept + slope*osm, color='red', lw=2)
        plt.title('Q-Q Plot of CO₂ Emissions (log)')
        plt.xlabel('Theoretical Quantiles')
        plt.ylabel('Ordered Values')

    plt.tight_layout()
    fig2  # last line so Marimo renders it
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Variance of the Dependent Variable
    """)
    return


@app.cell
def _(mo):
    # List of income groups
    income_groups = ['Low', 'Lower_middle', 'Upper_middle', 'High']

    # Let the user select which groups to display
    selected_groups = mo.ui.multiselect(
        options=income_groups,
        value=income_groups,  # default: show all
        label="Select income groups to display"
    )

    selected_groups

    return income_groups, selected_groups


@app.cell
def _(df_co2, income_groups, plt, selected_groups, sns):
    sns.set_style("whitegrid")
    fig3 = plt.figure(figsize=(10,6))


    df_plot = df_co2[df_co2['income_group'].isin(selected_groups.value)]

    ordered_groups = [g for g in income_groups if g in selected_groups.value]

    sns.boxplot(
        x='income_group',
        y='co2_emisions_log',
        data=df_plot,
        order=ordered_groups,  
        palette='Set2'
    )

    plt.title('CO₂ Emissions (Log) by Income Group')
    plt.xlabel('Income Group')
    plt.ylabel('CO₂ Emissions (Log)')
    plt.tight_layout()

    fig3  
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Anova
    """)
    return


@app.cell
def _(df_co2, ols, sm):
    # Fit ANOVA model
    model = ols('co2_emisions_log ~ C(income_group)', data=df_co2).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    print("ANOVA Table:")
    print(anova_table)
    return anova_table, model


@app.cell
def _(model, plt, sns):
    sns.set_style("whitegrid")
    fig4 = plt.figure(figsize=(8, 5))

    residuals = model.resid  # your residuals

    sns.histplot(residuals, bins=30, kde=True, color='skyblue')
    plt.title('Histogram of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.tight_layout()

    fig4  # last line → renders in Marimo View mode
    return


@app.cell
def _(anova_table):
    # Extract the sum of squares for the model (all rows except 'Residual')
    SS_model = anova_table.loc[anova_table.index != 'Residual', 'sum_sq'].sum()
    # Extract sum of squares for the residual
    SS_residual = anova_table.loc['Residual', 'sum_sq']
    # Total sum of squares
    SS_total = SS_model + SS_residual

    # Explained variance (eta-squared)
    explained_variance = SS_model / SS_total

    print(f'Explained Variance (η²): {explained_variance:.3f}')
    return


@app.cell
def _(mo):
    income_groups_order = ['Low', 'Lower_middle', 'Upper_middle', 'High']

    selected_groupss = mo.ui.multiselect(
        options=income_groups_order,
        value=income_groups_order,
        label="Select income groups to include in Tukey HSD test"
    )

    selected_groupss
    return (selected_groupss,)


@app.cell
def _(df_co2, pairwise_tukeyhsd, pd, selected_groupss):
    # Filter dataframe based on selected groups
    df_plot2 = df_co2[df_co2['income_group'].isin(selected_groupss.value)]

    # Tukey HSD test
    tukey = pairwise_tukeyhsd(
        endog=df_plot2['co2_emisions_log'],
        groups=df_plot2['income_group'],
        alpha=0.05
    )

    def color_significant(val):
        return 'background-color: yellow' if val=='True' else ''


    # Convert results to dataframe for clean display
    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    tukey_df
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Conclusion to Research Question 1
    Income group has a very strong effect on CO₂ emissions,and here is the results

    High-income countries emit significantly more CO₂ per capita than Low and Lower-Middle income countries.
    Upper-Middle income countries emit significantly more than Low-income countries.
    Income groups in the middle (Low ↔ Lower-Middle ↔ Upper-Middle) do NOT differ much.
    Upper-Middle countries are surprisingly close to High-income countries (no significant difference).
    """)
    return


@app.cell
def _(pd):
    import altair as alt

    life_df = pd.read_csv("Human-well-being-health.csv")

    return alt, life_df


@app.cell
def _(life_df):
    lean_df = life_df.dropna(subset=[
        'government_health_expenditure_percent', 
        'life_expectancy_at_birth',
        'continent',
        'income_group'
    ])
    return (lean_df,)


@app.cell
def _():
    #lean_df.isnull().sum()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Research Question 2: To what extent does a country's income classification significantly influence key development indicators, such as life expectancy and health expenditure?
    """)
    return


@app.cell
def _(alt, lean_df):

    # 1. Create a "selection" tool
    # This tells Altair to listen for clicks based on the 'continent' field
    click_selection = alt.selection_multi(fields=['continent'])

    # 2. The Scatter Plot (The Main View)
    scatter2 = alt.Chart(lean_df).mark_circle(size=60).encode(
        x=alt.X('government_health_expenditure_percent', title='Health Expenditure (%)'),
        y=alt.Y('life_expectancy_at_birth', scale=alt.Scale(domain=[50, 90]), title='Life Expectancy'),
    
        # The Magic Trick:
        # If a point is selected, color it by continent.
        # If NOT selected, turn it gray.
        color=alt.condition(click_selection, 'continent', alt.value('lightgray')),
        tooltip=['country', 'life_expectancy_at_birth']
    ).properties(
        width=400,
        title="Health vs Life Expectancy"
    )

    # 3. The Bar Chart (The Filter)
    bars2 = alt.Chart(lean_df).mark_bar().encode(
        x='count()',
        y='continent',
        color=alt.condition(click_selection, 'continent', alt.value('lightgray'))
    ).add_selection(
        click_selection # <--- We attach the click tool to this chart
    ).properties(
        width=200,
        title="Click a bar to filter"
    )

    # 4. Combine them side-by-side using the '|' symbol
    scatter2 | bars2
    return


@app.cell
def _(alt, lean_df):

    # 1. Create the "brush" tool
    # "interval" means we are selecting a range (an area), not just a single point
    brush = alt.selection_interval()

    # 2. The Scatter Plot (Where you draw the box)
    scatter = alt.Chart(lean_df).mark_circle(size=60).encode(
        x=alt.X('government_health_expenditure_percent', title='Health Expenditure (%)'),
        y=alt.Y('life_expectancy_at_birth', scale=alt.Scale(domain=[50, 90]), title='Life Expectancy'),
        color=alt.condition(brush, 'continent', alt.value('lightgray')),
        tooltip=['country']
    ).add_selection(
        brush  # <--- Attach the brush here!
    ).properties(
        width=400,
        title="Drag a box on this chart!"
    )

    # 3. The Bar Chart (Reacts to the box)
    bars = alt.Chart(lean_df).mark_bar().encode(
        x='count()',
        y='continent',
        color='continent'
    ).transform_filter(
        brush # <--- This filters the bars based on your box!
    ).properties(
        width=300,
        title="2. See counts update here"
    )

    # 4. Show them side-by-side
    scatter | bars
    return


@app.cell
def _(alt, lean_df):

    # 1. New Working URL (GeoJSON format)
    # This file contains country shapes AND names
    world_map_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"

    # 2. Define the source
    # Since it is GeoJSON, we use alt.Data instead of alt.topo_feature
    source = alt.Data(url=world_map_url, format=alt.DataFormat(property='features', type='json'))

    # 3. Build the Map
    map_chart = alt.Chart(source).mark_geoshape().encode(
        # Color: Use the Life Expectancy column
        color=alt.Color('life_expectancy_at_birth:Q', title='Life Expectancy', scale=alt.Scale(scheme='viridis')),
    
        # Tooltips: Show Country Name and Value
        tooltip=[
            alt.Tooltip('properties.name:N', title='Country'),
            alt.Tooltip('life_expectancy_at_birth:Q', title='Life Expectancy')
        ]
    ).transform_lookup(
        # Match 'properties.name' in the map file...
        lookup='properties.name',
    
        # ...with 'country' in your dataframe
        from_=alt.LookupData(lean_df, key='country', fields=['life_expectancy_at_birth'])
    ).project(
        type='naturalEarth1'
    ).properties(
        width=600,
        height=400,
        title="Global Life Expectancy"
    )

    map_chart
    return


@app.cell
def _(mo):

    # 1. Define the metrics we want to analyze
    # (Label -> Column Name)
    analysis_options = {
        'Life Expectancy (Years)': 'life_expectancy_at_birth',
        'Health Spending (% GDP)': 'government_health_expenditure_percent',
        'Access to Electricity (%)': 'access_to_electricity_percent',
        'Corruption Control': 'control_of_corruption_estimate',
    }

    # 2. Create the Selector
    analysis_selector = mo.ui.dropdown(
        options=analysis_options,
        value='Life Expectancy (Years)',
        label="Select Variable to Analyze"
    )

    analysis_selector
    return analysis_options, analysis_selector


@app.cell
def _(
    alt,
    analysis_options,
    analysis_selector,
    lean_df,
    mo,
    ols,
    pairwise_tukeyhsd,
    pd,
    sm,
):


    # 1. Get the User Selection
    # Get the selected column name (e.g., 'life_expectancy_at_birth')
    col_name = analysis_selector.value

    # Find the nice label for the title (e.g., 'Life Expectancy')
    # We look through the dictionary to find the Key that matches this Value
    chart_title = [k for k, v in analysis_options.items() if v == col_name][0]

    # 2. Prepare Data (Clean & Order)
    # FIXED LINE BELOW: Removed the extra quote after col_name
    work_df = lean_df[['income_group', col_name, 'country']].dropna()

    # Set the correct order for the x-axis
    group_order = ['Low', 'Lower_middle', 'Upper_middle', 'High']
    # Filter data to only include these 4 groups
    work_df = work_df[work_df['income_group'].isin(group_order)]

    # 3. Create the Charts
    # A. The Boxplot (Shows the ranges)
    boxplot = alt.Chart(work_df).mark_boxplot(extent='min-max', size=40).encode(
        x=alt.X('income_group', sort=group_order, title='Income Group'),
        y=alt.Y(col_name, title=chart_title),
        color=alt.Color('income_group', legend=None)
    )

    # B. The Jitter Points (Shows the individual countries)
    points = alt.Chart(work_df).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X('income_group', sort=group_order),
        y=alt.Y(col_name),
        color=alt.Color('income_group'),
        tooltip=['country', col_name, 'income_group']
    ).interactive()

    # Combine them
    combined_chart = (boxplot + points).properties(
        width=600, 
        height=400, 
        title=f"Distribution of {chart_title}"
    )

    # 4. Run the Statistics (Dynamic ANOVA)
    # This runs the math to prove if the groups are actually different
    formula = f'Q("{col_name}") ~ C(income_group)'
    model_ = ols(formula, data=work_df).fit()
    anova_table_ = sm.stats.anova_lm(model_, typ=3)
    p_val = anova_table_.loc['C(income_group)', 'PR(>F)']

    # 5. Prepare the Output
    stats_results = []
    tukey_display = None

    if p_val < 0.05:
        result_text = f"### Significant Difference (p = {p_val:.2e})"
    
        # Run Tukey HSD
        tukey_ = pairwise_tukeyhsd(endog=work_df[col_name], groups=work_df['income_group'], alpha=0.05)
    
        # Convert to DataFrame for nice display
        # We extract the data directly from the Tukey object
        tukey_data = pd.DataFrame(
            data=tukey_._results_table.data[1:], 
            columns=tukey_._results_table.data[0]
        )
        # Filter for significant rows only
        sig_diffs = tukey_data[tukey_data['reject'] == True]
    
        tukey_display = mo.vstack([
            mo.md("**Tukey Test Results (Significant Pairs Only):**"),
            mo.ui.table(sig_diffs, selection=None)
        ])
    else:
        result_text = f"### ❌ No Significant Difference (p = {p_val:.4f})"
        tukey_display = mo.md("Groups are statistically similar.")

    # 6. Final Display
    mo.vstack([
        combined_chart,
        mo.md("---"),
        mo.md(result_text),
        tukey_display
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Conclusion to Research Question 2:

    The One-Way ANOVA test was conducted to determine if Life Expectancy differs significantly by income group.

    1. ANOVA Results: The analysis revealed a statistically significant difference between the groups (p<0.05). This leads us to reject the Null Hypothesis, confirming that a country's wealth classification is a strong predictor of its population's longevity.

    2. Tukey Post-Hoc Analysis: Since the global test was significant, a Tukey HSD post-hoc test was performed to identify exactly where the differences lie. The results show that:
     - High Income vs. Low Income: There is a substantial gap, with High Income countries living significantly longer (approx. 15-20 years difference).
     - Middle Income Groups: Significant differences were also observed between Upper-Middle and Lower-Middle income countries, suggesting that even moderate economic improvements correlate with measurable health gains.´
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
