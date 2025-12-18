import json


def load_results(json_path='nonprofit_impact_report.json'):
    """Load impact assessment results from JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)


def create_program_cost_table(data):
    """
    Table 1: Program Cost Calculation Breakdown
    Shows how the annual budget was calculated.
    """
    # Note: This uses the default estimates from NonprofitCostCalculator
    # Adjust these to match your actual staff costs
    
    staff_costs = {
        'Workshop Facilitator 1 (Part-time)': 2_000_000,
        'Workshop Facilitator 2 (Part-time)': 2_000_000,
        'Workshop Facilitator 3 (Part-time)': 2_000_000,
        'Lead Outreach Coordinator (Full-time)': 3_000_000,
        'Program Coordinator (Full-time)': 1_500_000,
        'Admin Support (10% allocation)': 500_000,
    }
    
    operating_costs = {
        'Workshop Materials': 300_000,
        'Transportation': 400_000,
        'Hotline Infrastructure (Phone/Software)': 200_000,
        'Staff Training': 150_000,
        'Outreach Materials': 200_000,
        'Miscellaneous Supplies': 150_000,
    }
    
    total_staff = sum(staff_costs.values())
    benefits = total_staff * 0.15
    total_operating = sum(operating_costs.values())
    total_program = total_staff + benefits + total_operating
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 1: Annual Program Cost Calculation</strong></caption>
    <thead>
        <tr>
            <th>Cost Category</th>
            <th>Item</th>
            <th>Amount (JPY)</th>
        </tr>
    </thead>
    <tbody>
"""
    
    # Staff costs
    html += """
        <tr>
            <td rowspan="{}" valign="top"><strong>Staff Costs</strong></td>
            <td>{}</td>
            <td align="right">{:,}</td>
        </tr>
""".format(len(staff_costs), list(staff_costs.keys())[0], list(staff_costs.values())[0])
    
    for item, cost in list(staff_costs.items())[1:]:
        html += """
        <tr>
            <td>{}</td>
            <td align="right">{:,}</td>
        </tr>
""".format(item, cost)
    
    html += """
        <tr>
            <td colspan="2" align="right"><strong>Subtotal Staff</strong></td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
""".format(total_staff)
    
    # Benefits
    html += """
        <tr>
            <td colspan="2"><strong>Benefits (15% of staff costs)</strong></td>
            <td align="right">{:,}</td>
        </tr>
""".format(int(benefits))
    
    # Operating costs
    html += """
        <tr>
            <td rowspan="{}" valign="top"><strong>Operating Costs</strong></td>
            <td>{}</td>
            <td align="right">{:,}</td>
        </tr>
""".format(len(operating_costs), list(operating_costs.keys())[0], list(operating_costs.values())[0])
    
    for item, cost in list(operating_costs.items())[1:]:
        html += """
        <tr>
            <td>{}</td>
            <td align="right">{:,}</td>
        </tr>
""".format(item, cost)
    
    html += """
        <tr>
            <td colspan="2" align="right"><strong>Subtotal Operating</strong></td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
""".format(total_operating)
    
    # Total
    html += """
        <tr>
            <td colspan="2" align="right"><strong>TOTAL ANNUAL PROGRAM COST</strong></td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
""".format(int(total_program))
    
    html += """
    </tbody>
</table>
"""
    
    return html


def create_reach_calculation_table(data):
    """
    Table 2: Program Reach Calculation
    Shows how total reach was calculated.
    """
    reach = data['reach_metrics']
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 2: Program Reach Calculation</strong></caption>
    <thead>
        <tr>
            <th>Step</th>
            <th>Calculation</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="3"><strong>A. School-Based Workshops</strong></td>
        </tr>
        <tr>
            <td>1</td>
            <td>Schools reached</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Average students per school</td>
            <td align="right">500</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Students in workshops (1 × 2)</td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><strong>B. Crisis Hotline</strong></td>
        </tr>
        <tr>
            <td>4</td>
            <td>Total hotline contacts (raw)</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Unique contact rate (assumption)</td>
            <td align="right">80%</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Unique hotline contacts (4 × 5)</td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><strong>C. Total Program Reach</strong></td>
        </tr>
        <tr>
            <td>7</td>
            <td>Total individuals reached (3 + 6)</td>
            <td align="right"><strong>{:,}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><strong>D. National Coverage</strong></td>
        </tr>
        <tr>
            <td>8</td>
            <td>Total schools in Japan</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>9</td>
            <td>School coverage rate (1 ÷ 8)</td>
            <td align="right">{:.2f}%</td>
        </tr>
        <tr>
            <td>10</td>
            <td>National student population (8 × 2)</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Population coverage rate (7 ÷ 10)</td>
            <td align="right">{:.2f}%</td>
        </tr>
    </tbody>
</table>
""".format(
        reach['schools_reached'],
        reach['students_in_workshops'],
        reach['hotline_contacts_raw'],
        reach['unique_hotline_contacts'],
        reach['total_individuals_reached'],
        reach['total_schools_japan'],
        reach['school_coverage_pct'],
        reach['national_student_population'],
        reach['population_coverage_pct']
    )
    
    return html


def create_baseline_risk_table(data):
    """
    Table 3: Baseline Risk Calculation
    Shows expected deaths without intervention.
    """
    youth_data = data['youth_suicide_data']
    reach = data['reach_metrics']
    baseline = data['baseline_risk']
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 3: Baseline Risk Calculation</strong></caption>
    <thead>
        <tr>
            <th>Step</th>
            <th>Parameter</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="3"><strong>A. National Youth Suicide Data (Age 10-19)</strong></td>
        </tr>
        <tr>
            <td>1</td>
            <td>Data period</td>
            <td>{}</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Total youth suicides</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Annual average deaths</td>
            <td align="right">{:.1f}</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Most recent year ({})</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Youth population in Japan (age 10-19)</td>
            <td align="right">11,000,000</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Suicide rate per 100,000 (3 ÷ 5 × 100,000)</td>
            <td align="right"><strong>{:.2f}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><strong>B. Expected Deaths in Reached Population</strong></td>
        </tr>
        <tr>
            <td>7</td>
            <td>Individuals reached by program</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Expected deaths (7 ÷ 100,000 × 6)</td>
            <td align="right"><strong>{:.3f}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><em>Interpretation: Without intervention, we expect {:.3f} deaths annually in our reached population of {:,} individuals.</em></td>
        </tr>
    </tbody>
</table>
""".format(
        youth_data['year_range'],
        youth_data['total_suicides'],
        youth_data['annual_average'],
        youth_data['most_recent_year'],
        youth_data['most_recent_year_count'],
        baseline['suicide_rate_per_100k'],
        reach['total_individuals_reached'],
        baseline['expected_deaths_no_intervention'],
        baseline['expected_deaths_no_intervention'],
        reach['total_individuals_reached']
    )
    
    return html


def create_scenario_comparison_table(data):
    """
    Table 4: Impact Scenarios Comparison
    Shows results under different effectiveness assumptions.
    """
    scenarios = data['impact_scenarios']
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 4: Cost-Effectiveness Scenarios</strong></caption>
    <thead>
        <tr>
            <th>Metric</th>
            <th>Conservative<br>(15% effectiveness)</th>
            <th>Moderate<br>(25% effectiveness)</th>
            <th>Optimistic<br>(35% effectiveness)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="4"><strong>Impact Metrics</strong></td>
        </tr>
        <tr>
            <td>Lives Saved Annually</td>
            <td align="right">{:.3f}</td>
            <td align="right">{:.3f}</td>
            <td align="right">{:.3f}</td>
        </tr>
        <tr>
            <td>DALYs Averted (Years)</td>
            <td align="right">{:.1f}</td>
            <td align="right">{:.1f}</td>
            <td align="right">{:.1f}</td>
        </tr>
        <tr>
            <td>Years of Life per Person Saved</td>
            <td align="right">{}</td>
            <td align="right">{}</td>
            <td align="right">{}</td>
        </tr>
        <tr>
            <td colspan="4"><strong>Cost-Effectiveness</strong></td>
        </tr>
        <tr>
            <td>Cost per Life Saved (JPY)</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
        </tr>
        <tr>
            <td>Cost per Life Saved (Million JPY)</td>
            <td align="right">¥{:.1f}M</td>
            <td align="right">¥{:.1f}M</td>
            <td align="right">¥{:.1f}M</td>
        </tr>
        <tr>
            <td>Cost per DALY (JPY)</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
        </tr>
        <tr>
            <td>Cost per DALY (USD)</td>
            <td align="right">${:,.0f}</td>
            <td align="right">${:,.0f}</td>
            <td align="right">${:,.0f}</td>
        </tr>
        <tr>
            <td>Cost per Person Reached (JPY)</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
        </tr>
        <tr>
            <td colspan="4"><strong>Economic Value Created</strong></td>
        </tr>
        <tr>
            <td>Lifetime Gross Earnings per Person</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
        </tr>
        <tr>
            <td>Tax Revenue per Person (25% rate)</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
            <td align="right">¥{:,.0f}</td>
        </tr>
        <tr>
            <td>Total Economic Value Saved</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
        </tr>
        <tr>
            <td>Total Tax Revenue Saved</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
        </tr>
        <tr>
            <td>Net Benefit (Economic Value - Program Cost)</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
            <td align="right">¥{:.0f}M</td>
        </tr>
        <tr>
            <td colspan="4"><strong>Return on Investment</strong></td>
        </tr>
        <tr>
            <td>ROI (Gross Earnings Basis)</td>
            <td align="right">{:.1f}x</td>
            <td align="right">{:.1f}x</td>
            <td align="right">{:.1f}x</td>
        </tr>
        <tr>
            <td>ROI (Tax Revenue Basis)</td>
            <td align="right">{:.1f}x</td>
            <td align="right">{:.1f}x</td>
            <td align="right">{:.1f}x</td>
        </tr>
        <tr>
            <td colspan="4"><strong>WHO Cost-Effectiveness Classification</strong></td>
        </tr>
        <tr>
            <td>Classification</td>
            <td>Highly Cost-Effective</td>
            <td>Highly Cost-Effective</td>
            <td>Highly Cost-Effective</td>
        </tr>
        <tr>
            <td>Times Below WHO Threshold ($34,000)</td>
            <td align="right">{:.0f}x</td>
            <td align="right">{:.0f}x</td>
            <td align="right">{:.0f}x</td>
        </tr>
    </tbody>
</table>
""".format(
        # Impact metrics
        scenarios['conservative']['lives_saved_annually'],
        scenarios['moderate']['lives_saved_annually'],
        scenarios['optimistic']['lives_saved_annually'],
        scenarios['conservative']['dalys_averted'],
        scenarios['moderate']['dalys_averted'],
        scenarios['optimistic']['dalys_averted'],
        scenarios['conservative']['years_of_life_per_person'],
        scenarios['moderate']['years_of_life_per_person'],
        scenarios['optimistic']['years_of_life_per_person'],
        # Cost-effectiveness
        scenarios['conservative']['cost_per_life_saved_jpy'],
        scenarios['moderate']['cost_per_life_saved_jpy'],
        scenarios['optimistic']['cost_per_life_saved_jpy'],
        scenarios['conservative']['cost_per_life_saved_million'],
        scenarios['moderate']['cost_per_life_saved_million'],
        scenarios['optimistic']['cost_per_life_saved_million'],
        scenarios['conservative']['cost_per_daly_jpy'],
        scenarios['moderate']['cost_per_daly_jpy'],
        scenarios['optimistic']['cost_per_daly_jpy'],
        scenarios['conservative']['cost_per_daly_usd'],
        scenarios['moderate']['cost_per_daly_usd'],
        scenarios['optimistic']['cost_per_daly_usd'],
        scenarios['conservative']['cost_per_person_reached_jpy'],
        scenarios['moderate']['cost_per_person_reached_jpy'],
        scenarios['optimistic']['cost_per_person_reached_jpy'],
        # Economic value
        scenarios['conservative']['lifetime_value_per_person']['gross_earnings_jpy'],
        scenarios['moderate']['lifetime_value_per_person']['gross_earnings_jpy'],
        scenarios['optimistic']['lifetime_value_per_person']['gross_earnings_jpy'],
        scenarios['conservative']['lifetime_value_per_person']['tax_revenue_jpy'],
        scenarios['moderate']['lifetime_value_per_person']['tax_revenue_jpy'],
        scenarios['optimistic']['lifetime_value_per_person']['tax_revenue_jpy'],
        scenarios['conservative']['aggregate_economic_impact']['total_economic_value_million'],
        scenarios['moderate']['aggregate_economic_impact']['total_economic_value_million'],
        scenarios['optimistic']['aggregate_economic_impact']['total_economic_value_million'],
        scenarios['conservative']['aggregate_economic_impact']['total_tax_revenue_million'],
        scenarios['moderate']['aggregate_economic_impact']['total_tax_revenue_million'],
        scenarios['optimistic']['aggregate_economic_impact']['total_tax_revenue_million'],
        scenarios['conservative']['aggregate_economic_impact']['net_benefit_million'],
        scenarios['moderate']['aggregate_economic_impact']['net_benefit_million'],
        scenarios['optimistic']['aggregate_economic_impact']['net_benefit_million'],
        # ROI
        scenarios['conservative']['return_on_investment']['roi_gross_earnings'],
        scenarios['moderate']['return_on_investment']['roi_gross_earnings'],
        scenarios['optimistic']['return_on_investment']['roi_gross_earnings'],
        scenarios['conservative']['return_on_investment']['roi_tax_revenue'],
        scenarios['moderate']['return_on_investment']['roi_tax_revenue'],
        scenarios['optimistic']['return_on_investment']['roi_tax_revenue'],
        # WHO
        data['who_assessment']['conservative']['times_below_threshold'],
        data['who_assessment']['moderate']['times_below_threshold'],
        data['who_assessment']['optimistic']['times_below_threshold']
    )
    
    return html


def create_lives_saved_calculation_table(data):
    """
    Table 5: Lives Saved Calculation Detail
    Step-by-step calculation for moderate scenario.
    """
    baseline = data['baseline_risk']
    moderate = data['impact_scenarios']['moderate']
    reach = data['reach_metrics']
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 5: Lives Saved Calculation (Moderate Scenario)</strong></caption>
    <thead>
        <tr>
            <th>Step</th>
            <th>Calculation</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Individuals reached by program</td>
            <td align="right">{:,}</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Youth suicide rate (per 100,000)</td>
            <td align="right">{:.2f}</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Expected deaths without intervention (1 ÷ 100,000 × 2)</td>
            <td align="right">{:.3f}</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Intervention effectiveness rate</td>
            <td align="right">25%</td>
        </tr>
        <tr>
            <td>5</td>
            <td><strong>Lives saved (3 × 4)</strong></td>
            <td align="right"><strong>{:.3f}</strong></td>
        </tr>
        <tr>
            <td>6</td>
            <td>Average age at prevention</td>
            <td align="right">17 years</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Life expectancy in Japan</td>
            <td align="right">84 years</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Years of life saved per person (7 - 6)</td>
            <td align="right">{} years</td>
        </tr>
        <tr>
            <td>9</td>
            <td><strong>Total DALYs averted (5 × 8)</strong></td>
            <td align="right"><strong>{:.1f} years</strong></td>
        </tr>
        <tr>
            <td>10</td>
            <td>Program annual cost</td>
            <td align="right">¥10,000,000</td>
        </tr>
        <tr>
            <td>11</td>
            <td><strong>Cost per life saved (10 ÷ 5)</strong></td>
            <td align="right"><strong>¥{:,.0f}</strong></td>
        </tr>
        <tr>
            <td>12</td>
            <td><strong>Cost per DALY averted (10 ÷ 9)</strong></td>
            <td align="right"><strong>¥{:,.0f} (~${:,.0f})</strong></td>
        </tr>
    </tbody>
</table>
""".format(
        reach['total_individuals_reached'],
        baseline['suicide_rate_per_100k'],
        baseline['expected_deaths_no_intervention'],
        moderate['lives_saved_annually'],
        moderate['years_of_life_per_person'],
        moderate['dalys_averted'],
        moderate['cost_per_life_saved_jpy'],
        moderate['cost_per_daly_jpy'],
        moderate['cost_per_daly_usd']
    )
    
    return html


def create_economic_value_calculation_table(data):
    """
    Table 6: Economic Value Calculation Detail
    Shows how lifetime earnings were calculated.
    """
    moderate = data['impact_scenarios']['moderate']
    
    html = """
<table border="1" cellpadding="8" cellspacing="0">
    <caption><strong>Table 6: Economic Value Calculation (Per Life Saved)</strong></caption>
    <thead>
        <tr>
            <th>Step</th>
            <th>Parameter</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Average age at prevention</td>
            <td align="right">17 years</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Retirement age in Japan</td>
            <td align="right">65 years</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Working years remaining (2 - 1)</td>
            <td align="right">{} years</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Average annual salary (career average)</td>
            <td align="right">¥4,500,000</td>
        </tr>
        <tr>
            <td>5</td>
            <td><strong>Lifetime gross earnings (3 × 4)</strong></td>
            <td align="right"><strong>¥{:,}</strong></td>
        </tr>
        <tr>
            <td>6</td>
            <td>Effective tax rate (income + residence + social insurance)</td>
            <td align="right">25%</td>
        </tr>
        <tr>
            <td>7</td>
            <td><strong>Lifetime tax revenue (5 × 6)</strong></td>
            <td align="right"><strong>¥{:,}</strong></td>
        </tr>
        <tr>
            <td colspan="3"><strong>Aggregate Impact (Moderate Scenario)</strong></td>
        </tr>
        <tr>
            <td>8</td>
            <td>Lives saved annually</td>
            <td align="right">{:.3f}</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Total economic value saved (5 × 8)</td>
            <td align="right">¥{:.0f}M</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Total tax revenue saved (7 × 8)</td>
            <td align="right">¥{:.0f}M</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Program cost</td>
            <td align="right">¥10.0M</td>
        </tr>
        <tr>
            <td>12</td>
            <td><strong>Net economic benefit (9 - 11)</strong></td>
            <td align="right"><strong>¥{:.0f}M</strong></td>
        </tr>
        <tr>
            <td>13</td>
            <td><strong>ROI - Gross earnings basis (9 ÷ 11)</strong></td>
            <td align="right"><strong>{:.1f}x</strong></td>
        </tr>
        <tr>
            <td>14</td>
            <td><strong>ROI - Tax revenue basis (10 ÷ 11)</strong></td>
            <td align="right"><strong>{:.1f}x</strong></td>
        </tr>
    </tbody>
</table>
""".format(
        moderate['work_years_per_person'],
        moderate['lifetime_value_per_person']['gross_earnings_jpy'],
        moderate['lifetime_value_per_person']['tax_revenue_jpy'],
        moderate['lives_saved_annually'],
        moderate['aggregate_economic_impact']['total_economic_value_million'],
        moderate['aggregate_economic_impact']['total_tax_revenue_million'],
        moderate['aggregate_economic_impact']['net_benefit_million'],
        moderate['return_on_investment']['roi_gross_earnings'],
        moderate['return_on_investment']['roi_tax_revenue']
    )
    
    return html


def save_table_html(table_html, filename):
    """Save individual table as standalone HTML file."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
</head>
<body>
{}
</body>
</html>
""".format(filename.replace('.html', '').replace('_', ' ').title(), table_html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename


if __name__ == "__main__":
    # Load data
    data = load_results('nonprofit_impact_report.json')
    
    # Generate all tables
    tables = {
        'table1_program_cost.html': create_program_cost_table(data),
        'table2_reach_calculation.html': create_reach_calculation_table(data),
        'table3_baseline_risk.html': create_baseline_risk_table(data),
        'table4_scenario_comparison.html': create_scenario_comparison_table(data),
        'table5_lives_saved_calculation.html': create_lives_saved_calculation_table(data),
        'table6_economic_value_calculation.html': create_economic_value_calculation_table(data),
    }
    
    # Save each table as separate HTML
    for filename, table_html in tables.items():
        save_table_html(table_html, filename)
        print(f"✓ {filename}")
    
    print("All tables generated successfully!")