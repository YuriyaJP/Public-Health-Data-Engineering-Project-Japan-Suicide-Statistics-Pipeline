# Japan Suicide Statistics Forecasting and Policy Impact Analysis

This project builds a sustainable, automated pipeline for Japan police suicide statistics, providing interactive dashboards, time-series forecasting, and economic impact analysis to inform public health interventions.

## Features
- **Data Engineering:** Web scraping, cleaning, and building a self-updating pipeline.  
- **Data Visualization:** Interactive dashboards showing demographic and temporal trends.  
- **Time-Series Forecasting:** Linear regression and ARIMA models to predict suicide trends by age and gender.  
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
- `suicide_pipeline.ipynb`  
  - Implements data cleaning, dashboard creation, and forecasting  
  - Contains regression and ARIMA modeling  
  - Computes economic impact metrics and scenario simulations  
- `data_processed/*.csv`  
  - Cleaned source datasets ready for analysis  

## Usage
Install dependencies:  
```bash
pip install numpy pandas matplotlib seaborn statsmodels plotly
