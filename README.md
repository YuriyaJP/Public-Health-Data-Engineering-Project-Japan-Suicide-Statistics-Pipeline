# Japan Suicide Statistics Forecasting, Economic and Policy Impact Analysis

This project builds a sustainable, automated pipeline for Japan police suicide statistics, providing interactive dashboards, time-series forecasting, and economic impact analysis to inform public health interventions.

Read the full article about my porject here : https://forum.effectivealtruism.org/posts/Sg7ovepZcmY8GKpo3/how-i-attempted-to-measure-the-impact-of-my-nonprofit-s

## Features
- **Data Engineering:** Web scraping, cleaning, and building a self-updating pipeline.  
- **Data Visualization:** Interactive dashboards showing demographic and temporal trends.  
- **Time-Series Forecasting:** Linear regression and ARIMA models to predict suicide trends by age and gender. I attempted time series forecasting for age-specific suicide counts using Prophet. However, due to the small dataset and high variability in some age groups, predictive performance was poor (R² negative).
- **Economic Impact Analysis:** Estimates lost lifetime tax revenue and productivity to quantify cost-effectiveness of interventions.  
- **Policy-Relevant Outputs:** Scenario modeling to project the effects of school, workplace, and regional interventions.

## Dataset
The dataset contains historical Japan police suicide statistics, segmented by:
- Year (converted from Japanese eras to Gregorian)  
- Age group  
- Gender  
- Suicide counts  
- Cause classification  

Cleaned datasets are available in the `data_processed/` folder.

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
- `data_processed/*.csv`  
  - Cleaned source datasets ready for analysis
  - Contains data collection and cleaning

## Usage
Install dependencies:  
```bash
requirements.txt
