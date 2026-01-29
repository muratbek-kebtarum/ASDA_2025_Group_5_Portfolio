import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("https://raw.githubusercontent.com/muratbek-kebtarum/ASDA_2025_Group_5_Portfolio/refs/heads/main/additional_material/datasets/week11/6.3.3_spotify_5000_songs.csv")
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
