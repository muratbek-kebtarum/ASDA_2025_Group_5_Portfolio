import marimo

__generated_with = "0.19.7"
app = marimo.App(width="full")


@app.cell
def _():
    # %% [Cell 1: Imports and Configuration]
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    from typing import Optional, Tuple, Dict, List, Any
    from functools import lru_cache
    from pathlib import Path
    import re

    # Altair configuration for dark/light mode compatibility
    alt.themes.enable("default")

    # Constants
    DATA_PATH = "https://raw.githubusercontent.com/muratbek-kebtarum/ASDA_2025_Group_5_Portfolio/refs/heads/main/additional_material/datasets/week11/6.3.3_spotify_5000_songs.csv"
    DEFAULT_BINS = 30
    TOP_ARTISTS_LIMIT = 50
    MAX_EMBED_PLAYERS = 8
    COLOR_SCHEMES = {
        "primary": "#1DB954",  # Spotify green
        "secondary": "#191414",  # Spotify black
        "accent": "#1ED760",
        "categorical": "set2"
    }

    # Validation schema for expected columns
    REQUIRED_COLUMNS = {"name", "artist", "id"}
    NUMERIC_COLUMNS = {
        "duration_ms", "tempo", "energy", "valence", "danceability", 
        "loudness", "speechiness", "acousticness", "instrumentalness", 
        "liveness", "popularity"
    }
    return (
        COLOR_SCHEMES,
        DATA_PATH,
        DEFAULT_BINS,
        List,
        MAX_EMBED_PLAYERS,
        NUMERIC_COLUMNS,
        REQUIRED_COLUMNS,
        TOP_ARTISTS_LIMIT,
        Tuple,
        alt,
        mo,
        pd,
        re,
    )


@app.cell
def _(DATA_PATH, NUMERIC_COLUMNS, REQUIRED_COLUMNS, mo, pd, re):

    # %% [Cell 2: Data Loading Functions]
    def to_snake_case(name: str) -> str:
        """Convert column name to snake_case."""
        name = re.sub(r'[\s]+', '_', name.strip())
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return re.sub(r'[^a-z0-9_]', '', name)


    @mo.cache
    def load_and_clean_data(path: str = DATA_PATH) -> pd.DataFrame:
        """Load and clean Spotify dataset with feature engineering."""
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found at {path}")

        # Clean column names
        df.columns = [to_snake_case(col) for col in df.columns]

        # Validate
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Remove critical missing values
        df = df.dropna(subset=["name", "artist", "id"])

        # Fill numeric missing values
        for col in NUMERIC_COLUMNS & set(df.columns):
            if df[col].isna().any():
                df[col] = df[col].fillna(df[col].median())

        # Conversions
        if "duration_ms" in df.columns:
            df["duration_minutes"] = df["duration_ms"] / 60000

        if "tempo" in df.columns:
            df["tempo"] = pd.to_numeric(df["tempo"], errors="coerce")

        # Ensure strings
        for col in ["name", "artist", "album", "genre"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        # Feature engineering
        if "valence" in df.columns:
            df["mood"] = pd.cut(
                df["valence"],
                bins=[0, 0.4, 0.6, 1.0],
                labels=["Sad", "Neutral", "Happy"],
                include_lowest=True
            )

        if "energy" in df.columns:
            df["energy_level"] = pd.cut(
                df["energy"],
                bins=[0, 0.33, 0.66, 1.0],
                labels=["Low", "Medium", "High"],
                include_lowest=True
            )

        if "tempo" in df.columns:
            df["tempo_category"] = pd.cut(
                df["tempo"],
                bins=[0, 60, 90, 120, 150, 300],
                labels=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"]
            )

        # Spotify embed URLs
        df["spotify_embed_url"] = df["id"].apply(
            lambda x: f"https://open.spotify.com/embed/track/{x}" if pd.notna(x) else ""
        )

        return df


    # Load data
    df_clean = load_and_clean_data()
    return (df_clean,)


@app.cell
def _(TOP_ARTISTS_LIMIT, df_clean, mo):

    # %% [Cell 3: Sidebar UI Controls - CRITICAL FOR REACTIVITY]
    # These MUST be top-level variables so other cells can reference them

    # Get data ranges for sliders
    _energy_min = float(df_clean["energy"].min()) if "energy" in df_clean.columns else 0.0
    _energy_max = float(df_clean["energy"].max()) if "energy" in df_clean.columns else 1.0
    _valence_min = float(df_clean["valence"].min()) if "valence" in df_clean.columns else 0.0
    _valence_max = float(df_clean["valence"].max()) if "valence" in df_clean.columns else 1.0
    _tempo_min = float(df_clean["tempo"].min()) if "tempo" in df_clean.columns else 0.0
    _tempo_max = float(df_clean["tempo"].max()) if "tempo" in df_clean.columns else 200.0

    _top_artists = df_clean["artist"].value_counts().head(TOP_ARTISTS_LIMIT).index.tolist()

    # Define UI controls as global variables
    artist_select = mo.ui.multiselect(
        options=_top_artists,
        value=_top_artists[:10],
        label="🎤 Select Artists",
        full_width=True
    )

    energy_slider = mo.ui.range_slider(
        start=_energy_min,
        stop=_energy_max,
        step=0.01,
        value=(_energy_min, _energy_max),
        label="⚡ Energy Range"
    )

    valence_slider = mo.ui.range_slider(
        start=_valence_min,
        stop=_valence_max,
        step=0.01,
        value=(_valence_min, _valence_max),
        label="😊 Valence (Mood)"
    )

    tempo_slider = mo.ui.range_slider(
        start=_tempo_min,
        stop=_tempo_max,
        step=1.0,
        value=(_tempo_min, _tempo_max),
        label="🥁 Tempo (BPM)"
    )

    danceability_dropdown = mo.ui.dropdown(
        options=["All", "High (>0.6)", "Medium (0.4-0.6)", "Low (<0.4)"],
        value="All",
        label="💃 Danceability"
    )

    instrumental_toggle = mo.ui.switch(
        value=False,
        label="🎺 Instrumental Only"
    )

    live_toggle = mo.ui.switch(
        value=False,
        label="🎵 Live Recordings"
    )

    sort_dropdown = mo.ui.dropdown(
        options=["Energy", "Valence", "Tempo", "Duration", "Popularity"],
        value="Energy",
        label="📊 Sort By"
    )

    search_box = mo.ui.text(
        value="",
        label="🔍 Search Songs/Artists",
        full_width=True
    )

    reset_button = mo.ui.button(
        label="🔄 Reset Filters",
        kind="warn"
    )

    # Create sidebar layout
    sidebar = mo.sidebar([
        mo.md("## 🎧 Spotify Analytics"),
        mo.md("Filter your music library"),
        mo.callout("Adjust controls to explore patterns.", kind="info"),
        mo.md("---"),
        search_box,
        artist_select,
        mo.md("---"),
        mo.md("### Audio Features"),
        energy_slider,
        valence_slider,
        tempo_slider,
        danceability_dropdown,
        mo.hstack([instrumental_toggle, live_toggle]),
        mo.md("---"),
        sort_dropdown,
        mo.md("---"),
        reset_button
    ])
    return (
        artist_select,
        danceability_dropdown,
        energy_slider,
        instrumental_toggle,
        live_toggle,
        reset_button,
        search_box,
        sidebar,
        sort_dropdown,
        tempo_slider,
        valence_slider,
    )


@app.cell
def _(
    artist_select,
    danceability_dropdown,
    energy_slider,
    instrumental_toggle,
    live_toggle,
    reset_button,
    search_box,
    tempo_slider,
    valence_slider,
):


    # %% [Cell 4: Reset Logic]
    # Handle reset button press
    if reset_button.value:
        artist_select.value = _top_artists[:10]
        energy_slider.value = (_energy_min, _energy_max)
        valence_slider.value = (_valence_min, _valence_max)
        tempo_slider.value = (_tempo_min, _tempo_max)
        danceability_dropdown.value = "All"
        instrumental_toggle.value = False
        live_toggle.value = False
        search_box.value = ""

    return


@app.cell
def _(
    List,
    Tuple,
    artist_select,
    danceability_dropdown,
    df_clean,
    energy_slider,
    instrumental_toggle,
    live_toggle,
    pd,
    search_box,
    sort_dropdown,
    tempo_slider,
    valence_slider,
):

    # %% [Cell 5: Reactive Filter Logic]
    def create_filter_mask(
        df: pd.DataFrame,
        artists: List[str],
        energy_range: Tuple[float, float],
        valence_range: Tuple[float, float],
        tempo_range: Tuple[float, float],
        danceability: str,
        instrumental: bool,
        live: bool,
        search_query: str
    ) -> pd.Series:
        """Create boolean mask for filtering dataframe."""
        mask = pd.Series([True] * len(df), index=df.index)

        if artists:
            mask &= df["artist"].isin(artists)

        if "energy" in df.columns:
            mask &= (df["energy"] >= energy_range[0]) & (df["energy"] <= energy_range[1])

        if "valence" in df.columns:
            mask &= (df["valence"] >= valence_range[0]) & (df["valence"] <= valence_range[1])

        if "tempo" in df.columns:
            mask &= (df["tempo"] >= tempo_range[0]) & (df["tempo"] <= tempo_range[1])

        if danceability != "All" and "danceability" in df.columns:
            if "High" in danceability:
                mask &= df["danceability"] > 0.6
            elif "Low" in danceability:
                mask &= df["danceability"] < 0.4
            else:
                mask &= (df["danceability"] >= 0.4) & (df["danceability"] <= 0.6)

        if instrumental and "instrumentalness" in df.columns:
            mask &= df["instrumentalness"] > 0.5

        if live and "liveness" in df.columns:
            mask &= df["liveness"] > 0.8

        if search_query:
            search_lower = search_query.lower()
            name_match = df["name"].str.lower().str.contains(search_lower, na=False)
            artist_match = df["artist"].str.lower().str.contains(search_lower, na=False)
            mask &= (name_match | artist_match)

        return mask


    def sort_dataframe(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
        """Sort dataframe by selected column."""
        column_map = {
            "Energy": "energy",
            "Valence": "valence",
            "Tempo": "tempo",
            "Duration": "duration_minutes",
            "Popularity": "popularity"
        }
        col = column_map.get(sort_by, "energy")
        if col in df.columns:
            return df.sort_values(by=col, ascending=False)
        return df


    # CRITICAL: Reference the global UI variables directly
    # This creates the reactive dependency - when these .value attributes change, this cell re-runs
    filtered_df = df_clean[
        create_filter_mask(
            df_clean,
            artist_select.value,        # Global variable reference
            energy_slider.value,        # Global variable reference  
            valence_slider.value,       # Global variable reference
            tempo_slider.value,         # Global variable reference
            danceability_dropdown.value,# Global variable reference
            instrumental_toggle.value,  # Global variable reference
            live_toggle.value,          # Global variable reference
            search_box.value            # Global variable reference
        )
    ]

    filtered_df = sort_dataframe(filtered_df, sort_dropdown.value)

    return (filtered_df,)


@app.cell
def _(COLOR_SCHEMES, filtered_df, mo, pd):
    # %% [Cell 6: Statistics Cards]
    def generate_stats_cards(df: pd.DataFrame):
        """Generate dynamic statistics cards."""
        if df.empty:
            return mo.callout("No songs match the current filters.", kind="warn")

        count = len(df)
        avg_duration = df["duration_minutes"].mean() if "duration_minutes" in df.columns else 0
        avg_tempo = df["tempo"].mean() if "tempo" in df.columns else 0
        avg_energy = df["energy"].mean() if "energy" in df.columns else 0

        def stat_card(value, label, color=COLOR_SCHEMES["primary"]):
            return mo.md(f"""
            <div style="
                background: linear-gradient(135deg, {color}22, {color}11);
                border-left: 4px solid {color};
                padding: 1rem;
                border-radius: 8px;
                min-width: 120px;
            ">
                <div style="font-size: 1.5rem; font-weight: bold; color: {color};">{value}</div>
                <div style="font-size: 0.875rem; opacity: 0.8;">{label}</div>
            </div>
            """)

        return mo.hstack([
            stat_card(f"{count}", "🎵 Songs"),
            stat_card(f"{avg_duration:.1f}m", "⏱️ Avg Duration"),
            stat_card(f"{avg_tempo:.0f}", "🥁 Avg BPM"),
            stat_card(f"{avg_energy:.2f}", "⚡ Avg Energy"),
        ], justify="space-between", gap=2)


    stats_cards = generate_stats_cards(filtered_df)
    return (stats_cards,)


@app.cell
def _(COLOR_SCHEMES, DEFAULT_BINS, alt, filtered_df, pd):
    # %% [Cell 7: Visualization Functions]
    def create_scatter_plot(df: pd.DataFrame):
        """Create Energy vs Valence scatter plot."""
        if df.empty or "energy" not in df.columns or "valence" not in df.columns:
            return alt.Chart(pd.DataFrame()).mark_text(text="No data available")

        top_artists = df["artist"].value_counts().head(10).index.tolist()
        df_plot = df.copy()
        df_plot["color_group"] = df_plot["artist"].apply(
            lambda x: x if x in top_artists else "Other"
        )

        return alt.Chart(df_plot).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X("energy:Q", title="Energy", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("valence:Q", title="Valence (Mood)", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("color_group:N", title="Artist", scale=alt.Scale(scheme=COLOR_SCHEMES["categorical"])),
            tooltip=["name:N", "artist:N", "energy:Q", "valence:Q", "tempo:Q"]
        ).properties(
            title="Energy vs Valence",
            width=400,
            height=350
        ).interactive()


    def create_histogram(df: pd.DataFrame, feature: str = "tempo"):
        """Create histogram of selected audio feature."""
        if df.empty or feature not in df.columns:
            return alt.Chart(pd.DataFrame()).mark_text(text="No data")

        return alt.Chart(df).mark_bar(color=COLOR_SCHEMES["primary"], opacity=0.7).encode(
            x=alt.X(f"{feature}:Q", bin=alt.Bin(maxbins=DEFAULT_BINS)),
            y="count()",
            tooltip=[f"{feature}:Q", "count()"]
        ).properties(
            title=f"Distribution of {feature.title()}",
            width=350,
            height=300
        )


    def create_correlation_heatmap(df: pd.DataFrame):
        """Create correlation heatmap."""
        numeric_cols = ["energy", "valence", "danceability", "tempo", "loudness", 
                       "speechiness", "acousticness", "instrumentalness", "liveness"]
        available_cols = [col for col in numeric_cols if col in df.columns]

        if len(available_cols) < 2:
            return alt.Chart(pd.DataFrame()).mark_text(text="Insufficient data")

        corr_matrix = df[available_cols].corr().reset_index().melt(
            id_vars="index", var_name="feature2", value_name="correlation"
        )
        corr_matrix.columns = ["feature1", "feature2", "correlation"]

        base = alt.Chart(corr_matrix).mark_rect().encode(
            x="feature1:N",
            y="feature2:N",
            color=alt.Color("correlation:Q", scale=alt.Scale(domain=[-1, 1], scheme="blueorange")),
            tooltip=["feature1", "feature2", alt.Tooltip("correlation:Q", format=".2f")]
        ).properties(
            title="Feature Correlations",
            width=400,
            height=400
        )

        text = alt.Chart(corr_matrix).mark_text(size=10).encode(
            x="feature1:N",
            y="feature2:N",
            text=alt.Text("correlation:Q", format=".2f"),
            color=alt.condition(alt.datum.correlation > 0.5, alt.value("white"), alt.value("black"))
        )

        return base + text


    def create_artist_bar_chart(df: pd.DataFrame):
        """Create bar chart of top artists."""
        if df.empty:
            return alt.Chart(pd.DataFrame()).mark_text(text="No data")

        artist_counts = df["artist"].value_counts().head(10).reset_index()
        artist_counts.columns = ["artist", "count"]

        return alt.Chart(artist_counts).mark_bar(color=COLOR_SCHEMES["primary"]).encode(
            x="count:Q",
            y=alt.Y("artist:N", sort="-x"),
            tooltip=["artist", "count"]
        ).properties(
            title="Top 10 Artists",
            width=350,
            height=300
        )


    # Generate charts (these will re-run when filtered_df changes)
    scatter_chart = create_scatter_plot(filtered_df)
    tempo_histogram = create_histogram(filtered_df, "tempo")
    energy_histogram = create_histogram(filtered_df, "energy")
    correlation_heatmap = create_correlation_heatmap(filtered_df)
    artist_chart = create_artist_bar_chart(filtered_df)

    return (
        artist_chart,
        correlation_heatmap,
        energy_histogram,
        scatter_chart,
        tempo_histogram,
    )


@app.cell
def _(MAX_EMBED_PLAYERS, filtered_df, mo, pd):

    # %% [Cell 8: Playlist Components]
    def create_playlist_table(df: pd.DataFrame):
        """Create styled table for filtered songs."""
        if df.empty:
            return mo.md("No songs match your criteria.")

        display_cols = ["name", "artist", "duration_minutes", "energy", "valence"]
        available_cols = [col for col in display_cols if col in df.columns]
        table_data = df[available_cols].head(50).copy()

        column_map = {
            "name": "Song",
            "artist": "Artist", 
            "duration_minutes": "Duration (min)",
            "energy": "Energy",
            "valence": "Valence"
        }
        table_data = table_data.rename(columns={k: v for k, v in column_map.items() if k in table_data.columns})

        return mo.ui.table(table_data, selection="single", label="Click a row to preview")


    def create_embed_players(df: pd.DataFrame, max_players: int = MAX_EMBED_PLAYERS):
        """Create Spotify embed iframes."""
        if df.empty or "spotify_embed_url" not in df.columns:
            return [mo.md("No playable tracks available.")]

        players = []
        for _, row in df.head(max_players).iterrows():
            if row["spotify_embed_url"]:
                iframe_html = f"""
                <iframe src="{row['spotify_embed_url']}" width="100%" height="80" 
                frameBorder="0" allowtransparency="true" allow="encrypted-media"
                style="border-radius: 12px; margin-bottom: 0.5rem;"></iframe>
                """
                players.append(mo.Html(iframe_html))

        return players


    playlist_table = create_playlist_table(filtered_df)
    embed_players = create_embed_players(filtered_df)

    return embed_players, playlist_table


@app.cell
def _(
    artist_chart,
    correlation_heatmap,
    embed_players,
    energy_histogram,
    filtered_df,
    mo,
    playlist_table,
    scatter_chart,
    sidebar,
    stats_cards,
    tempo_histogram,
):

    # %% [Cell 9: Main Layout]
    # Pre-calculate stats
    avg_energy = filtered_df['energy'].mean() if 'energy' in filtered_df.columns else None
    avg_valence = filtered_df['valence'].mean() if 'valence' in filtered_df.columns else None
    energy_corr_valence = filtered_df['energy'].corr(filtered_df['valence']) if ('energy' in filtered_df.columns and 'valence' in filtered_df.columns) else 0

    energy_str = f"{avg_energy:.2f}" if avg_energy is not None else "N/A"
    valence_str = f"{avg_valence:.2f}" if avg_valence is not None else "N/A"
    insight_text = "High energy correlates with positive mood!" if energy_corr_valence > 0.3 else "Energy and mood show diverse patterns."

    # Layout composition
    header = mo.vstack([
        mo.md("# 🎵 Spotify Music Analytics Dashboard"),
        mo.md(f"Exploring **{len(filtered_df)}** songs"),
        stats_cards,
        mo.md("---")
    ], gap=1)

    viz_tabs = mo.ui.tabs({
        "Energy vs Mood": scatter_chart,
        "Distributions": mo.vstack([tempo_histogram, energy_histogram]),
        "Correlations": correlation_heatmap,
        "Artist Stats": artist_chart
    })

    playlist_section = mo.vstack([
        mo.md("## 🎧 Now Playing"),
        mo.hstack([
            mo.vstack([mo.md("### Selected Tracks"), playlist_table], justify="start"),
            mo.vstack([mo.md("### Preview Players")] + embed_players[:4], justify="start")
        ], justify="space-between", gap=2)
    ])

    main_content = mo.vstack([
        header,
        mo.md("## 📊 Audio Features Analysis"),
        mo.callout(f"**Insight:** Average energy: {energy_str}, valence: {valence_str}. {insight_text}", kind="success"),
        viz_tabs,
        mo.md("---"),
        playlist_section
    ], gap=2)

    # Final output
    mo.vstack([sidebar, main_content])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
