## 0. Authors of the report
| Name | Contribution |
| :--- | :--- |
|Ahmed|  |
|Akash|  |
|Ilyas|  |
|Murat| Managed the team tasks and prepared the report. Cleaned the data and created features for the time of day. Built the Negative Binomial GLM and compared it against OLS and Poisson baselines to find the best model.|
|Viktoria|  |

## 1. Dataset Overview
> | Item                          | Description |
| :---                          | :--- |
| Dataset name                  | Metro_Interstate_Traffic_Volume.csv |
| Time period                   |  2012-10-02 09:00:00 to 2018-09-30 23:00:00|
| Sampling frequency            | Hourly (freq='h') |
| Number of rows                | 48,204 |
| Number of columns             |  9|
| Format file (.csv, .txt, etc) | .csv |
| Creator of the dataset        |  |
| Source (name)                 |  |
| Source (link)                 |  |


## 2. Dataset Structure
| Feature/variable | Data type | Description | Number of unique values | Example values |
| :---             | :---      | :---        | :---                    | :---           |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |


## 3. Data cleaning
| Issue                      | Names of columns affected | Description of the issue | Action taken |
| :---                       | :---                      | :---                     | :---         |
| Inconsistent column labeling | -                         | None observed            | -            |
| Wrong data types           | date_time                 | Loaded as object (string) instead of datetime | Converted using `pd.to_datetime` |
| Time gaps                  | date_time                 | Large gaps/missing periods in the full dataset | Filtered dataset to retain only contiguous data from 2016–2017 |
| Duplicates                 | -                         | None observed            | -            |
| Inconsistent categories    | weather_main              | Categorical text data (e.g., "Rain", "Squall") not usable by GLM | Applied One-Hot Encoding (`pd.get_dummies`) to create numeric binary columns |
| Other                      | temp, hour                | Temp was in Kelvin; Hour was linear (0-23) misrepresenting time cyclicity | Converted Temp to Celsius; Transformed Hour into Cyclic features (Sin/Cos) |

## 4. Descriptive statistics – numeric
|                        | Target variable | Predictor 1 | Predictor 2 | Predictor 3 | Predictor 4 |
| :---                   | :---           | :---        | :---        | :---        | :---        |
| Count                  |                |             |             |             |             |
| Mean                   |                |             |             |             |             |
| Standard deviation     |                |             |             |             |             |
| Min                    |                |             |             |             |             |
| 25%                    |                |             |             |             |             |
| 50%                    |                |             |             |             |             |
| 75%                    |                |             |             |             |             |
| Max                    |                |             |             |             |             |
| Variance               |                |             |             |             |             |
| Dispersion index (Variance / Mean)|                |             |             |             |             |
