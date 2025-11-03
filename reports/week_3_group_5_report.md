# Lego inventory cleaning

## Project Report

### 1. Dataset Overview

| Item                     | Description |
|--------------------------|-------------|
| Dataset name                 | Lego Dataset                  |
| Authors                      |Leuphana University of Lüneburg|
| Number of entries            | 189                           |
| Number of features/variables | 10                            |
| Format file (.csv,.txt, etc) | .xlsx                         |

*This dataset contains detailed information about Lego pieces, including color, type, shape, size, and material properties.*

---

### 2. Dataset Structure

| Feature / Variable | Data Type | Description | Unique Values | Example Values |
|------------------|-----------|-------------|----------------|----------------|
| id | int64 | Unique identifier for each brick | 189 | 1, 2, 3 |
| color | object | Color of the brick | 63 | darkblue, green, coral |
| is duplo? | bool | Indicates if the brick is Duplo | 2 | True, False |
| size type | object | Type of brick size category | 3 | brick, plate |
| base shape | object | Shape of the brick base | 8 | rectangle, square |
| base dimensions | object | Stud dimension of brick base (W × L) | 22 | 2X4, 2X2, 1X4 |
| number of studs | int64 | Count of studs on top | 10 | 4, 8, 16 |
| has slope? | bool | Whether the brick has a slope | 2 | True, False |
| slope degree | float64 | Slope angle for sloped bricks | 3 | 33, 45, 60 |
| in stock | int64 | Inventory amount of the brick | 3 | 1, 2, 3 |



---

### 3. Descriptive statistics

**Numeric columns**

| | id | number of studs | slope degree | in stock |
|:---|:---|:---|:---|:---|
| **count** | 189.000000 | 189.000000 | 189.000000 | 189.000000 |
| **mean** | 95.000000 | 5.375661 | 1.198413 | 1.185185 |
| **std** | 54.743037 | 3.525547 | 7.995963 | 0.457850 |
| **min** | 1.000000 | 0.000000 | 0.000000 | 1.000000 |
| **25%** | 48.000000 | 2.000000 | 0.000000 | 1.000000 |
| **50%** | 95.000000 | 4.000000 | 0.000000 | 1.000000 |
| **75%** | 142.000000 | 8.000000 | 0.000000 | 1.000000 |
| **max** | 189.000000 | 24.000000 | 45.000000 | 3.000000 |

---
### 4. Exploratory plots

| Plot Name | Description |
|------------|-------------|
| Color Distribution | Shows the frequency of Lego pieces by color, highlighting yellow as the most common. |
| Type Distribution | Displays proportions of different Lego types (Brick, Plate, Tile). |
| Shape Distribution | Highlights the dominance of rectangular and square shapes. |
| Stud Count Distribution | Visualizes the distribution of the number of studs among Lego pieces. |

---
### 5. Data cleaning procedure
---
#### 5.1 Major data inconsistencies:

| Issue | Columns affected | Description | Action Taken |
|--------|------------------|-------------|---------------|
| Inconsistent column labeling | All | Mixed casing and extra spaces in headers | Standardized column names to lowercase with underscores |
| Wrong data types | slope degree, in stock | Numeric fields stored as strings | Converted to appropriate numeric types |
| Missing values | slope degree, color | Some slope values missing for non-sloped bricks | Filled with 0 or “N/A” as appropriate |
| Duplicates | All except id | Duplicate Lego entries found | Removed duplicate rows |
| Inconsistent categories | color | Variations like “Blck” and “Black” | Standardized spelling and lowercase |

#### 5.2 Minor data inconsistencies
Some uncommon color names (e.g., “transparent sky blue”) were normalized but kept due to their uniqueness.

---

### 6. Recommendations for good practices regarding data collection

- Maintain consistent column naming conventions (snake_case).  
- Ensure categorical values follow a fixed reference list (e.g., color names).  
- Validate data types during import to prevent string–numeric mismatches.  
- Document assumptions about missing values and category normalization.  
- Regularly visualize the dataset to detect anomalies early.

### 7. AI Disclaimer

*AI assistance was used during data merging, specifically to resolve duplicate records and merge conflicts, ensuring a clean and consistent dataset.*