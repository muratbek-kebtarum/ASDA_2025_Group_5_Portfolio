# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.20.2",
#     "pandas",
#     "numpy",
#     "matplotlib",
#     "seaborn",
#     "plotly",
#     "scipy",
#     "scikit-learn",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    from scipy import stats
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA

    return PCA, StandardScaler, mo, np, pd, plt, px, sns


@app.cell
def _(pd):
    _url = (
        "https://huggingface.co/datasets/tarummurat/"
        "apartments_for_rent_classified_10K"
        "/raw/main/apartments_for_rent_classified_10K.csv"
    )
    raw = pd.read_csv(
        _url, sep=";", encoding="cp1252", na_values=["null", "None"]
    )
    return (raw,)


@app.cell
def _(raw):
    df_clean = raw.copy()

    # Drop rows missing core fields
    df_clean.dropna(subset=["bathrooms", "bedrooms"], inplace=True)
    df_clean = df_clean[df_clean["bathrooms"] > 0]

    # Normalise every price to monthly frequency
    df_clean.loc[
        df_clean["price_type"].str.lower() == "weekly", "price"
    ] *= 4
    df_clean.loc[
        df_clean["price_type"].str.lower() == "daily", "price"
    ] *= 30
    df_clean.loc[
        df_clean["price_type"].str.lower() == "yearly", "price"
    ] /= 12

    # Drop columns we no longer need
    df_clean.drop(
        columns=["price_type", "source", "currency"], inplace=True
    )

    # Fill / remap categorical columns
    df_clean["pets_allowed"] = df_clean["pets_allowed"].fillna("Not specified")
    df_clean["has_photo"] = df_clean["has_photo"].replace("Thumbnail", "Yes")

    # Remove fee, non-apartment categories
    df_clean.drop(columns=["fee"], errors="ignore", inplace=True)
    df_clean.drop(
        df_clean[
            df_clean["category"].str.contains("home|short_term", na=False)
        ].index,
        inplace=True,
    )
    df_clean.drop(columns=["category"], inplace=True)
    return (df_clean,)


@app.cell
def _(df_clean, np, pd):
    df = df_clean.copy()

    # IQR-based outlier removal on price and square_feet
    for _col in ["price", "square_feet"]:
        Q1, Q3 = df[_col].quantile(0.25), df[_col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[_col] >= Q1 - 1.5 * IQR) & (df[_col] <= Q3 + 1.5 * IQR)]

    # Derived numeric columns
    df["price_per_sqft"] = df["price"] / df["square_feet"].replace(0, np.nan)
    df = df[df["square_feet"] > 0]

    # Temporal features
    df["listing_date"] = pd.to_datetime(df["time"], unit="s")
    df["listing_month"] = df["listing_date"].dt.month
    df["listing_year"] = df["listing_date"].dt.year

    # Amenity flags (regex on the amenities text column)
    _amenity_patterns = {
        "has_parking": r"parking|garage",
        "has_laundry": r"laundry|washer|dryer",
        "has_pool": r"pool",
        "has_gym": r"gym|fitness|exercise",
        "has_ac": r"air conditioning|ac|a/c|hvac",
        "has_dishwasher": r"dishwasher",
        "has_balcony": r"balcony|patio|deck|terrace",
        "has_hardwood": r"hardwood|wood floor",
        "has_fireplace": r"fireplace",
        "has_doorman": r"doorman|concierge|24.hour|security",
        "has_elevator": r"elevator",
        "has_storage": r"storage",
        "is_furnished": r"furnished",
        "has_cable": r"cable|internet|wifi",
        "has_view": r"view|scenic",
    }
    _amen_clean = df["amenities"].fillna("").str.lower()
    for _feat, _pat in _amenity_patterns.items():
        df[_feat] = _amen_clean.str.contains(_pat, regex=True).astype(int)

    df["amenity_count"] = df[list(_amenity_patterns)].sum(axis=1)
    df["log_price"] = np.log1p(df["price"])
    return (df,)


@app.cell
def _(mo):
    mo.md("""
    # 🏠 Apartment Rental Price Dashboard

    **Dataset:** ~10 000 US rental listings  ·  **Target:** Monthly rent (USD)

    Explore interactive maps, filter by state / bedrooms / price,
    and dive into amenity analysis & model results.
    """)
    return


@app.cell
def _(df, mo):
    _n = len(df)
    _med = df["price"].median()
    _avg = df["price"].mean()
    _std = df["price"].std()
    _top_state = df.groupby("state")["price"].median().idxmax()
    _top_val = df.groupby("state")["price"].median().max()
    _n_states = df["state"].nunique()
    _n_cities = df["cityname"].nunique()
    _avg_sqft = df["square_feet"].median()

    mo.hstack(
        [
            mo.stat(label="Total Listings", value=f"{_n:,}"),
            mo.stat(label="Median Rent", value=f"${_med:,.0f}"),
            mo.stat(label="Mean Rent", value=f"${_avg:,.0f}"),
            mo.stat(label="Std Dev", value=f"${_std:,.0f}"),
            mo.stat(label="States Covered", value=f"{_n_states}"),
            mo.stat(label="Cities Covered", value=f"{_n_cities}"),
            mo.stat(label="Median Sq Ft", value=f"{_avg_sqft:,.0f}"),
            mo.stat(
                label="Priciest State",
                value=f"{_top_state} (${_top_val:,.0f})",
            ),
        ],
        justify="space-around",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🗺️ Interactive Listing Map

    Every dot is a **real apartment listing** — hover for details, click to
    zoom, scroll to explore the real-world neighbourhood on the street map.
    """)
    return


@app.cell
def _(mo):
    map_color = mo.ui.dropdown(
        options=["Price", "Bedrooms", "Price per Sq Ft", "Amenity Count"],
        value="Price",
        label="Colour by",
    )
    map_sample = mo.ui.slider(
        start=500, stop=5000, value=3000, step=500,
        label="Max points to display (for speed)",
        show_value=True,
    )
    mo.hstack([map_color, map_sample], justify="start", gap=2)
    return map_color, map_sample


@app.cell
def _(df, map_color, map_sample, mo, px):
    _col_map = {
        "Price": "price",
        "Bedrooms": "bedrooms",
        "Price per Sq Ft": "price_per_sqft",
        "Amenity Count": "amenity_count",
    }
    _color_col = _col_map[map_color.value]

    _n = min(map_sample.value, len(df))
    _df_map = (
        df.dropna(subset=["latitude", "longitude"])
        .sample(_n, random_state=42)
        .copy()
    )

    _df_map["hover"] = (
        _df_map["cityname"].astype(str) + ", " + _df_map["state"].astype(str)
        + "<br>$" + _df_map["price"].apply(lambda x: f"{x:,.0f}")
        + "/mo<br>" + _df_map["bedrooms"].astype(int).astype(str) + " bed, "
        + _df_map["bathrooms"].astype(str) + " bath"
        + "<br>" + _df_map["square_feet"].apply(lambda x: f"{x:,.0f}") + " sq ft"
        + "<br>" + _df_map["amenity_count"].astype(int).astype(str) + " amenities"
    )

    _cscale = "Turbo" if _color_col == "price" else "Viridis"

    fig_map = px.scatter_mapbox(
        _df_map,
        lat="latitude", lon="longitude",
        color=_color_col,
        size="price", size_max=12, opacity=0.7,
        hover_name="hover",
        hover_data={
            "latitude": False, "longitude": False,
            _color_col: False, "price": False,
        },
        color_continuous_scale=_cscale,
        mapbox_style="open-street-map",
        zoom=3.3,
        center={"lat": 38.5, "lon": -96},
        height=620,
        title=f"US Apartment Listings coloured by {map_color.value}",
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title=map_color.value),
    )
    mo.ui.plotly(fig_map)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🇺🇸 State-Level Rent Choropleth

    Colour-coded map of every US state present in the data.
    Toggle between median rent, mean rent, or listing count.
    """)
    return


@app.cell
def _(mo):
    choro_metric = mo.ui.dropdown(
        options=["Median Rent", "Mean Rent", "Listing Count"],
        value="Median Rent",
        label="Metric",
    )
    choro_metric
    return (choro_metric,)


@app.cell
def _(choro_metric, df, mo, px):
    _metric_name = choro_metric.value

    if _metric_name == "Listing Count":
        _state_agg = df.groupby("state")["price"].count().reset_index()
        _state_agg.columns = ["state", "value"]
        _clabel = "Count"
    elif _metric_name == "Mean Rent":
        _state_agg = df.groupby("state")["price"].mean().reset_index()
        _state_agg.columns = ["state", "value"]
        _clabel = "Mean Rent ($)"
    else:
        _state_agg = df.groupby("state")["price"].median().reset_index()
        _state_agg.columns = ["state", "value"]
        _clabel = "Median Rent ($)"

    fig_choro = px.choropleth(
        _state_agg,
        locations="state", locationmode="USA-states",
        color="value", color_continuous_scale="Reds",
        scope="usa",
        hover_name="state",
        hover_data={"value": ":.0f", "state": False},
        labels={"value": _clabel},
        title=f"{_metric_name} by US State",
        height=500,
    )
    fig_choro.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    mo.ui.plotly(fig_choro)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 📊 Top States by Rent

    Interactive horizontal bar chart. Adjust the slider to see more or
    fewer states and switch between median, mean, or listing count.
    """)
    return


@app.cell
def _(mo):
    geo_metric = mo.ui.dropdown(
        options=["Median Rent", "Mean Rent", "Listing Count"],
        value="Median Rent",
        label="Metric",
    )
    top_n = mo.ui.slider(
        start=5, stop=30, value=15, step=5,
        label="Top N states", show_value=True,
    )
    mo.hstack([geo_metric, top_n], justify="start", gap=2)
    return geo_metric, top_n


@app.cell
def _(df, geo_metric, mo, px, top_n):
    _metric = geo_metric.value

    if _metric == "Listing Count":
        _sv = df.groupby("state")["price"].count().sort_values(ascending=False)
        _ylabel = "Number of Listings"
    elif _metric == "Mean Rent":
        _sv = df.groupby("state")["price"].mean().sort_values(ascending=False)
        _ylabel = "Mean Monthly Rent ($)"
    else:
        _sv = df.groupby("state")["price"].median().sort_values(ascending=False)
        _ylabel = "Median Monthly Rent ($)"

    _top = _sv.head(top_n.value).reset_index()
    _top.columns = ["State", "Value"]

    fig_bar = px.bar(
        _top, x="Value", y="State", orientation="h",
        color="Value", color_continuous_scale="Reds",
        text="Value",
        labels={"Value": _ylabel, "State": ""},
        title=f"Top {top_n.value} States - {_metric}",
        height=max(350, top_n.value * 30),
    )
    fig_bar.update_traces(
        texttemplate=(
            "%{text:,.0f}" if _metric == "Listing Count"
            else "$%{text:,.0f}"
        ),
        textposition="outside",
    )
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        margin=dict(l=0, r=60, t=40, b=0),
    )
    mo.ui.plotly(fig_bar)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🔍 EDA Explorer

    Use the filters below to narrow down by state, bedrooms, and price
    range, then explore the resulting distribution, boxplots, and scatter.
    """)
    return


@app.cell
def _(df, mo):
    _states = sorted(df["state"].dropna().unique().tolist())
    _bed_vals = sorted(df["bedrooms"].dropna().unique().tolist())

    state_filter = mo.ui.multiselect(
        options=_states,
        value=[],
        label="Filter by State (leave empty = all)",
    )
    bedroom_filter = mo.ui.multiselect(
        options=[str(int(b)) for b in _bed_vals],
        value=[],
        label="Filter by Bedrooms (leave empty = all)",
    )
    price_slider = mo.ui.range_slider(
        start=int(df["price"].min()),
        stop=int(df["price"].max()),
        value=[
            int(df["price"].quantile(0.05)),
            int(df["price"].quantile(0.95)),
        ],
        step=50,
        label="Price Range ($)",
        show_value=True,
    )

    mo.vstack([
        mo.hstack([state_filter, bedroom_filter], justify="start", gap=2),
        price_slider,
    ])
    return bedroom_filter, price_slider, state_filter


@app.cell
def _(bedroom_filter, df, price_slider, state_filter):
    _dff = df.copy()

    if state_filter.value:
        _dff = _dff[_dff["state"].isin(state_filter.value)]
    if bedroom_filter.value:
        _beds = [float(b) for b in bedroom_filter.value]
        _dff = _dff[_dff["bedrooms"].isin(_beds)]

    lo, hi = price_slider.value
    _dff = _dff[(_dff["price"] >= lo) & (_dff["price"] <= hi)]

    df_filtered = _dff
    return (df_filtered,)


@app.cell
def _(df_filtered, mo, px):
    fig_hist = px.histogram(
        df_filtered, x="price", nbins=50,
        color_discrete_sequence=["steelblue"],
        labels={"price": "Monthly Rent ($)"},
        title=f"Price Distribution (n = {len(df_filtered):,})",
    )
    _med = df_filtered["price"].median()
    _mean = df_filtered["price"].mean()
    fig_hist.add_vline(
        x=_med, line_dash="dash", line_color="red",
        annotation_text=f"Median ${_med:,.0f}",
    )
    fig_hist.add_vline(
        x=_mean, line_dash="dash", line_color="orange",
        annotation_text=f"Mean ${_mean:,.0f}",
    )
    mo.ui.plotly(fig_hist)
    return


@app.cell
def _(df_filtered, mo, px):
    fig_bed = px.box(
        df_filtered, x="bedrooms", y="price",
        color_discrete_sequence=["coral"],
        labels={"bedrooms": "Bedrooms", "price": "Rent ($)"},
        title="Rent by Bedrooms",
    )

    _sample = df_filtered.sample(
        min(3000, len(df_filtered)), random_state=42
    )
    fig_scatter = px.scatter(
        _sample, x="square_feet", y="price",
        color="bedrooms", opacity=0.5,
        labels={
            "square_feet": "Square Feet",
            "price": "Rent ($)",
            "bedrooms": "Beds",
        },
        title="Square Feet vs Price",
        color_continuous_scale="Viridis",
    )

    mo.hstack(
        [mo.ui.plotly(fig_bed), mo.ui.plotly(fig_scatter)],
        widths="equal",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🛏️ Price by Bedrooms - Distribution Explorer

    Switch between Box, Violin, and Strip+Box layouts.
    Toggle log-scale to better see the spread for lower-rent apartments.
    """)
    return


@app.cell
def _(mo):
    plot_type = mo.ui.dropdown(
        options=["Box Plot", "Violin Plot", "Strip + Box"],
        value="Box Plot",
        label="Chart type",
    )
    show_log = mo.ui.switch(label="Log-scale Y axis", value=False)

    mo.hstack([plot_type, show_log], justify="start", gap=2)
    return plot_type, show_log


@app.cell
def _(df, plot_type, plt, show_log, sns):
    fig_bed2, ax_bed2 = plt.subplots(figsize=(12, 5))

    _ptype = plot_type.value
    if _ptype == "Violin Plot":
        sns.violinplot(
            data=df, x="bedrooms", y="price",
            ax=ax_bed2, palette="Set2", cut=0,
        )
    elif _ptype == "Strip + Box":
        sns.boxplot(
            data=df, x="bedrooms", y="price",
            ax=ax_bed2, palette="Set2",
            flierprops=dict(marker="", alpha=0),
        )
        sns.stripplot(
            data=df.sample(min(2000, len(df)), random_state=1),
            x="bedrooms", y="price", ax=ax_bed2,
            color="black", alpha=0.15, size=2, jitter=True,
        )
    else:
        sns.boxplot(
            data=df, x="bedrooms", y="price",
            ax=ax_bed2, palette="Set2",
        )

    if show_log.value:
        ax_bed2.set_yscale("log")

    ax_bed2.set_xlabel("Number of Bedrooms")
    ax_bed2.set_ylabel(
        "Monthly Rent ($)" + (" - log" if show_log.value else "")
    )
    ax_bed2.set_title(
        "Rent Distribution by Bedroom Count", fontweight="bold"
    )
    plt.tight_layout()
    fig_bed2
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🏷️ Amenity Prevalence & Rent Premium

    Left chart: how common is each amenity across all listings.
    Right chart: median rent difference between listings
    **with** vs **without** each amenity.
    """)
    return


@app.cell
def _(mo):
    amenity_sort = mo.ui.dropdown(
        options=["By Prevalence (%)", "By Rent Premium ($)"],
        value="By Prevalence (%)",
        label="Sort by",
    )
    amenity_sort
    return (amenity_sort,)


@app.cell
def _(amenity_sort, df, mo, pd, px):
    _amenity_cols = [
        "has_parking", "has_laundry", "has_pool", "has_gym", "has_ac",
        "has_dishwasher", "has_balcony", "has_hardwood", "has_fireplace",
        "has_doorman", "has_elevator", "has_storage", "is_furnished",
        "has_cable", "has_view",
    ]
    _label_map = {
        "has_parking": "Parking",
        "has_laundry": "Laundry/Washer",
        "has_pool": "Swimming Pool",
        "has_gym": "Gym/Fitness",
        "has_ac": "Air Conditioning",
        "has_dishwasher": "Dishwasher",
        "has_balcony": "Balcony/Patio",
        "has_hardwood": "Hardwood Floors",
        "has_fireplace": "Fireplace",
        "has_doorman": "Doorman/Security",
        "has_elevator": "Elevator",
        "has_storage": "Storage",
        "is_furnished": "Furnished",
        "has_cable": "Cable/Internet",
        "has_view": "Scenic View",
    }

    _rows = []
    for _col in _amenity_cols:
        _pct = df[_col].mean() * 100
        _with = df[df[_col] == 1]["price"].median()
        _without = df[df[_col] == 0]["price"].median()
        _rows.append({
            "Amenity": _label_map[_col],
            "Prevalence (%)": round(_pct, 1),
            "Premium ($)": round(_with - _without, 0),
        })
    _amen_df = pd.DataFrame(_rows)

    _sort_map = {
        "By Prevalence (%)": "Prevalence (%)",
        "By Rent Premium ($)": "Premium ($)",
    }
    _sort_col = _sort_map[amenity_sort.value]
    _amen_df = _amen_df.sort_values(_sort_col, ascending=True)

    # Prevalence chart
    fig_prev = px.bar(
        _amen_df, x="Prevalence (%)", y="Amenity", orientation="h",
        color="Prevalence (%)", color_continuous_scale="Blues",
        text="Prevalence (%)",
        title="How Common Is Each Amenity?",
        height=450,
    )
    fig_prev.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside"
    )
    fig_prev.update_layout(
        showlegend=False, margin=dict(l=0, r=60, t=40, b=0)
    )

    # Premium chart
    _amen_df["Color"] = _amen_df["Premium ($)"].apply(
        lambda v: "Premium" if v >= 0 else "Discount"
    )
    fig_prem = px.bar(
        _amen_df, x="Premium ($)", y="Amenity", orientation="h",
        color="Color",
        color_discrete_map={"Premium": "#27ae60", "Discount": "#e74c3c"},
        text="Premium ($)",
        title="Median Rent Premium vs No-Amenity",
        height=450,
    )
    fig_prem.update_traces(
        texttemplate="$%{text:+,.0f}", textposition="outside"
    )
    fig_prem.update_layout(margin=dict(l=0, r=80, t=40, b=0))

    mo.hstack(
        [mo.ui.plotly(fig_prev), mo.ui.plotly(fig_prem)],
        widths="equal",
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🏙️ City Deep-Dive Map

    Select a city to see **every listing pinned on a street-level map**.
    Hover for details - zoom into neighbourhoods, scroll to explore
    the real world around each apartment.
    """)
    return


@app.cell
def _(df, mo):
    _city_counts = df["cityname"].value_counts()
    _top_cities = _city_counts[_city_counts >= 10].index.tolist()[:60]

    city_picker = mo.ui.dropdown(
        options=sorted(_top_cities),
        value=sorted(_top_cities)[0],
        label="Pick a city",
    )
    city_picker
    return (city_picker,)


@app.cell
def _(city_picker, df, mo, np, px):
    _city = city_picker.value
    _dfc = (
        df[df["cityname"] == _city]
        .dropna(subset=["latitude", "longitude"])
        .copy()
    )


    _rng = np.random.default_rng(42)
    _dfc["latitude"]  = _dfc["latitude"]  + _rng.uniform(-0.012, 0.012, len(_dfc))
    _dfc["longitude"] = _dfc["longitude"] + _rng.uniform(-0.012, 0.012, len(_dfc))

    _dfc["hover"] = (
        "$" + _dfc["price"].apply(lambda x: f"{x:,.0f}")
        + "/mo<br>" + _dfc["bedrooms"].astype(int).astype(str) + " bed, "
        + _dfc["bathrooms"].astype(str) + " bath"
        + "<br>" + _dfc["square_feet"].apply(lambda x: f"{x:,.0f}") + " sq ft"
        + "<br>Pets: " + _dfc["pets_allowed"].astype(str)
    )

    _center_lat = _dfc["latitude"].median()
    _center_lon = _dfc["longitude"].median()

    fig_city = px.scatter_mapbox(
        _dfc,
        lat="latitude", lon="longitude",
        color="price",
        size_max=14, opacity=0.8,
        hover_name="hover",
        hover_data={
            "latitude": False, "longitude": False,
            "price": False,
        },
        color_continuous_scale="YlOrRd",
        mapbox_style="open-street-map",
        zoom=11,
        center={"lat": _center_lat, "lon": _center_lon},
        height=550,
        title=f"{_city} \u2014 {len(_dfc)} listings (coloured by price)",
    )
    fig_city.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title="Rent ($)"),
    )
    mo.ui.plotly(fig_city)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 📐 PCA - Dimensionality Explorer

    PCA on all numeric features (excluding price targets).
    Drag the slider to choose how many components to highlight.
    """)
    return


@app.cell
def _(mo):
    n_pcs = mo.ui.slider(
        start=2, stop=10, value=5, step=1,
        label="Number of PCs to display",
        show_value=True,
    )
    n_pcs
    return (n_pcs,)


@app.cell
def _(PCA, StandardScaler, df, n_pcs, np, plt):
    _scale_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    _scale_cols = [c for c in _scale_cols if c not in ["id", "time"]]
    _pca_features = [
        c for c in _scale_cols
        if c not in ["price", "price_per_sqft", "log_price"]
    ]

    _scaler = StandardScaler()
    _X_sc = _scaler.fit_transform(df[_pca_features].dropna())
    _pca = PCA()
    _pca.fit(_X_sc)

    _n = n_pcs.value
    _ev = _pca.explained_variance_ratio_
    _cu = np.cumsum(_ev)

    fig_pca, axes_pca = plt.subplots(1, 2, figsize=(14, 5))

    # Scree plot
    axes_pca[0].bar(
        range(1, len(_ev) + 1), _ev * 100,
        color="steelblue", edgecolor="black",
    )
    axes_pca[0].axvline(
        _n + 0.5, color="red", ls="--", lw=1.5,
        label=f"Selected: {_n} PCs",
    )
    axes_pca[0].set_xlabel("Principal Component")
    axes_pca[0].set_ylabel("Explained Variance (%)")
    axes_pca[0].set_title("Scree Plot", fontweight="bold")
    axes_pca[0].legend()

    # Cumulative variance
    axes_pca[1].plot(
        range(1, len(_cu) + 1), _cu * 100, "o-", color="coral", lw=2,
    )
    axes_pca[1].axhline(80, color="green", ls="--", lw=1.5, label="80%")
    axes_pca[1].axhline(90, color="orange", ls="--", lw=1.5, label="90%")
    axes_pca[1].fill_between(
        range(1, _n + 1), 0, _cu[:_n] * 100, alpha=0.15, color="coral",
    )
    axes_pca[1].set_xlabel("Number of Components")
    axes_pca[1].set_ylabel("Cumulative Explained Variance (%)")
    axes_pca[1].set_title(
        f"Cumulative - {_n} PCs = {_cu[_n-1]*100:.1f}%",
        fontweight="bold",
    )
    axes_pca[1].legend()

    plt.tight_layout()
    fig_pca
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🔎 Listing Data Table

    Browse individual listings. Filter by state, sort by any column,
    and control how many rows to display.
    """)
    return


@app.cell
def _(df, mo):
    _state_options = ["All"] + sorted(
        df["state"].dropna().unique().tolist()
    )
    table_state = mo.ui.dropdown(
        options=_state_options,
        value="All",
        label="Filter by State",
    )
    sort_col = mo.ui.dropdown(
        options=[
            "price", "square_feet", "bedrooms",
            "price_per_sqft", "amenity_count",
        ],
        value="price",
        label="Sort by",
    )
    sort_dir = mo.ui.dropdown(
        options=["Descending", "Ascending"],
        value="Descending",
        label="Order",
    )
    n_rows = mo.ui.slider(
        start=10, stop=100, value=25, step=5,
        label="Rows", show_value=True,
    )

    mo.hstack(
        [table_state, sort_col, sort_dir, n_rows],
        justify="start", gap=2,
    )
    return n_rows, sort_col, sort_dir, table_state


@app.cell
def _(df, mo, n_rows, sort_col, sort_dir, table_state):
    _display_cols = [
        "state", "cityname", "bedrooms", "bathrooms", "square_feet",
        "price", "price_per_sqft", "amenity_count", "pets_allowed",
        "latitude", "longitude",
    ]
    _tbl = df[[c for c in _display_cols if c in df.columns]].copy()

    if table_state.value != "All":
        _tbl = _tbl[_tbl["state"] == table_state.value]

    _asc = sort_dir.value == "Ascending"
    _tbl = _tbl.sort_values(sort_col.value, ascending=_asc).head(n_rows.value)

    mo.ui.table(_tbl.reset_index(drop=True))
    return


@app.cell
def _(mo):
    # A professional team credits section
    team_credits = mo.md(
        f"""
        ---
        ### 👥 Project Team
        **Dashboard, analysis and visualizations:** Muratbek Nurmatov & Ahmed Essam  <br>

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
