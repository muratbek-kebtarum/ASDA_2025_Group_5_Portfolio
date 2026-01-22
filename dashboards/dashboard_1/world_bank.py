import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## World Bank Project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Importing libraries
    """)
    return


@app.cell
def _():
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
    return np, ols, pairwise_tukeyhsd, pd, plt, sm, sns, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Loading and Merging data
    """)
    return


@app.cell
def _(pd):
    df1=pd.read_csv("../additional_material/datasets/week5/world_bank_development_indicators.csv")
    df2=pd.read_excel("../additional_material/datasets/week5/income.xlsx")
    df = pd.merge(df1, df2, left_on='country', right_on='Economy', how="inner")
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Data Inspection
    """)
    return


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    df.sample(8)
    return


@app.cell
def _(df):
    # Information about the dataset
    df.info()
    return


@app.cell
def _(df):
    # Dataset Shape
    print("Dataset Shape:", df.shape)
    return


@app.cell
def _(df):
    # columns in the dataset 
    print("Columns in the dataset:")
    for col in df.columns:
        print(col)
    return


@app.cell
def _(df):
    # percentage of missing values in each column
    missing_percentage = df.isnull().mean() * 100
    print("Percentage of missing values in each column:")
    print(missing_percentage)
    return


@app.cell
def _(df):
    # Checking for missing values
    df.isnull().sum()
    return


@app.cell
def _(df):
    # decribe the dataset
    df.describe()
    return


@app.cell
def _(df):
    # describe the dataset object type
    df.describe(include=['object'])
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
    # duplicated rows in the dataset
    df.duplicated().sum()
    return


@app.cell
def _(df):
    # number of entries for each income group
    df['Income group'].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Data Cleaning
    """)
    return


@app.cell
def _(df):
    df['Region'].value_counts()
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
    df['country'].unique()
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
    df_1 = df.drop(columns=['country_clean'])
    df_1 = df_1.drop(columns=['Region'])
    df_1['country'].unique()
    return (df_1,)


@app.cell
def _(df_1):
    df_1['Income group'] = df_1['Income group'].str.replace(' income', '').str.replace(' ', '_')
    return


@app.cell
def _(df_1):
    # Edit columns names 
    df_1.columns = [col.strip().lower().replace(' ', '_') for col in df_1.columns]
    #change % in column names to _percent
    df_1.columns = [col.replace('%', '_percent') for col in df_1.columns]
    df_1.columns
    return


@app.cell
def _(df_1):
    df_1.sample(5)
    return


@app.cell
def _(df_1):
    df_1.columns
    return


@app.cell
def _(df_1, pd):
    # edit the data types of date column, income_group column and continent column
    # Convert 'date' column to datetime
    df_1['date'] = pd.to_datetime(df_1['date'])
    df_1['income_group'] = df_1['income_group'].astype('category')
    # Convert 'income_group' and 'continent' to categorical
    df_1['continent'] = df_1['continent'].astype('category')
    # Check the data types
    print(df_1.dtypes)
    return


@app.cell
def _(df_1, np):
    #we need to have independent samples for ANOVA test so we should have one entry per country
    # Filter years 2015–2019 
    df_filtered = df_1[(df_1['date'].dt.year >= 2015) & (df_1['date'].dt.year <= 2019)]
    numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
    #Separate numeric and non-numeric columns 
    non_numeric_cols = df_filtered.select_dtypes(exclude=np.number).columns.tolist()
    non_numeric_cols = [col for col in non_numeric_cols if col != 'country']

    def mode_or_first(series):
    # Function to take mode (most frequent value) we will use it for non numerical columns
        m = series.mode()
        if not m.empty:
            return m[0]
        else:
            return series.iloc[0]
    agg_dict = {col: 'mean' for col in numeric_cols}  # fallback if all missing
    agg_dict.update({col: mode_or_first for col in non_numeric_cols})
    #Group by country and aggregate
    # numeric → mean
    df_filtered = df_filtered.groupby('country', as_index=False).agg(agg_dict)
    # categorical → mode
    df_filtered.head()
    return (df_filtered,)


@app.cell
def _(df_filtered, pd):
    # missing values summary
    missing_counts = df_filtered.isnull().sum()
    missing_pct = df_filtered.isnull().mean() * 100

    # create missing report dataframe
    missing_report = (
        pd.DataFrame({'missing_count': missing_counts, 'missing_pct': missing_pct})
        .sort_values('missing_pct', ascending=False)
    )

    print(missing_report)
    return


@app.cell
def _(df_filtered):
    # columns to drop
    cols_to_drop = ['electric_power_consumption', 'multidimensional_poverty_headcount_ratio_percent', 'risk_premium_on_lending', 'time_to_get_operation_license', 'central_goverment_debt_percent', 'gini_index', 'real_interest_rate', 'research_and_development_expenditure_percent', 'lending_category', 'human_capital_index', 'expense_percent', 'tax_revenue_percent', 'avg_precipitation', 'date', 'population_density', 'rural_population', 'regulatory_quality_estimate', 'logistic_performance_index', 'other_greenhouse_emisions', 'military_expenditure_percent', 'code', 'statistical_performance_indicators', 'voice_and_accountability_std', 'political_stability_std', 'rule_of_law_std', 'regulatory_quality_std', 'goverment_effectiveness_std', 'control_of_corruption_std', 'economy', 'land_area', 'birth_rate', 'death_rate']
    df_filtered_1 = df_filtered.drop(columns=cols_to_drop)  #missing value >30%  #99%  #77%  #71%  #70%  #68%  #50  #48%  #45%  #44%  #36%  #34%  #31%  # irrelevant Indicators  #std columns  #redundant columns  # duplicate of country  # have high correlation with life_expectancy_at_birth                
    return (df_filtered_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Data Inspection & Visualiztion
    """)
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.head()
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.info()
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.describe()
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.describe(include=['object', 'category'])
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1['income_group'].value_counts()
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1['continent'].value_counts()
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.shape
    return


@app.cell
def _(df_filtered_1, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.set_style('whitegrid')
    palette = sns.color_palette('Set3')
    income_counts = df_filtered_1['income_group'].value_counts()
    sns.barplot(x=income_counts.index, y=income_counts.values, ax=_axes[0], palette=palette)
    _axes[0].set_title('Number of Countries by Income Group', fontsize=12)
    _axes[0].set_xlabel('Income Group')
    _axes[0].set_ylabel('Number of Countries')
    continent_counts = df_filtered_1['continent'].value_counts()
    sns.barplot(x=continent_counts.index, y=continent_counts.values, ax=_axes[1], palette=palette)
    _axes[1].set_title('Number of Countries by Continent', fontsize=12)
    _axes[1].set_xlabel('Continent')
    _axes[1].set_ylabel('Number of Countries')
    _axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    #continue some visualizations
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Anova

    check assumptions
    - Independent samples
    - Equal sample sizes of groups → Type 3 Anova if not equal
    - Equal variances of groups
    - Normal distribution of the dependent variable → log-transform if needed
    - Normal distribution of residuals
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Environmental sustainability
    Question:
    - Does CO2 emission per capita differ across income groups?

    Variables:
    - DV (dependent variable) → co2_emissions

    - IV (independent variable / factor) → income_group
    """)
    return


@app.cell
def _(df_filtered_1):
    df_co2 = df_filtered_1[['country', 'income_group', 'co2_emisions', 'population']].copy()
    df_co2.head()
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
    #drop the 2 missing values
    df_co2_1 = df_co2.dropna(subset=['co2_emisions'])
    print(df_co2_1['co2_emisions'].isna().sum())
    return (df_co2_1,)


@app.cell
def _(df_co2_1):
    ##### Environmental sustainability
    # 1-We have independent samples as each country's data is independent of others.
    # 2- Sample sizes of groups are not equal, so we will use Type 3 Anova.
    df_co2_1['income_group'].value_counts()
    return


@app.cell
def _(df_co2_1, np):
    df_co2_1['co2_emisions_log'] = np.log(df_co2_1['co2_emisions'] + 1)
    return


@app.cell
def _(df_co2_1, plt, sns, stats):
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df_co2_1['co2_emisions_log'], kde=True, bins=30, color='skyblue', ax=_axes[0])
    _axes[0].set_title('Histogram of CO2 emisions')
    _axes[0].set_xlabel('CO2 emisions(log)')
    _axes[0].set_ylabel('Frequency')
    _osm, _osr = stats.probplot(df_co2_1['co2_emisions_log'])[0]
    _slope, _intercept, _r_value, _p_value, _std_err = stats.linregress(_osm, _osr)
    _axes[1].scatter(_osm, _osr, color='blue')
    _axes[1].plot(_osm, _intercept + _slope * _osm, color='red', lw=2)
    _axes[1].set_title('Q-Q Plot of CO2 emisions(log)')
    _axes[1].set_xlabel('Theoretical Quantiles')
    _axes[1].set_ylabel('Ordered Values')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_co2_1, np, stats):
    _stat, _p = stats.shapiro(np.log(df_co2_1['co2_emisions']))
    print(f'Statistics={_stat:.3f}, p={_p:.3f}')
    if _p > 0.05:
        print('Residuals look Gaussian (fail to reject H0)')
    else:
        print('Residuals do NOT look Gaussian (reject H0)')
    return


@app.cell
def _(df_co2_1, plt, sns):
    # 4-Equal variances of groups
    # Boxplot to visualize variance per income group
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='income_group', y='co2_emisions_log', data=df_co2_1, order=['Low', 'Lower_middle', 'Upper_middle', 'High'], palette='Set2')
    plt.title('CO2 emissions(Log) by Income Group')
    plt.xlabel('Income Group')
    plt.ylabel('CO2 emisions(Log)')
    plt.show()
    return


@app.cell
def _(df_co2_1, ols, sm):
    # Fit ANOVA model
    model = ols('co2_emisions_log ~ C(income_group)', data=df_co2_1).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    print('ANOVA Table:')
    print(anova_table)
    return anova_table, model


@app.cell
def _(model, plt, sns):
    residuals = model.resid

    plt.figure(figsize=(8,5))
    sns.histplot(residuals, bins=30, kde=True, color='skyblue')
    plt.title('Histogram of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.show()
    return (residuals,)


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
def _(df_co2_1, pairwise_tukeyhsd):
    # Tukey HSD post-hoc test
    tukey = pairwise_tukeyhsd(endog=df_co2_1['co2_emisions_log'], groups=df_co2_1['income_group'], alpha=0.05)
    print(tukey)  # your dependent variable  # your factor
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Income group has a very strong effect on CO₂ emissions,and here is the results
    - High-income countries emit significantly more CO₂ per capita than Low and Lower-Middle income countries.
    - Upper-Middle income countries emit significantly more than Low-income countries.
    - Income groups in the middle (Low ↔ Lower-Middle ↔ Upper-Middle) do NOT differ much.
    - Upper-Middle countries are surprisingly close to High-income countries (no significant difference).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Economic performance
    """)
    return


@app.cell
def _(df_filtered_1):
    df_gdp = df_filtered_1[['country', 'income_group', 'gdp_current_us']].copy()
    print(df_gdp['gdp_current_us'].isna().sum())
    #Impute missing values by the mean of their income group
    df_gdp['gdp_current_us'] = df_gdp.groupby('income_group')['gdp_current_us'].transform(lambda x: x.fillna(x.mean()))
    #Verify no missing values remain
    print(df_gdp['gdp_current_us'].isna().sum())
    return (df_gdp,)


@app.cell
def _(df_gdp):
    #drop the 2 missing values
    df_gdp_1 = df_gdp.dropna(subset=['gdp_current_us'])
    print(df_gdp_1['gdp_current_us'].isna().sum())
    return (df_gdp_1,)


@app.cell
def _(df_gdp_1, np):
    df_gdp_1['gdp_current_us_log'] = np.log(df_gdp_1['gdp_current_us'] + 1)
    return


@app.cell
def _(df_gdp_1, plt, sns, stats):
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df_gdp_1['gdp_current_us_log'], kde=True, bins=30, color='skyblue', ax=_axes[0])
    _axes[0].set_title('Histogram of GDP')
    _axes[0].set_xlabel('GDP(log)')
    _axes[0].set_ylabel('Frequency')
    _osm, _osr = stats.probplot(df_gdp_1['gdp_current_us_log'])[0]
    _slope, _intercept, _r_value, _p_value, _std_err = stats.linregress(_osm, _osr)
    _axes[1].scatter(_osm, _osr, color='blue')
    _axes[1].plot(_osm, _intercept + _slope * _osm, color='red', lw=2)
    _axes[1].set_title('Q-Q Plot of GDP(log)')
    _axes[1].set_xlabel('Theoretical Quantiles')
    _axes[1].set_ylabel('Ordered Values')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_gdp_1, stats):
    _stat, _p = stats.shapiro(df_gdp_1['gdp_current_us_log'])
    print(f'Statistics={_stat:.3f}, p={_p:.3f}')
    if _p > 0.05:
        print('Residuals look Gaussian (fail to reject H0)')
    else:
        print('Residuals do NOT look Gaussian (reject H0)')
    return


@app.cell
def _(df_gdp_1, plt, sns):
    # 4-Equal variances of groups
    # Boxplot to visualize variance per income group
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='income_group', y='gdp_current_us_log', data=df_gdp_1, order=['Low', 'Lower_middle', 'Upper_middle', 'High'], palette='Set2')
    plt.title('GDP(Log) by Income Group')
    plt.xlabel('Income Group')
    plt.ylabel('GDP(Log)')
    plt.show()
    return


@app.cell
def _(df_gdp_1, stats):
    groups_data = [df_gdp_1[df_gdp_1['income_group'] == g]['gdp_current_us_log'].dropna() for g in ['Low', 'Lower_middle', 'Upper_middle', 'High']]
    _stat, _p = stats.levene(*groups_data)
    print(f"Levene's Test: Statistic = {_stat:.3f}, p-value = {_p:.3f}")
    if _p > 0.05:
        print('Variances are equal across groups (fail to reject H0).')
    else:
        print('Variances are NOT equal across groups (reject H0).')
    return


@app.cell
def _(df_gdp_1):
    #non equal variances anova
    import pingouin as pg
    welch_result = pg.welch_anova(dv='gdp_current_us_log', between='income_group', data=df_gdp_1)
    # Welch ANOVA using pingouin
    print(welch_result)
    return (pg,)


@app.cell
def _(df_gdp_1, pg):
    posthoc = pg.pairwise_gameshowell(dv='gdp_current_us_log', between='income_group', data=df_gdp_1)
    posthoc
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - High-income countries have significantly higher GDP compared to Low-, Lower-Middle-, and Upper-Middle income countries.
    - Differences among the Low-, Lower-Middle-, and Upper-Middle income groups are not statistically significant, indicating that GDP levels within these middle and lower groups are relatively similar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Human well-being and health
    """)
    return


@app.cell
def _(df_filtered_1):
    df_filtered_1.to_csv('Human-well-being-health.csv', index=False)
    return


@app.cell
def _(
    df_filtered_1,
    levene,
    np,
    ols,
    pairwise_tukeyhsd,
    plt,
    residuals,
    sm,
    sns,
):
    group_order = ['Low', 'Lower_middle', 'Upper_middle', 'High']

    def analyze_indicator(data, col_name, title, apply_log=False):
        """
        Runs the full analysis pipeline: Boxplot -> Assumptions -> ANOVA -> Tukey
        """
        print(f"\n{'=' * 60}")
        print(f'ANALYSIS FOR: {title}')
        print(f"{'=' * 60}")
        work_df = data[['income_group', col_name]].dropna()
        if apply_log:
            work_df[col_name] = np.log(work_df[col_name])
            print('Note: Data has been log-transformed for analysis.')
        _fig, _axes = plt.subplots(1, 3, figsize=(18, 5))
        sns.boxplot(x='income_group', y=col_name, data=work_df, order=group_order, ax=_axes[0], palette='Set2')
        _axes[0].set_title(f'Boxplot: {title}')
        _axes[0].set_xlabel('Income Group')
        sns.histplot(residuals, kde=True, ax=_axes[1], color='skyblue')
        _axes[1].set_title('Histogram of Residuals')
        _axes[1].set_xlabel('Residuals')
        sm.qqplot(residuals, line='45', fit=True, ax=_axes[2])
        _axes[2].set_title('Q-Q Plot of Residuals')
        plt.tight_layout()
        plt.show()
        print('--- Assumptions ---')
        groups = [work_df[work_df['income_group'] == g][col_name] for g in group_order if g in work_df['income_group'].unique()]
        _stat, p_levene = levene(*groups)
        print(f"Levene's Test (Equal Variance): p-value = {p_levene:.4f}")
        if p_levene < 0.05:
            print('  -> Warning: Variances are not equal (Assumption violated).')
        else:
            print('  -> Variances are equal.')
        print('\n--- Type 3 ANOVA Results ---')
        formula = f'Q("{col_name}") ~ C(income_group)'
        model = ols(formula, data=work_df).fit()
        anova_table = sm.stats.anova_lm(model, typ=3)
        print(anova_table)
        p_val = anova_table.loc['C(income_group)', 'PR(>F)']
        if p_val < 0.05:
            print('\n--- Significant difference found! Running Tukey HSD ---')
            tukey = pairwise_tukeyhsd(endog=work_df[col_name], groups=work_df['income_group'], alpha=0.05)
            print(tukey)
        else:
            print('\nNo significant difference found between groups.')
    analyze_indicator(df_filtered_1, 'life_expectancy_at_birth', 'Life Expectancy')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Human Well-being: Life Expectancy at Birth

    Our analysis reveals a striking, stepwise stratification in human longevity based on national income. An Analysis of Variance (ANOVA) confirmed highly significant differences between groups ($F(3, 183) = 106.9, p < 0.001$).

    Post-hoc analysis (Tukey HSD) demonstrates that these disparities exist at every level of development; every income group is statistically distinct from the others. The disparity is most profound at the extremes: **individuals in High-Income countries live, on average, 17.5 years longer than those in Low-Income countries.**

    Notably, the "development ladder" yields consistent gains: moving from Low to Lower-Middle income is associated with a **5.3-year increase** in life expectancy, suggesting that even early-stage economic development yields major health dividends.

    > **Methodological Note:** Levene’s test indicated unequal variances between groups ($p=0.02$), reflecting greater variability in outcomes within lower-income nations compared to the consistently high outcomes in wealthy nations.
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

