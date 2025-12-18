import pandas as pd
import plotly.express as px
import os
import assumptions

# ============================================================================
# VISUAL THEME — MODERN, SUBTLE, POLICY-SAFE
# ============================================================================

COLOR_SEQ_MAIN = [
    "#0B5D3B", "#1E7F5C", "#4C9A7A", "#8FBF9F",
    "#BFD9C7", "#6C7D8A", "#9AA5AE", "#C1C7CD", "#7A6C5D"
]

COLOR_SEQ_SOFT = [
    "#E8F3EE", "#D6EBE1", "#C4E2D4", "#B2DAC7", "#A0D1BA"
]

COLOR_SCALE_GREEN = [
    "#F1F7F4", "#CFE6DA", "#9FCDB8", "#5FA98C", "#0B5D3B"
]

def apply_global_layout(fig):
    fig.update_layout(
        font=dict(family="Inter, Arial", size=14),
        title_font=dict(size=18),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    return fig


# ============================================================================
# LOAD DATA
# ============================================================================

df_age = pd.read_csv("../../data_clean/age_cleaned.csv")
df_gender = pd.read_csv("../../data_clean/gender_cleaned.csv")
df_cause = pd.read_csv("../../data_clean/reason_cleaned.csv")

df_gender = df_gender.rename(columns={
    '自殺者_総数': 'total',
    '自殺者_男性': 'male',
    '自殺者_女性': 'female'
})
for col in ['total', 'male', 'female']:
    df_gender[col] = pd.to_numeric(df_gender[col], errors='coerce')
df_gender.dropna(inplace=True)

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

df_age = df_age.rename(columns={'年齢層': 'age_group', '人数': 'suicides'})
age_map = {
    '0～9歳': '0-9', '10～19歳': '10-19', '20～29歳': '20-29',
    '30～39歳': '30-39', '40～49歳': '40-49', '50～59歳': '50-59',
    '60～69歳': '60-69', '70～79歳': '70-79', '80歳以上': '80+'
}
df_age['age_group'] = df_age['age_group'].map(age_map)
df_age['suicides'] = pd.to_numeric(df_age['suicides'], errors='coerce')
df_age.dropna(inplace=True)


# ============================================================================
# ECONOMIC MODEL
# ============================================================================

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

# Pull baseline and reduced loss from assumptions.py
df_policy['baseline_loss'] = df_policy['annual_loss_yen'].apply(assumptions.baseline_loss)
df_policy['reduced_loss'] = df_policy['annual_loss_yen'].apply(assumptions.reduced_loss)


# ============================================================================
# CHARTS
# ============================================================================

def create_suicide_trends_unified():
    fig = px.line(
        df_age, x='year', y='suicides', color='age_group',
        title='Suicide Trends by Age Group (Japan)',
        color_discrete_sequence=COLOR_SEQ_MAIN,
        template='plotly_white'
    )
    fig.update_traces(mode='lines+markers', marker=dict(size=4))
    fig.update_layout(hovermode='x unified', height=600)
    return apply_global_layout(fig)


def create_economic_loss_by_age():
    # Convert annual loss to billions for readability
    df_econ_plot = df_econ.copy()
    df_econ_plot['loss_billion'] = df_econ_plot['annual_loss_yen'] / 1e9

    # Horizontal bar chart
    fig = px.bar(
        df_econ_plot.sort_values('loss_billion', ascending=True),
        x='loss_billion',
        y='age_group',
        orientation='h',
        text='loss_billion',
        labels={'loss_billion': 'Annual Loss (Billion ¥)', 'age_group': 'Age Group'},
        title='Annual Economic Loss by Age Group',
        template='plotly_white',
        color='loss_billion',
        color_continuous_scale=COLOR_SCALE_GREEN
    )

    # Format text and hover labels
    fig.update_traces(
        texttemplate='¥%{x:.1f}B',
        textposition='outside',
        hovertemplate='Age %{y}<br>Loss: ¥%{x:.1f}B'
    )

    # Layout adjustments
    fig.update_layout(
        height=500,
        margin=dict(l=80, r=40, t=60, b=40),
        yaxis_title='Age Group',
        xaxis_title='Annual Economic Loss (Billion ¥)',
        coloraxis_showscale=False  # remove unnecessary color legend
    )

    return apply_global_layout(fig)



def create_roi_by_age():
    fig = px.bar(
        df_policy, x='age_group', y='roi',
        title='Return on Investment by Age Group',
        template='plotly_white'
    )
    fig.update_traces(marker_color="#1E7F5C")
    fig.add_hline(
        y=1, line_dash='dash', line_color="#6C7D8A",
        annotation_text='Break-even', annotation_font_color="#6C7D8A"
    )
    fig.update_layout(height=500)
    return apply_global_layout(fig)


def create_cause_heatmap():
    # Pivot table: rows = year, columns = cause, values = count proportion
    pivot = df_cause.pivot_table(
        index='year', columns='cause', values='count', aggfunc='sum', fill_value=0
    )
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100  # convert to %
    
    # Create heatmap
    fig = px.imshow(
        pivot_pct,
        aspect='auto',
        color_continuous_scale='Greens',
        text_auto='.1f',  # show percentage inside cells
        labels={'x': 'Cause', 'y': 'Year', 'color': '% of Suicides'},
        title='Proportion of Suicides by Cause Over Time'
    )

    # Layout improvements
    fig.update_layout(
        height=600,
        xaxis_tickangle=-45,
        xaxis_title='Cause of Suicide',
        yaxis_title='Year',
        margin=dict(l=80, r=40, t=60, b=120)
    )

    # Adjust font
    fig.update_xaxes(tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return apply_global_layout(fig)


def create_policy_scenario_comparison(df_policy):
    df_long = df_policy.melt(
        id_vars='age_group',
        value_vars=['baseline_loss', 'reduced_loss'],
        var_name='scenario',
        value_name='loss'
    )

    scenario_labels = {
        'baseline_loss': 'Baseline',
        'reduced_loss': '15% Reduction'
    }
    df_long['scenario'] = df_long['scenario'].map(scenario_labels)

    fig = px.bar(
        df_long,
        x='age_group',
        y='loss',
        color='scenario',
        barmode='group',
        title='Economic Impact: Baseline vs 15% Reduction',
        labels={'loss': 'Annual Economic Loss (¥)', 'age_group': 'Age Group'},
        template='plotly_white',
        color_discrete_sequence=[
            "#9AA5AE",  # muted gray-blue (baseline)
            "#1E7F5C"   # policy green (reduction)
        ]
    )

    fig.update_traces(
        hovertemplate='Age %{x}<br>Loss: ¥%{y:,.0f}<extra></extra>'
    )

    fig.update_layout(
        height=520,
        font=dict(family="Inter, Arial", size=14),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        bargap=0.25
    )

    return fig


# ============================================================================
# SAVE OUTPUTS
# ============================================================================

if __name__ == "__main__":
    os.makedirs("charts", exist_ok=True)

    create_suicide_trends_unified().write_html("charts/suicide_trends_unified.html")
    create_economic_loss_by_age().write_html("charts/economic_loss_by_age.html")
    create_roi_by_age().write_html("charts/roi_by_age.html")
    create_cause_heatmap().write_html("charts/cause_heatmap.html")
    create_policy_scenario_comparison(df_policy).write_html("charts/policy_scenario_comparison.html")

    print("✅ All charts generated with modern visual styling.")


import numpy as np
import plotly.graph_objects as go

# =========================
# DATA (FROM YOUR MODEL)
# =========================

YOUTH_POPULATION = 6_950_000
SUICIDE_RATE_PER_100K = 20.8914772727

reach_pct = np.linspace(0.008, 0.02, 60)     # 0.8% → 2.0%
effectiveness = np.linspace(0.15, 0.35, 60)

R, E = np.meshgrid(reach_pct, effectiveness)

individuals_reached = R * YOUTH_POPULATION
expected_deaths = individuals_reached * SUICIDE_RATE_PER_100K / 100_000
lives_saved = expected_deaths * E

# =========================
# CONTOUR PLOT
# =========================

fig = go.Figure()

fig.add_trace(go.Contour(
    x=reach_pct * 100,
    y=effectiveness * 100,
    z=lives_saved,
    colorscale=COLOR_SCALE_GREEN,
    contours=dict(
        showlabels=True,
        labelfont=dict(size=12)
    ),
    hovertemplate=(
        "Reach: %{x:.2f}%<br>"
        "Effectiveness: %{y:.1f}%<br>"
        "Lives saved: %{z:.2f}<extra></extra>"
    )
))

# =========================
# SCENARIO POINTS
# =========================

scenarios = {
    "Conservative": (1.15, 15, 2.50),
    "Moderate": (1.15, 25, 4.16),
    "Optimistic": (1.15, 35, 5.83)
}

for name, (r, e, z) in scenarios.items():
    fig.add_trace(go.Scatter(
        x=[r],
        y=[e],
        mode="markers+text",
        marker=dict(size=10, color="#0B5D3B"),
        text=[name],
        textposition="top center",
        hovertemplate=(
            f"{name}<br>"
            f"Reach: {r:.2f}%<br>"
            f"Effectiveness: {e:.0f}%<br>"
            f"Lives saved: {z:.2f}<extra></extra>"
        ),
        showlegend=False
    ))

# =========================
# LAYOUT
# =========================

fig.update_layout(
    title="Iso-Impact Map: Annual Lives Saved",
    xaxis_title="Program Reach (% of youth population)",
    yaxis_title="Intervention Effectiveness (%)",
    margin=dict(l=60, r=40, t=60, b=60)
)

apply_global_layout(fig)

fig.write_html(
    "impact_contour_lives_saved.html",
    include_plotlyjs="cdn"
)
