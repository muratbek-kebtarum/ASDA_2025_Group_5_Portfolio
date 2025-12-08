## 0. Authors of the report
| Name | Contribution |
| :--- | :--- |
|Ahmed|Report Participation & Date Cleaning & Data Visalizations &  Built the Negative Binomial GLM and compared it against OLS and Poisson baselines to find the best model|
|Akash|  |
|Ilyas|  |
|Murat| Managed the team tasks and prepared the report. Cleaned the data and created features for the time of day. Built the Negative Binomial GLM and compared it against OLS and Poisson baselines to find the best model.|
|Viktoria|  |

## 1. Dataset Overview
| Item                          | Description |
| :---                          | :--- |
| Dataset name                  | Metro_Interstate_Traffic_Volume.csv |
| Time period                   |  2012-10-02 09:00:00 to 2018-09-30 23:00:00|
| Sampling frequency            | Hourly  |
| Number of rows                | 48,204 |
| Number of columns             |  9|
| Format file (.csv, .txt, etc) | .csv |
| Creator of the dataset        | John Hogue |
| Source (name)                 |Metro Interstate Traffic Volume  |
| Source (link)                 | https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume |



## 2. Dataset Structure
| Feature/variable | Data type    | Description                                              | Number of unique values | Example values                           |
| :---             | :---        | :---                                                     | :---                    | :---                                     |
| rain1h           | float       | Precipitation in the last hour (mm)                     | many (continuous)       | 0.05, 0.09, 1.78                         |
| trafficvolume    | int         | Number of vehicles observed in the hour                 | many (continuous)       | 43522, 45518, 47569                      |
| tempcelsius      | float       | Air temperature in degrees Celsius                      | many (continuous)       | 0.0, 10.0, 11.0                          |
| isholiday        | int (0/1)   | Indicator whether the hour is on a holiday (1) or not   | 2                       | 0, 1                                     |
| hoursin          | float       | Sine transform of hour of day (cyclical encoding)       | many (−1 to 1)          | 0.0, 0.5, −0.5                           |
| hourcos          | float       | Cosine transform of hour of day (cyclical encoding)     | many (−1 to 1)          | 1.0, 0.71, −1.0                          |
| daysin           | float       | Sine transform of day-of-week (cyclical encoding)       | many (−1 to 1)          | 0.78, 0.97, −0.43                        |
| daycos           | float       | Cosine transform of day-of-week (cyclical encoding)     | many (−1 to 1)          | 0.62, −0.22, −0.90                       |
| weathercloudy    | bool (0/1)  | Indicator for cloudy weather condition                  | 2                       | False, True                              |
| weatherfoggy     | bool (0/1)  | Indicator for foggy weather condition                   | 2                       | False, True                              |
| weatherrainy     | bool (0/1)  | Indicator for rainy weather condition                   | 2                       | False, True                              |
| weathersnowy     | bool (0/1)  | Indicator for snowy weather condition                   | 2                       | False, True                              |
| weatherstormy    | bool (0/1)  | Indicator for stormy weather condition                  | 2                       | False, True                              |


## 3. Data cleaning
| Issue                      | Names of columns affected | Description of the issue | Action taken |
| :---                       | :---                      | :---                     | :---         |
| Inconsistent column labeling | -                         | None observed            | -            |
| Wrong data types           | date_time                 | Loaded as object (string) instead of datetime | Converted using `pd.to_datetime` |
| Time gaps                  | date_time                 | Large gaps/missing periods in the full dataset | Filtered dataset to retain only contiguous data from 2016–2017 |
| Duplicates                 | -                         | None observed            | -            |
| Inconsistent categories    | weather_main              | Categorical text data (e.g., "Rain", "Squall") not usable by GLM | Applied One-Hot Encoding (`pd.get_dummies`) to create numeric binary columns |
| Other                      | temp, hour,Day               | Temp was in Kelvin;Day_0f_week was linear(0-7);Hour was linear (0-23) misrepresenting time cyclicity | Converted Temp to Celsius; Transformed Hour into Cyclic features (Sin/Cos) |

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
