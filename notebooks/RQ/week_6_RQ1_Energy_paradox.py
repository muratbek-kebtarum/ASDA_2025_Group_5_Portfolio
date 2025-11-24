import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np

# Set the visual style for professional plots
sns.set_theme(style="whitegrid")

# 1. Load Data
# Ensure 'filtered.csv' is in the same folder as this notebook
df = pd.read_csv('../additional_material/filtered.csv')

# ==========================================
# FIGURE 1: DATA INSPECTION (Histogram)
# ==========================================
plt.figure(figsize=(8, 5))
sns.histplot(df['renewvable_energy_consumption_percent'], bins=20, kde=True, color='teal')
plt.title('Data Inspection: Distribution of Renewable Energy', fontsize=14)
plt.xlabel('Renewable Energy Consumption (%)')
plt.ylabel('Number of Countries')
plt.tight_layout()
plt.savefig('figure1_inspection.png')
plt.show()

# ==========================================
# FIGURE 2: VISUALIZATION (Energy Paradox Scatter)
# ==========================================
plt.figure(figsize=(10, 6))
income_order = ['Low', 'Lower_middle', 'Upper_middle', 'High']

sns.scatterplot(
    data=df,
    x='access_to_electricity_percent',
    y='renewvable_energy_consumption_percent',
    hue='income_group',
    hue_order=income_order,
    palette='viridis',
    s=100, alpha=0.7, edgecolor='black'
)

plt.title('The Clean Energy Paradox', fontsize=14)
plt.xlabel('Access to Electricity (%)')
plt.ylabel('Renewable Energy Consumption (%)')
plt.legend(title='Income Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('figure2_visualization.png') # Matches the report link
plt.show()

# ==========================================
# STATISTICAL TEST (Detailed Pingouin Stats)
# ==========================================
# We calculate this to get the numbers for the text (r, p-value, CI, Power)
stats_data = df.dropna(subset=['access_to_electricity_percent', 
                               'renewvable_energy_consumption_percent'])

stats = pg.corr(
    x=stats_data['access_to_electricity_percent'],
    y=stats_data['renewvable_energy_consumption_percent'],
    method='spearman'
)
print(stats)
print("-" * 30)
print("MAIN RQ STATISTICS (Pingouin):")
print("-" * 30)
display(stats) # Prints the table with r, CI95%, p-val, power

# ==========================================
# FIGURE 3: STATISTICAL TEST (Heatmap)
# ==========================================
cols = ['access_to_electricity_percent', 'renewvable_energy_consumption_percent', 'gdp_current_us']
heatmap_data = df[cols].dropna()
heatmap_data.columns = ['Electricity Access', 'Renewable %', 'GDP']

plt.figure(figsize=(6, 5))
sns.heatmap(
    heatmap_data.corr(method='spearman'), # Spearman for skewed data
    annot=True,
    fmt='.2f',
    cmap='RdBu_r',
    vmin=-1, vmax=1,
    cbar_kws={'label': 'Correlation Strength'}
)
plt.title('Statistical Test (Spearman Correlation)', fontsize=14)
plt.tight_layout()
plt.savefig('figure3_stats.png')
plt.show()

