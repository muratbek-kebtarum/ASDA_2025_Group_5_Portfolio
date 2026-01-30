import marimo

__generated_with = "0.19.7"
app = marimo.App(width="columns")


@app.cell
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
    return KMeans, StandardScaler, mo, np, pd, plt, silhouette_score, sns


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
    df.columns = df.columns.str.strip()
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={'name': 'track_name', 'artist': 'artist_name'})

    feature_cols = ['danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 
                   'liveness', 'valence', 'tempo', 'duration_ms']

    df_clean = df.dropna(subset=feature_cols).copy()
    X = df_clean[feature_cols].values
    return X, df, df_clean, feature_cols


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
def _(df_clean, mo):
    mo.md(f"""
    ## 🎵 Spotify Clustering Dashboard\n**Loaded:** {len(df_clean):,} tracks
    """)
    return


@app.cell
def _(StandardScaler, X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return (X_scaled,)


@app.cell
def _(mo):
    max_clusters = mo.ui.slider(2, 15, value=10, label="Max Clusters for Analysis")
    k_selected = mo.ui.slider(2, 10, value=4, label="K for K-Means")
    min_cluster_size = mo.ui.slider(5, 50, value=15, label="HDBSCAN Min Cluster Size")

    mo.hstack([max_clusters, k_selected, min_cluster_size])
    return k_selected, max_clusters


@app.cell
def _(KMeans, X_scaled, max_clusters, mo):

    inertias = []
    k_range = list(range(2, max_clusters.value + 1))

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    mo.md(f"Elbow method calculated for k=2 to {max_clusters.value}")
    return inertias, k_range


@app.cell
def _(inertias, k_range, mo, plt):

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('Inertia (WCSS)')
    ax.set_title('Elbow Method for Optimal k')
    ax.grid(True, alpha=0.3)
    mo.mpl.interactive(fig)
    return


@app.cell
def _(KMeans, X_scaled, k_range, mo, np, silhouette_score):
    sil_scores = []
    for k1 in k_range:
        labels_temp = KMeans(n_clusters=k1, random_state=42, n_init=10).fit_predict(X_scaled)
        sil_scores.append(silhouette_score(X_scaled, labels_temp))

    best_k = k_range[np.argmax(sil_scores)]
    mo.md(f"**Best k by Silhouette:** {best_k} (score: {max(sil_scores):.3f})")
    return (sil_scores,)


@app.cell
def _(k_range, mo, np, plt, sil_scores):
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bars = ax2.bar(k_range, sil_scores, color='skyblue', edgecolor='navy')
    bars[np.argmax(sil_scores)].set_color('gold')
    ax2.set_xlabel('Number of Clusters (k)')
    ax2.set_ylabel('Silhouette Score')
    ax2.set_title('Silhouette Analysis')
    ax2.set_xticks(k_range)
    mo.mpl.interactive(fig2)
    return


@app.cell
def _(KMeans, X_scaled, k_selected, mo, silhouette_score):
    kmeans = KMeans(n_clusters=k_selected.value, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(X_scaled)

    # Calculate silhouette for selected k
    current_silhouette = silhouette_score(X_scaled, kmeans_labels)
    mo.md(f"### K-Means Results (k={k_selected.value})\n**Silhouette Score:** {current_silhouette:.3f}")
    return (kmeans,)


@app.cell
def _(feature_cols, kmeans, mo, pd, plt, sns):

    centers_df = pd.DataFrame(kmeans.cluster_centers_, columns=feature_cols)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.heatmap(centers_df.T, annot=True, fmt='.2f', cmap='RdYlBu_r', center=0, ax=ax3)
    ax3.set_title('Cluster Centers (Standardized Features)')
    mo.mpl.interactive(fig3)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
