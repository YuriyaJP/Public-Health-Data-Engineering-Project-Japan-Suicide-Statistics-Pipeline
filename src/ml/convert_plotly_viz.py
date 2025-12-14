"""
convert_to_plotly.py
Converts Japan suicide statistics analysis to interactive Plotly HTML charts
Author: Yulia Chekhovska
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

print("Loading data...")

# Load your age data
df_age = pd.read_csv("../../data_clean/age_cleaned.csv")

# Rename columns to English
df_age = df_age.rename(columns={
    '年齢層': 'age_group',
    '人数': 'suicides',
    'year': 'year'
})

# Map Japanese age groups to English
age_map = {
    '0～9歳': '0-9',
    '10～19歳': '10-19',
    '20～29歳': '20-29',
    '30～39歳': '30-39',
    '40～49歳': '40-49',
    '50～59歳': '50-59',
    '60～69歳': '60-69',
    '70～79歳': '70-79',
    '80歳以上': '80+',
    '不詳': 'Unknown',
    '合計': 'Total'
}

df_age['age_group'] = df_age['age_group'].map(age_map)

# Drop unknown and total
df_age = df_age[~df_age['age_group'].isin(['Unknown', 'Total'])]

# Convert suicides to numeric
df_age['suicides'] = pd.to_numeric(df_age['suicides'], errors='coerce')

# Drop any rows with missing values
df_age = df_age.dropna()

print(f"✓ Loaded {len(df_age)} records across {df_age['year'].nunique()} years")

# ============================================================================
# CHART 1: INTERACTIVE LINE CHART - ALL AGE GROUPS ON ONE CHART
# ============================================================================

def create_suicide_trends_unified():
    """
    Single interactive line chart showing all age groups.
    Better than facet grid for comparing trends across groups.
    """
    
    fig = px.line(
        df_age,
        x='year',
        y='suicides',
        color='age_group',
        title='Suicide Trends by Age Group in Japan (1978-2024)',
        labels={
            'suicides': 'Number of Suicides',
            'year': 'Year',
            'age_group': 'Age Group'
        },
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    # Add markers and improve hover
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=4),
        hovertemplate='<b>Age %{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      'Suicides: %{y:,.0f}<br>' +
                      '<extra></extra>'
    )
    
    # Improve layout
    fig.update_layout(
        hovermode='x unified',  # Show all age groups when hovering over a year
        height=600,
        font=dict(size=14),
        legend=dict(
            title=dict(text='Age Group', font=dict(size=14)),
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=5, label="5y", step="year", stepmode="backward"),
                    dict(count=10, label="10y", step="year", stepmode="backward"),
                    dict(count=20, label="20y", step="year", stepmode="backward"),
                    dict(step="all", label="All")
                ]),
                bgcolor="rgba(255,255,255,0.9)",
                activecolor="rgba(100,100,255,0.3)"
            )
        )
    )
    
    return fig

# ============================================================================
# CHART 2: SMALL MULTIPLES - INDIVIDUAL AGE GROUP TRENDS
# ============================================================================

def create_suicide_trends_faceted():
    """
    Facet grid showing individual trend for each age group.
    This is your original Seaborn FacetGrid converted to Plotly.
    """
    
    fig = px.line(
        df_age,
        x='year',
        y='suicides',
        facet_col='age_group',
        facet_col_wrap=3,  # 3 columns
        title='Number of Suicides by Age Group Over Time',
        labels={
            'suicides': 'Number of Suicides',
            'year': 'Year'
        },
        template='plotly_white',
        markers=True
    )
    
    # Customize each subplot
    fig.update_traces(
        line=dict(color='#2E86AB', width=2),
        marker=dict(size=4, color='#A23B72'),
        hovertemplate='Year: %{x}<br>Suicides: %{y:,.0f}<extra></extra>'
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        showlegend=False,
        font=dict(size=12)
    )
    
    # Clean up facet titles (remove "age_group=" prefix)
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("age_group=", "")))
    
    # Make y-axes independent (like your Seaborn sharey=False)
    fig.update_yaxes(matches=None)
    
    return fig

# ============================================================================
# CHART 3: TOP AGE GROUPS OVER TIME (STACKED AREA)
# ============================================================================

def create_top_age_groups_area():
    """
    Stacked area chart showing composition of suicides by age group.
    Shows which age groups dominate at different time periods.
    """
    
    # Calculate total suicides per year for percentage calculation
    yearly_totals = df_age.groupby('year')['suicides'].sum().reset_index()
    yearly_totals.columns = ['year', 'total']
    
    # Merge and calculate percentages
    df_pct = df_age.merge(yearly_totals, on='year')
    df_pct['percentage'] = (df_pct['suicides'] / df_pct['total']) * 100
    
    fig = px.area(
        df_pct,
        x='year',
        y='percentage',
        color='age_group',
        title='Suicide Composition by Age Group (%)',
        labels={
            'percentage': 'Percentage of Total Suicides',
            'year': 'Year',
            'age_group': 'Age Group'
        },
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        hovertemplate='<b>Age %{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      'Percentage: %{y:.1f}%<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        height=600,
        hovermode='x unified',
        font=dict(size=14),
        legend=dict(
            title=dict(text='Age Group'),
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=0.99
        )
    )
    
    return fig

# ============================================================================
# CHART 4: HIGHEST SUICIDE RATES - BAR CHART
# ============================================================================

def create_highest_suicides_bar():
    """
    Bar chart showing which age groups have highest total suicides.
    Recreates your existing static image as interactive chart.
    """
    
    # Calculate total suicides per age group across all years
    total_by_age = df_age.groupby('age_group')['suicides'].sum().reset_index()
    total_by_age = total_by_age.sort_values('suicides', ascending=False)
    
    fig = px.bar(
        total_by_age,
        x='age_group',
        y='suicides',
        title='Total Suicides by Age Group (1978-2024)',
        labels={
            'suicides': 'Total Number of Suicides',
            'age_group': 'Age Group'
        },
        template='plotly_white',
        color='suicides',
        color_continuous_scale='Reds'
    )
    
    fig.update_traces(
        hovertemplate='<b>Age %{x}</b><br>' +
                      'Total Suicides: %{y:,.0f}<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        font=dict(size=14),
        xaxis=dict(categoryorder='total descending')
    )
    
    return fig

# ============================================================================
# CHART 5: RECENT TRENDS (LAST 10 YEARS)
# ============================================================================

def create_recent_trends():
    """
    Focus on recent decade to show current state.
    """
    
    # Get last 10 years
    recent_years = df_age['year'].max() - 9
    df_recent = df_age[df_age['year'] >= recent_years]
    
    fig = px.line(
        df_recent,
        x='year',
        y='suicides',
        color='age_group',
        title=f'Recent Suicide Trends ({int(recent_years)}-2024)',
        labels={
            'suicides': 'Number of Suicides',
            'year': 'Year',
            'age_group': 'Age Group'
        },
        template='plotly_white',
        markers=True
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate='<b>Age %{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      'Suicides: %{y:,.0f}<br>' +
                      '<extra></extra>'
    )
    
    fig.update_layout(
        height=600,
        hovermode='x unified',
        font=dict(size=14),
        legend=dict(
            title=dict(text='Age Group'),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# ============================================================================
# SAVE ALL CHARTS
# ============================================================================

if __name__ == "__main__":
    
    # Create charts directory
    os.makedirs('charts', exist_ok=True)
    
    print("\n" + "="*60)
    print("Generating Interactive Plotly Charts")
    print("="*60 + "\n")
    
    # Chart 1: Unified trends (RECOMMENDED for recruiters)
    print("📊 Creating unified trends chart...")
    fig1 = create_suicide_trends_unified()
    fig1.write_html(
        'charts/suicide_trends_unified.html',
        config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
    )
    print("   ✓ Saved: charts/suicide_trends_unified.html")
    
    # Chart 2: Faceted trends (your original Seaborn version)
    print("📊 Creating faceted trends chart...")
    fig2 = create_suicide_trends_faceted()
    fig2.write_html(
        'charts/suicide_trends_faceted.html',
        config={'displayModeBar': True, 'displaylogo': False}
    )
    print("   ✓ Saved: charts/suicide_trends_faceted.html")
    
    # Chart 3: Area chart
    print("📊 Creating composition area chart...")
    fig3 = create_top_age_groups_area()
    fig3.write_html(
        'charts/suicide_composition.html',
        config={'displayModeBar': True, 'displaylogo': False}
    )
    print("   ✓ Saved: charts/suicide_composition.html")
    
    # Chart 4: Bar chart
    print("📊 Creating total suicides bar chart...")
    fig4 = create_highest_suicides_bar()
    fig4.write_html(
        'charts/highest_suicides.html',
        config={'displayModeBar': True, 'displaylogo': False}
    )
    print("   ✓ Saved: charts/highest_suicides.html")
    
    # Chart 5: Recent trends
    print("📊 Creating recent trends chart...")
    fig5 = create_recent_trends()
    fig5.write_html(
        'charts/recent_trends.html',
        config={'displayModeBar': True, 'displaylogo': False}
    )
    print("   ✓ Saved: charts/recent_trends.html")
    
    print("\n" + "="*60)
    print("✅ All charts generated successfully!")
    print("="*60)
    print("\n📁 Files created in 'charts/' directory:")
    print("   1. suicide_trends_unified.html    (RECOMMENDED for portfolio)")
    print("   2. suicide_trends_faceted.html    (Your original FacetGrid)")
    print("   3. suicide_composition.html       (Stacked area chart)")
    print("   4. highest_suicides.html          (Bar chart)")
    print("   5. recent_trends.html             (Last 10 years)")
    print("\n🚀 Next steps:")
    print("   1. Upload 'charts/' folder to your GitHub repo")
    print("   2. Update your HTML page with iframe embeds")
    print("   3. Test on your GitHub pages site")