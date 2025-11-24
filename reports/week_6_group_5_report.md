# World Bank Project Part 2: Correlation Analysis
**Group:** 5 
**Date:** November 24, 2025

---

## Introduction
Building on our previous comparative analysis of World Bank data, this report investigates the relationships between key development indicators. Specifically, we explore the link between :
- Infrastructure development (`Electricity Access`) and environmental sustainability (`Renewable Energy Consumption`). While traditional development theory suggests that advanced infrastructure facilitates greener technology, our analysis tests whether this holds true across the global economic spectrum.
- ...

---

## Research Question 1: The Energy Paradox
**RQ:** *Does universal access to electricity imply a transition to cleaner energy sources, or does it historically rely on non-renewable infrastructure?*

We hypothesized that as countries develop their power grids (higher access), they would utilize modern technology, leading to a positive correlation with renewable energy usage.

#### Data Inspection
We began by inspecting the distribution of our dependent variable, `renewvable_energy_consumption_percent`, using the `World Bank` dataset.

![Distribution of Renewable Energy](../additional_material/visualizations/week6/energy_paradox/Energy_paradox.png)
*Pic. 1: Distribution of Renewable Energy Consumption. The histogram displays a right-skewed distribution, indicating that the majority of nations have low renewable energy shares (< 20%). However, a distinct secondary cluster appears at the high end (> 80%), representing biomass-dependent nations. This non-normal shape confirms the need for Spearman correlation.*

**Observation:** The data is not normally distributed. It shows a clear polarization: countries tend to rely either heavily on fossil fuels (the left spike) or heavily on biomass (the right cluster). This skewness necessitated the use of the **Spearman** rank correlation test instead of Pearson.

#### Visualization
To investigate the relationship, we plotted `access_to_electricity_percent` against `renewvable_energy_consumption_percent`, coloring the data points by `income_group` to highlight economic disparities.

![alt text](../additional_material/visualizations/week6/energy_paradox/Energy_paradox2.png)
*Pic. 2: The Clean Energy Paradox. A scatter plot illustrating the relationship between electricity access and renewable energy consumption. Color coding by income group highlights a transition: low-income nations (purple) rely on traditional renewables, while high-income nations (yellow) have historically relied on non-renewable infrastructure to achieve universal access.*

**Observation:** The plot reveals a distinct negative curve. Low-income nations (purple) cluster at the top-left (Low Access, High Renewable), while high-income nations (yellow) cluster at the bottom-right (High Access, Low Renewable).

#### Statistical Test
We quantified the strength of this relationship using a Spearman correlation test via the Pingouin library to ensure statistical robustness.

![Spearman Correlation Matrix](../additional_material/visualizations/week6/energy_paradox/Energy_paradox3.png)
*Pic. 3: Spearman Correlation Matrix. The matrix displays the correlation coefficients between key development indicators.*

**Detailed Results (from Pingouin):**
* **Sample Size ($N$):** 188
* **Test:** Spearman Rank Correlation
* **Coefficient ($r$):** -0.60
* **95% Confidence Interval (CI):** [-0.69, -0.50]
* **Significance ($p$):** $4.51 \times 10^{-20}$ (Highly Significant)
* **Statistical Power:** ~1.0

**Analysis:** The analysis yields a strong negative correlation ($r = -0.60$). The 95% Confidence Interval indicates high precision, suggesting the true population correlation lies between -0.69 and -0.50. Additionally, a statistical power of 1.0 confirms that our sample size ($N=188$) was sufficient to reliably detect this effect.

#### Interpretation
The statistical analysis reveals a strong, significant negative correlation ($r = -0.60$) between electricity access and renewable energy consumption. This finding contradicts our initial hypothesis and highlights a "Clean Energy Paradox."

1.  **The "Green" Trap:** The high renewable pictures in low-income nations do not reflect advanced wind/solar technology but rather a reliance on "traditional biomass" (wood, charcoal) for survival.
2.  **The Cost of Access:** The transition to 100% electricity access (seen in high-income nations) has historically been powered by non-renewable fossil fuels (coal/gas), causing a sharp drop in renewable share as development increases.

**Correlation vs. Causation:**
This result does not imply that electricity *causes* a rejection of green energy. Rather, it reflects a historical developmental timeline: countries transition from biomass $\rightarrow$ fossil fuels to build reliable grids. The negative correlation captures the "middle phase" of industrialization where environmental sustainability is often traded for grid stability.

---

## Research Question 2: The Institutional Nexus
**RQ:** *Are countries that are good at fighting corruption also just generally good at running things? Does this link hold true no matter which continent you look at?*

We bet there's a nearly perfect match between low corruption and effective government globally. We expect that wherever you find less bribery and cleaner deals, you'll find better services

#### Data Inspection
We began by inspecting the distribution of our governance indicators using the World Bank dataset.


---
### Conclusion

The data confirms that the path to universal electricity access has historically led away from renewable sources. Furthermore, our extension analysis links this "traditional renewable" usage to lower life expectancy, suggesting that for developing nations, the 'green' energy of the past (biomass) was insufficient for a healthy life. Future development policies must actively break this pattern to ensure that emerging economies can achieve 100% access without replicating the fossil-fuel dependence of the current high-income nations.
