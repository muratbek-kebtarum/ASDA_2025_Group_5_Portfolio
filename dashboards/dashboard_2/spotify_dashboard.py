import marimo

__generated_with = "0.19.6"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    from scipy.cluster.hierarchy import linkage, fcluster
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from sklearn.model_selection import train_test_split
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    return mo, np, pd


@app.cell
def _(mo):
    mo.md("""
    # 🎵 Interactive Spotify Clustering Dashboard
    **Explore how songs group together based on their audio features.**
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("https://raw.githubusercontent.com/muratbek-kebtarum/ASDA_2025_Group_5_Portfolio/refs/heads/main/additional_material/datasets/week11/6.3.3_spotify_5000_songs.csv")
    df
    return (df,)


@app.cell
def _(df, np):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return


@app.cell
def _(get_spotify_player):
    get_spotify_player("1n7JnwviZ7zf0LR1tcGFq7")
    return


@app.cell
def _(mo):
    def get_spotify_player(track_id):
        if not track_id:
            return mo.md("_Select a song to play_")
    
        # Spotify Embed URL structure
        embed_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
    
        return mo.Html(
            f"""
            <iframe 
                src="{embed_url}" 
                width="100%" 
                height="152" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
            </iframe>
            """
        )
    return (get_spotify_player,)


@app.cell
def _():
    return


@app.cell(column=1)
def _():
    return


if __name__ == "__main__":
    app.run()
