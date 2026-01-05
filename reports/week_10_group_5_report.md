<details>
<summary><span style="font-size: 25px; font-weight: bold">
          0. Authors of the report
      </span></summary>

| Name | Contribution |
| :--- | :--- |
|Ahmed|  |
|Akash|  |
|Ilyas|  |
|Murat|Data analysis, Visualization, Report assembly|
|Viktoria|  |

</details>

<details>
<summary><span style="font-size: 25px; font-weight: bold">
          1. Dataset Overview
      </span></summary>

| Item                          | Description |
| :---                          | :--- |
| Dataset name                  | World Happiness dataset |
| Time period                   | 2018 (as provided in the attached CSV) |
| Sampling frequency            | Yearly |
| Number of rows                | 156 |
| Number of columns             | 9 |
| Format file (.csv, .txt, etc) | .csv |
| Creator of the dataset        | - |
| Source (name)                 | - |
| Source (link)                 | [link](https://github.com/datagus/ASDA2025/tree/main/datasets/homework_week10) |

</details>

<details>
<summary><span style="font-size: 25px; font-weight: bold">
          2. Dataset Structure
      </span></summary>

| Feature/variable                | Data type | Description                                                                 | Number of unique values | Example values |
| :------------------------------ | :-------- | :-------------------------------------------------------------------------- | :---------------------- | :------------- |
| Overall rank                    | Integer   | List of ranks of different countries from 1 to 156                           | 156                     | 1              |
| Country or region               | String    | List of the names of different countries                                     | 156                     | Finland        |
| Score                           | Float     | List of happiness scores of different countries                              | 154                     | 7.632          |
| GDP per capita                  | Float     | The GDP per capita score of different countries                              | 147                     | 1.305          |
| Social support                  | Float     | The social support of different countries                                    | 146                     | 1.592          |
| Healthy life expectancy         | Float     | The healthy life expectancy of different countries                           | 143                     | 0.874          |
| Freedom to make life choices    | Float     | The score of perception of freedom of different countries                    | 136                     | 0.681          |
| Generosity                      | Float     | Generosity (the quality of being kind and generous) score                    | 122                     | 0.202          |
| Perceptions of corruption       | Float     | The score of the perception of corruption in different countries             | 111                     | 0.393          |             |

</details>

<details>
<summary><span style="font-size: 25px; font-weight: bold">
          3. Data cleaning
      </span></summary>

| Issue                     | Names of columns affected | Description of the issue                            | Action taken |
| :------------------------ | :------------------------ | :-------------------------------------------------- | :----------- |
| Inconsistent column labeling | None                      | Column names are consistent and descriptive         | None needed  |
| Wrong data types          | None                      | All numeric columns are floats/ints as expected     | None needed  |
| Time gaps                 | N/A                       | Dataset is cross-sectional (single year)            | None needed  |
| Duplicates                | All                       | No duplicate rows found                             | None needed  |
| Inconsistent categories   | Country or region         | All country names are unique strings               | None needed  |
| Other                     | None                      | No missing values (NaN) found in dataset            | None needed  |

</details>

<details>
<summary><span style="font-size: 25px; font-weight: bold">
          4. Descriptive statistics
      </span></summary>

|                         | Target variable (Score) | Predictor 1 (GDP per capita) | Predictor 2 (Social support) | Predictor 3 (Healthy life expectancy) | Predictor 4 (Freedom to make life choices) |
| :---------------------- | :---------------------- | :--------------------------- | :--------------------------- | :------------------------------------ | :----------------------------------------- |
| Count                   | 156.0                   | 156.0                        | 156.0                        | 156.0                                 | 156.0                                      |
| Mean                    | 5.376                   | 0.891                        | 1.213                        | 0.597                                 | 0.455                                      |
| Standard deviation      | 1.120                   | 0.392                        | 0.302                        | 0.248                                 | 0.162                                      |
| Min                     | 2.905                   | 0.000                        | 0.000                        | 0.000                                 | 0.000                                      |
| 25%                     | 4.454                   | 0.616                        | 1.067                        | 0.422                                 | 0.356                                      |
| 50%                     | 5.378                   | 0.950                        | 1.255                        | 0.644                                 | 0.487                                      |
| 75%                     | 6.169                   | 1.198                        | 1.463                        | 0.777                                 | 0.579                                      |
| Max                     | 7.632                   | 2.096                        | 1.644                        | 1.030                                 | 0.724                                      |
| Variance                | 1.253                   | 0.154                        | 0.091                        | 0.061                                 | 0.026                                      |
| Dispersion index (Variance / Mean) | 0.233            | 0.172                        | 0.075                        | 0.103                                 | 0.058                                      |


</details>
<details>
<summary>
    <span style="font-size: 25px; font-weight: bold">
     Main Conclusions
</span>
</summary>
   <span style="font-size: 20px; font-weight: bold">
    Q1 & Q2: Regional Groups & Patterns</span>
<br>
<span style="font-size: 16px; font-weight: bold">Do countries in the same region stay together? </span>
<br> Yes. As you can see in the plot below, regions form clear groups. This happens because countries in the same region often have similar levels of development.
<br>
<ul> 
<li><span style="color: #0145a5ff">Western Europe (Blue) </span> : Usually has high scores on PC1 (Wealth & Stability).
<li><span style="color: #a59d01ff">Sub-Saharan Africa (Yellow): </span> Usually has low scores on PC1.
<li><span style="color: grey">South Asia (Grey):</span> Is spread out across PC2 (Generosity & Freedom).
<br>

 ![PCA Plot](../additional_material/visualizations/week10/world_hapiness_pca_region.png)

<hr>

   <span style="font-size: 20px; font-weight: bold">Q3: Finding Unusual Countries (Outliers)</span>
   <span style="font-size: 16px; font-weight: bold">Are some countries different from their neighbors? </span>
   Yes. We found a few countries that do not follow the usual pattern of their region.
<span style="font-size: 16px; font-weight: bold">Case A: Latin America (The "Wealthy" Exceptions)</span>
Most Latin American countries have average scores for Wealth and Stability (PC1). However, three countries are much higher. They look more like Western European countries.
| Country      | PC1 Score (Wealth/Stability) | Regional Average | Status         |
| :----------- | :--------------------------- | :--------------- | :------------- |
| Costa Rica   | 1.31                         | 0.87             | High Outlier   |
| Uruguay      | 1.47                         | 0.87             | High Outlier   |
| Panama       | 1.05                         | 0.87             | High Outlier   |

<b>Conclusion:</b> These countries are richer and have better social support than their neighbors.
<hr>
Case B: South Asia (The "Generous" Exceptions)
South Asia usually has lower happiness scores. But, three countries have very high scores for Generosity and Freedom (PC2).

| Country      | PC2 Score (Generosity/Freedom) | Regional Average | Status          |
| :----------- | :------------------------------ | :--------------- | :-------------- |
| Bhutan       | High                            | Low/Average      | Social Outlier  |
| Nepal        | High                            | Low/Average      | Social Outlier  |
| Uzbekistan   | High                            | Low/Average      | Social Outlier  |

<b>Conclusion:</b> People in these countries feel more free and generous than others in the region, even though their economy is similar.
</details>