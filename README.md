# Japan Suicide Statistics Forecasting, Economic and Policy Impact Analysis

This project builds a sustainable, automated pipeline for Japan police suicide statistics, providing interactive dashboards, time-series forecasting, and economic impact analysis to inform public health interventions.

Read the full article about my porject here : https://forum.effectivealtruism.org/posts/Sg7ovepZcmY8GKpo3/how-i-attempted-to-measure-the-impact-of-my-nonprofit-s

## Features
- **Data Engineering:** Web scraping (script only, website banned), cleaning, and building comprehensive dataset.  
- **Data Visualization:** Interactive dashboards showing demographic and temporal trends for the youth rates.  
- **Economic Impact Analysis:** Estimates lost lifetime tax revenue and productivity to quantify cost-effectiveness of intervention.  

## Dataset
The dataset contains historical Japan police suicide statistics, segmented by:
- Year (converted from Japanese eras to Gregorian)  
- Age group  
- Gender  
- Suicide and attempted suicide counts  
- Cause classification  

Cleaned datasets are available in the `data_clean/` folder.

## Preprocessing
- Japanese era conversion (昭和, 平成, 令和 → Gregorian years)  
- Aggregation by age, gender, and cause  
- Handling missing values and standardizing categorical features  

## Key Files
- `suicide-data-viz.ipynb`
  - Evidence synthesis (age, gender, reason cross-analysis)
  - Critical analysis (identify patterns and anomalies)
  - Economic Impact Analysis
- `time-series-forecast.ipynb`  
  - Contains regression, XGBoost, Prophet and ARIMA modeling all with poor results 
- `data_clean/*.csv`  
  - Cleaned source datasets ready for analysis
  - `suicide_prevention_report.py`
    - Extracts key economic and epidemiological metrics from the suicide prevention visualization pipeline for downstream reporting and analysis workflows.

## Usage
Install dependencies:  
```bash
requirements.txt
