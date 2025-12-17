"""
Metric Extraction Pipeline for Economic Impact Analysis
========================================================

This module extracts key economic and epidemiological metrics from the 
suicide prevention visualization pipeline for downstream reporting and 
analysis workflows.

Author: Public Health Data Engineering Project
Purpose: Generate structured metric outputs for policy reporting
"""

import pandas as pd
import numpy as np
import json
import sys
import os

sys.path.append('../../')
import assumptions


def load_and_prepare_data():
    """
    Load raw data files and apply standardized transformations.
    
    Returns:
        tuple: (df_age, df_gender, df_cause) - cleaned dataframes
    """
    df_age = pd.read_csv("../../data_clean/age_cleaned.csv")
    df_gender = pd.read_csv("../../data_clean/gender_cleaned.csv")
    df_cause = pd.read_csv("../../data_clean/reason_cleaned.csv")
    
    # Standardize gender data column names
    df_gender = df_gender.rename(columns={
        '自殺者_総数': 'total',
        '自殺者_男性': 'male',
        '自殺者_女性': 'female'
    })
    
    for col in ['total', 'male', 'female']:
        df_gender[col] = pd.to_numeric(df_gender[col], errors='coerce')
    df_gender.dropna(inplace=True)
    
    # Translate and clean cause categories
    issue_translation = {
        'その他': 'Other',
        '交男際（女男問女）題問題': 'Relationship issues',
        '健康問題': 'Health issues',
        '勤務問題': 'Work-related issues',
        '学校問題': 'School issues',
        '家庭問題': 'Family issues',
        '経済・生活問題': 'Economic / Life issues'
    }
    
    df_cause['cause'] = df_cause['問題分類'].map(issue_translation)
    df_cause['count'] = pd.to_numeric(df_cause['人数'], errors='coerce')
    df_cause.dropna(subset=['cause', 'count'], inplace=True)
    
    # Standardize age group labels
    df_age = df_age.rename(columns={'年齢層': 'age_group', '人数': 'suicides'})
    
    age_map = {
        '0～9歳': '0-9', '10～19歳': '10-19', '20～29歳': '20-29',
        '30～39歳': '30-39', '40～49歳': '40-49', '50～59歳': '50-59',
        '60～69歳': '60-69', '70～79歳': '70-79', '80歳以上': '80+'
    }
    
    df_age['age_group'] = df_age['age_group'].map(age_map)
    df_age['suicides'] = pd.to_numeric(df_age['suicides'], errors='coerce')
    df_age.dropna(inplace=True)
    
    return df_age, df_gender, df_cause


def calculate_economic_impact(df_age):
    """
    Calculate economic loss metrics using human capital approach.
    
    Args:
        df_age: DataFrame with age-stratified suicide counts
        
    Returns:
        DataFrame: Extended metrics including economic impact and policy scenarios
    """
    df_age_total = df_age.groupby('age_group', as_index=False)['suicides'].sum()
    
    df_age_total['lifetime_earnings_yen'] = df_age_total['age_group'].apply(
        lambda a: assumptions.SALARY_BY_AGE.get(a, 0) * assumptions.WORK_YEARS_LEFT.get(a, 0)
    )
    
    df_econ = df_age_total.copy()
    df_econ['annual_loss_yen'] = df_econ['suicides'] * df_econ['lifetime_earnings_yen']
    
    df_policy = df_econ.copy()
    df_policy['loss_prevented'] = df_policy['annual_loss_yen'] * assumptions.SUICIDE_REDUCTION_RATE
    df_policy['intervention_cost'] = df_policy['age_group'].map(assumptions.INTERVENTION_COST_BY_AGE)
    df_policy['roi'] = df_policy['loss_prevented'] / df_policy['intervention_cost']
    df_policy['baseline_loss'] = df_policy['annual_loss_yen'].apply(assumptions.baseline_loss)
    df_policy['reduced_loss'] = df_policy['annual_loss_yen'].apply(assumptions.reduced_loss)
    df_policy['net_benefit'] = df_policy['loss_prevented'] - df_policy['intervention_cost']
    
    return df_policy


def extract_summary_metrics(df_policy):
    """
    Generate aggregate economic and intervention metrics.
    
    Args:
        df_policy: DataFrame with full economic impact calculations
        
    Returns:
        dict: Summary statistics for overall economic burden and intervention impact
    """
    return {
        'total_annual_loss_yen': float(df_policy['annual_loss_yen'].sum()),
        'total_annual_loss_billion': float(df_policy['annual_loss_yen'].sum() / 1e9),
        'total_suicides': int(df_policy['suicides'].sum()),
        'total_loss_prevented_yen': float(df_policy['loss_prevented'].sum()),
        'total_loss_prevented_billion': float(df_policy['loss_prevented'].sum() / 1e9),
        'total_intervention_cost_yen': float(df_policy['intervention_cost'].sum()),
        'total_intervention_cost_billion': float(df_policy['intervention_cost'].sum() / 1e9),
        'total_net_benefit_yen': float(df_policy['net_benefit'].sum()),
        'total_net_benefit_billion': float(df_policy['net_benefit'].sum() / 1e9),
        'overall_roi': float(df_policy['loss_prevented'].sum() / df_policy['intervention_cost'].sum()),
        'intervention_effectiveness_rate': assumptions.SUICIDE_REDUCTION_RATE,
        'avg_lifetime_earnings_million': float(df_policy['lifetime_earnings_yen'].mean() / 1e6)
    }


def extract_age_breakdown(df_policy):
    """
    Generate detailed metrics stratified by age group.
    
    Args:
        df_policy: DataFrame with economic impact by age
        
    Returns:
        list: Dictionaries containing age-specific metrics
    """
    age_breakdown = []
    
    for _, row in df_policy.iterrows():
        age_breakdown.append({
            'age_group': row['age_group'],
            'total_suicides': int(row['suicides']),
            'baseline_loss_yen': float(row['baseline_loss']),
            'baseline_loss_billion': float(row['baseline_loss'] / 1e9),
            'loss_per_person_yen': float(row['lifetime_earnings_yen']),
            'loss_per_person_million': float(row['lifetime_earnings_yen'] / 1e6),
            'intervention_cost_yen': float(row['intervention_cost']),
            'intervention_cost_billion': float(row['intervention_cost'] / 1e9),
            'loss_prevented_yen': float(row['loss_prevented']),
            'loss_prevented_billion': float(row['loss_prevented'] / 1e9),
            'reduced_loss_yen': float(row['reduced_loss']),
            'reduced_loss_billion': float(row['reduced_loss'] / 1e9),
            'net_benefit_yen': float(row['net_benefit']),
            'net_benefit_billion': float(row['net_benefit'] / 1e9),
            'roi': float(row['roi']),
            'salary_yen': assumptions.SALARY_BY_AGE[row['age_group']],
            'work_years_left': assumptions.WORK_YEARS_LEFT[row['age_group']]
        })
    
    return age_breakdown


def extract_working_age_metrics(df_policy):
    """
    Calculate aggregate metrics for working-age population (20-59 years).
    
    Args:
        df_policy: DataFrame with economic impact by age
        
    Returns:
        dict: Working-age specific economic burden and intervention metrics
    """
    working_age_groups = ['20-29', '30-39', '40-49', '50-59']
    df_working = df_policy[df_policy['age_group'].isin(working_age_groups)]
    
    return {
        'total_suicides': int(df_working['suicides'].sum()),
        'total_loss_yen': float(df_working['annual_loss_yen'].sum()),
        'total_loss_billion': float(df_working['annual_loss_yen'].sum() / 1e9),
        'percent_of_total_loss': float(
            df_working['annual_loss_yen'].sum() / df_policy['annual_loss_yen'].sum() * 100
        ),
        'avg_roi': float(df_working['roi'].mean())
    }


def extract_gender_summary(df_gender):
    """
    Generate gender-stratified suicide statistics.
    
    Args:
        df_gender: DataFrame with gender-disaggregated counts
        
    Returns:
        dict: Gender distribution metrics
    """
    return {
        'total_deaths': int(df_gender['total'].sum()),
        'male_deaths': int(df_gender['male'].sum()),
        'female_deaths': int(df_gender['female'].sum()),
        'male_percentage': float(df_gender['male'].sum() / df_gender['total'].sum() * 100),
        'female_percentage': float(df_gender['female'].sum() / df_gender['total'].sum() * 100)
    }


def extract_top_causes(df_cause, n=5):
    """
    Identify leading causes of suicide by frequency.
    
    Args:
        df_cause: DataFrame with cause-specific counts
        n: Number of top causes to return
        
    Returns:
        list: Top N causes with counts and percentages
    """
    cause_summary = df_cause.groupby('cause')['count'].sum().sort_values(ascending=False)
    top_causes = []
    
    for cause, count in cause_summary.head(n).items():
        top_causes.append({
            'cause': cause,
            'total_deaths': int(count),
            'percentage': float(count / cause_summary.sum() * 100)
        })
    
    return top_causes


def extract_temporal_trends(df_age):
    """
    Calculate year-over-year suicide trends if temporal data available.
    
    Args:
        df_age: DataFrame with time-indexed suicide counts
        
    Returns:
        tuple: (yearly_trends dict, years_available list)
    """
    if 'year' in df_age.columns:
        yearly_trends = df_age.groupby('year')['suicides'].sum().to_dict()
        years_available = sorted(df_age['year'].unique().tolist())
    else:
        yearly_trends = {}
        years_available = []
    
    return yearly_trends, years_available


def convert_to_native_types(obj):
    """
    Recursively convert NumPy/Pandas types to native Python types for JSON serialization.
    
    Args:
        obj: Object to convert (can be nested dict/list)
        
    Returns:
        Object with all NumPy/Pandas types converted to native Python equivalents
    """
    if isinstance(obj, dict):
        return {key: convert_to_native_types(val) for key, val in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_types(item) for item in obj]
    elif isinstance(obj, (np.integer, pd.Int64Dtype)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def save_metrics_to_json(data, filepath='extracted_metrics.json'):
    """
    Export metrics dictionary to JSON file with proper type handling.
    
    Args:
        data: Dictionary containing all extracted metrics
        filepath: Output file path
    """
    data_clean = convert_to_native_types(data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_clean, f, indent=2, ensure_ascii=False)
    
    return filepath


def print_summary_report(summary, working_age, gender, top_causes):
    """
    Generate console output summarizing key findings.
    
    Args:
        summary: Overall economic metrics
        working_age: Working-age specific metrics
        gender: Gender distribution metrics
        top_causes: Leading causes of suicide
    """
    print("\n" + "="*80)
    print("ECONOMIC IMPACT ANALYSIS - KEY FINDINGS")
    print("="*80)
    
    print("\nAGGREGATE ECONOMIC BURDEN:")
    print(f"  Annual productivity loss: JPY {summary['total_annual_loss_billion']:.1f} billion")
    print(f"  Total suicides in dataset: {summary['total_suicides']:,}")
    print(f"  Average lifetime earnings lost: JPY {summary['avg_lifetime_earnings_million']:.1f} million")
    
    print("\nINTERVENTION IMPACT (15% reduction scenario):")
    print(f"  Loss prevented: JPY {summary['total_loss_prevented_billion']:.1f} billion")
    print(f"  Total intervention cost: JPY {summary['total_intervention_cost_billion']:.1f} billion")
    print(f"  Net economic benefit: JPY {summary['total_net_benefit_billion']:.1f} billion")
    print(f"  Return on investment: {summary['overall_roi']:.2f}x")
    
    print("\nWORKING-AGE POPULATION (20-59 years):")
    print(f"  Economic loss: JPY {working_age['total_loss_billion']:.1f}B "
          f"({working_age['percent_of_total_loss']:.0f}% of total)")
    print(f"  Average ROI: {working_age['avg_roi']:.2f}x")
    
    print("\nGENDER DISTRIBUTION:")
    print(f"  Male: {gender['male_percentage']:.1f}%")
    print(f"  Female: {gender['female_percentage']:.1f}%")
    
    print("\nLEADING CAUSES:")
    for i, cause in enumerate(top_causes[:3], 1):
        print(f"  {i}. {cause['cause']}: {cause['percentage']:.1f}%")
    
    print("\n" + "="*80)
    print("Metrics export complete. Data ready for downstream analysis pipelines.")
    print("="*80 + "\n")


def main():
    """
    Main execution pipeline for metric extraction.
    """
    print("Initializing metric extraction pipeline...")
    
    df_age, df_gender, df_cause = load_and_prepare_data()
    print("Data loading complete.")
    
    df_policy = calculate_economic_impact(df_age)
    print("Economic impact calculations complete.")
    
    summary_metrics = extract_summary_metrics(df_policy)
    age_breakdown = extract_age_breakdown(df_policy)
    working_age_metrics = extract_working_age_metrics(df_policy)
    gender_summary = extract_gender_summary(df_gender)
    top_causes = extract_top_causes(df_cause)
    yearly_trends, years_available = extract_temporal_trends(df_age)
    
    extracted_data = {
        'summary_metrics': summary_metrics,
        'age_breakdown': age_breakdown,
        'working_age_metrics': working_age_metrics,
        'gender_summary': gender_summary,
        'top_causes': top_causes,
        'yearly_trends': yearly_trends,
        'years_available': years_available,
        'data_sources': {
            'age_data_shape': df_age.shape,
            'gender_data_shape': df_gender.shape,
            'cause_data_shape': df_cause.shape
        }
    }
    
    output_path = save_metrics_to_json(extracted_data)
    print(f"Metrics successfully exported: {output_path}")
    
    print_summary_report(
        summary_metrics, 
        working_age_metrics, 
        gender_summary, 
        top_causes
    )


if __name__ == "__main__":
    main()