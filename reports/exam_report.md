## 0. Authors of the report
| Name | Contribution |
| :--- | :--- |
|Ahmed|  |
|Akash|  |
|Ilyas|  |
|Murat|  |
|Viktoria|  |

## 1. Dataset Overview
| Item                          | Description |
| :---                          | :--- |
| Dataset name                  |apartments_for_rent_classified_10K |
| Time period                   | December 2019 (Point-in-time snapshot based on the Unix timestamps in the time column) |
| Sampling frequency            |  Cross-sectional snapshot (Data was scraped as a one-time static collection, not updated daily/weekly)|
| Number of rows                |  10,000 listings|
| Number of columns             | 22 original variables |
| Format file (.csv, .txt, etc) | .csv (Comma-Separated Values, though technically formatted with a semicolon ; delimiter and cp1252/latin1 encoding) |
| Creator of the dataset        | Originally scraped from public rental platforms (e.g., RentLingo, Listanza), uploaded to this repository by user tarummurat. |
| Source (name)                 |  Hugging Face Datasets|
| Source (link)                 |  https://www.google.com/search?q=https://huggingface.co/datasets/tarummurat/apartments_for_rent_classified_10K|


## 2. Dataset Structure
| Feature/variable | Data type      | Description | Number of unique values | Example values |
| :---             | :---           | :---        | :---                    | :---           |
|    price         |Numeric (Float) |The monthly rental cost in USD (Target Variable)|1,600|1200, 1500, 2150|
|square_feet       |Numeric (Float) |Total living area of the apartment in square feet|18,00|750, 1000, 1250|
|  bathrooms       |Numeric (Float) |Number of bathrooms available in the unit|15|1.0, 1.5, 2.0|
| bedrooms         |Numeric (Float) |Number of sleeping rooms available in the unit|10|1.0, 2.0, 3.0|
|cityname          |Text (String)   |The city where the apartment is located|15,00|Austin, Seattle, Dallas|
|State             |Text (String)   |The US State abbreviation|51|TX, CA, WA|
|latitude          |Numeric (Float)|Geographic latitude coordinate for mapping|8,000|30.2672, 38.9057|
|longitude         |Numeric (Float)|Geographic longitude coordinate for mapping|8,000|-97.7431, -76.9861|
|has_photo         |Text (String)|Indicates the type/presence of visual marketing media|3|Thumbnail, Yes, No|
|pets_allowed      |Text (String)|The landlord's policy regarding animals|3|Cats,Dogs, Dogs, None|
|amenities         |Text (String)|Comma-separated list of building/unit features|3,200|AC, Gym, Pool, Parking|
|time              |Numeric (Int)|Listing creation timestamp (Unix format).|9,500|1577359415|
|body              |Text (String)|Unstructured text description provided by the lister.|9,900|"Beautiful 2 bed 1 bath..."|

## 3. Data cleaning
| Issue                      | Names of columns affected | Description of the issue | Action taken |
| :---                       | :---                      | :---                     | :---         |
| Inconsistent column labeling |All columns (during load)|The raw CSV file had formatting issues, specifically using a semicolon (;) delimiter and cp1252 encoding, which can cause loading errors|Handled directly during the initial data loading phase by specifying sep=';' and encoding='cp1252' in pd.read_csv()|
| Wrong data types           |time|The time column is in Unix timestamp format (integer) rather than a readable DateTime format|Left as int64 since the data is a static cross-sectional snapshot and no time-series forecasting was performed|
| Time gaps                  |time|The dataset is a snapshot (predominantly from December 2019) rather than a continuous time series|No action needed. Acknowledged as a single point-in-time dataset|
| Duplicates                 |All columns|Checked the dataset for completely identical/duplicated rows|Evaluated using df.duplicated().sum(). The result was 0, meaning no duplicates existed, so no rows were removed|
| Inconsistent categories    |price_type, has_photo, category|1. price_type contained 'Weekly', 'Daily', and 'Yearly' instead of just Monthly


2. has_photo used the category 'Thumbnail' alongside 'Yes' and 'No'


3. category contained a few 'home' and 'short_term' outliers|1. Mathematically converted prices to a monthly standard (e.g., Weekly * 4), then dropped the price_type column


2. Replaced 'Thumbnail' with 'Yes'


3. Dropped the rows for 'home'/'short_term', then dropped the category column entirely|
| Other (Missing values & Outliers)|bathrooms, bedrooms, pets_allowed|Small amount of NaN values in structural columns, physically impossible values (0 bathrooms), and gaps in pet policies.|Dropped rows with missing bathrooms/bedrooms. Dropped rows where bathrooms == 0. Filled missing pets_allowed with "Not specified"|
|Other (Single-Value Dominance)|currency, source, fee, is_studio|fee, is_studio	Columns contained >90% identical values (e.g., currency was 100% USD, fee was 100% No), providing no mathematical variance for analysis|Dropped these columns entirely from the dataset to reduce noise and dimensionality|

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


---

## Introduction
...

---
## Methodological limitations
This analysis is based on observational data from a sample of 10,000 rental listings and should be interpreted with caution. 
The relationships we identify are statistical associations, not causal effects. 
Important factors such as neighbourhood quality, proximity to public transport, or building condition are not included in the dataset and may influence rental prices. 
Moreover, the reported prices reflect advertised listings rather than final contract prices, which may limit the accuracy of price-related conclusions.

...

The sample represents a fixed subset of listings and may not fully capture the diversity of the entire U.S. rental market.
Therefore, the findings indicate general patterns in this dataset, but they should not be generalized to the entire housing market without further validation.

---
## Research Question 1: In which square footage and price range is the highest density of rental inventory concentrated, and what does this reveal about the 'standard' apartment in the market?
**RQ:** *xxxxx*



---
## Research Question 2:  How do apartment size and bedroom count influence the price per square foot across the rental market, and at what point does 'bulk value' peak for renters?
**RQ:** *xxxxx*

## Research Question 3: Is there a 'sweet spot' in the rental market where size, location, and amenities offer the best value for money?
**RQ:** *xxxxx*

---

## AI disclaimer
AI tools were used to improve the clarity, structure, and grammatical accuracy of the written text.

...
