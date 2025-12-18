"""
Nonprofit Crisis Intervention Program: Cost-Effectiveness Analysis
===================================================================
Direct attribution model calculating impact of school-based prevention 
workshops and crisis hotline services.

Date: 2025
"""

import pandas as pd
import numpy as np
import json


class NonprofitCostCalculator:
    """
    Calculate actual program operating costs.
    """
    
    def __init__(self):
        # Staff costs (annual, JPY)
        self.staff_costs = {
            'workshop_facilitator_1': 2_000_000,     # Part-time
            'workshop_facilitator_2': 2_000_000,     # Part-time
            'workshop_facilitator_3': 2_000_000,     # Part-time
            'lead_outreach_coordinator': 3_000_000,   # Full-time
            'program_director': 5_000_000,        # Full-time
            'admin_support': 500_000,                # Shared resource (10% allocation)
        }
        
        # Operating costs (annual, JPY)
        self.operating_costs = {
            'workshop_materials': 300_000,
            'transportation': 400_000,
            'hotline_infrastructure': 200_000,      # Phone/software subscription
            'staff_training': 150_000,
            'outreach_materials': 200_000,
            'misc_supplies': 150_000,
        }
        
        # Benefits rate (social insurance, pension, etc.)
        self.benefits_rate = 0.15  # 15% of salary costs
    
    
    def calculate_total_cost(self):
        """
        Calculate total annual program cost.
        
        Returns:
            dict: Breakdown of costs
        """
        total_staff = sum(self.staff_costs.values())
        total_benefits = total_staff * self.benefits_rate
        total_operating = sum(self.operating_costs.values())
        total_program_cost = total_staff + total_benefits + total_operating
        
        return {
            'staff_costs_jpy': total_staff,
            'benefits_jpy': total_benefits,
            'operating_costs_jpy': total_operating,
            'total_program_cost_jpy': total_program_cost,
            'total_program_cost_million': total_program_cost / 1_000_000,
            'breakdown': {
                'staff': self.staff_costs,
                'operating': self.operating_costs
            }
        }


class ProgramImpactModel:
    """
    Calculate cost-effectiveness of the nonprofit crisis intervention program.
    """
    
    def __init__(self, program_cost_jpy, youth_data_path=None):
        """
        Args:
            program_cost_jpy: Annual operating budget
            youth_data_path: Path to master_cleaned_dataset.csv with actual youth suicide counts
        """
        self.program_cost = program_cost_jpy
        
        # National context
        self.total_schools_japan = 13_900  # Junior high + high school
        self.avg_students_per_school = 500
        self.national_student_population = self.total_schools_japan * self.avg_students_per_school
        
        # Load dataset
        if youth_data_path:
            self.youth_data = self._load_youth_suicide_data(youth_data_path)
            self.youth_suicide_rate_per_100k = self.youth_data['rate_per_100k']
            self.annual_youth_suicides = self.youth_data['annual_average']
            self.recent_year_suicides = self.youth_data['most_recent_year_count']
            self.data_years = self.youth_data['year_range']
        else:
            self.youth_suicide_rate_per_100k = None
            self.annual_youth_suicides = None
            self.recent_year_suicides = None
            self.data_years = None
            print("\n⚠️  WARNING: No youth data provided. Please provide master_cleaned_dataset.csv")
            print("   Expected columns: 'year', '年齢層' (with '10～19歳'), '人数_x'")
        
        # Life expectancy and economic parameters
        self.life_expectancy_japan = 84
        self.retirement_age = 65
        self.avg_annual_salary = 4_500_000  # Average across working life
        self.effective_tax_rate = 0.25  # Income tax + residence tax + social insurance
    
    
    def _load_youth_suicide_data(self, filepath):
        """
        Load and process actual youth suicide data from your dataset.
        
        Args:
            filepath: Path to master_cleaned_dataset.csv
            
        Returns:
            dict: Processed youth suicide statistics
        """
        try:
            df = pd.read_csv(filepath)
            
            # Filter for youth age group (10-19)
            youth_df = df[df['年齢層'] == '10～19歳'].copy()
            
            if youth_df.empty:
                raise ValueError("No data found for age group '10～19歳'")
            
            # Get suicide counts
            youth_df['suicides'] = pd.to_numeric(youth_df['人数_x'], errors='coerce')
            youth_df = youth_df.dropna(subset=['suicides'])
            
            # Calculate statistics
            total_suicides = youth_df['suicides'].sum()
            years_span = youth_df['year'].max() - youth_df['year'].min() + 1
            annual_average = total_suicides / years_span
            
            # Get most recent year
            most_recent_year = youth_df['year'].max()
            most_recent_count = youth_df[youth_df['year'] == most_recent_year]['suicides'].values[0]
            
            # Calculate rate per 100,000
            # Japan youth population (10-19) approximately 11 million (2023)
            japan_youth_population = 11_000_000
            rate_per_100k = (annual_average / japan_youth_population) * 100_000
            
            return {
                'total_suicides': int(total_suicides),
                'annual_average': float(annual_average),
                'most_recent_year': int(most_recent_year),
                'most_recent_year_count': int(most_recent_count),
                'rate_per_100k': float(rate_per_100k),
                'year_range': f"{youth_df['year'].min()}-{youth_df['year'].max()}",
                'data_source': filepath
            }
            
        except Exception as e:
            print(f"\n❌ ERROR loading youth data: {e}")
            print("   Please check:")
            print("   1. File exists at specified path")
            print("   2. Column names: 'year', '年齢層', '人数_x'")
            print("   3. Age group '10～19歳' exists in data")
            raise
    
    
    def calculate_reach(self, schools_reached, workshops_delivered, hotline_contacts_annual):
        """
        Calculate YOUR program's actual reach.
        
        Args:
            schools_reached: Schools where workshops delivered (145)
            workshops_delivered: Total workshops conducted (97)
            hotline_contacts_annual: Annual crisis line contacts (9,000)
            
        Returns:
            dict: Reach metrics
        """
        students_in_workshops = schools_reached * self.avg_students_per_school
        
        # Assume 80% of hotline contacts are unique individuals
        unique_hotline_contacts = int(hotline_contacts_annual * 0.80)
        
        total_reach = students_in_workshops + unique_hotline_contacts
        
        school_coverage_pct = (schools_reached / self.total_schools_japan) * 100
        population_coverage_pct = (total_reach / self.national_student_population) * 100
        
        return {
            'schools_reached': schools_reached,
            'total_schools_japan': self.total_schools_japan,
            'school_coverage_pct': school_coverage_pct,
            'workshops_delivered': workshops_delivered,
            'students_in_workshops': students_in_workshops,
            'hotline_contacts_raw': hotline_contacts_annual,
            'unique_hotline_contacts': unique_hotline_contacts,
            'total_individuals_reached': total_reach,
            'national_student_population': self.national_student_population,
            'population_coverage_pct': population_coverage_pct
        }
    
    
    def calculate_baseline_risk(self, population_reached):
        """
        Calculate expected deaths in YOUR reached population without intervention.
        Uses ACTUAL youth suicide data from your dataset.
        
        Args:
            population_reached: Number of individuals your program reached
            
        Returns:
            float: Expected annual deaths
        """
        if self.youth_suicide_rate_per_100k is None:
            raise ValueError("Youth suicide data not loaded. Please provide master_cleaned_dataset.csv")
        
        expected_deaths = (population_reached / 100_000) * self.youth_suicide_rate_per_100k
        return expected_deaths
    
    
    def calculate_impact(self, reach_metrics, avg_age_at_prevention=17):
        """
        Calculate lives saved and cost-effectiveness for YOUR program.
        
        Args:
            reach_metrics: Output from calculate_reach()
            avg_age_at_prevention: Average age of program participants
            
        Returns:
            dict: Impact metrics across three scenarios
        """
        population = reach_metrics['total_individuals_reached']
        expected_deaths = self.calculate_baseline_risk(population)
        
        # Effectiveness rates from crisis intervention literature
        scenarios = {
            'conservative': 0.15,  # 15% reduction
            'moderate': 0.25,      # 25% reduction
            'optimistic': 0.35     # 35% reduction (combined school + hotline)
        }
        
        results = {}
        
        for scenario_name, effectiveness in scenarios.items():
            lives_saved = expected_deaths * effectiveness
            
            # Years of life saved
            years_of_life = self.life_expectancy_japan - avg_age_at_prevention
            dalys_averted = lives_saved * years_of_life
            
            # Economic value
            work_years = self.retirement_age - avg_age_at_prevention
            lifetime_gross_earnings = work_years * self.avg_annual_salary
            lifetime_tax_revenue = lifetime_gross_earnings * self.effective_tax_rate
            
            total_economic_value = lives_saved * lifetime_gross_earnings
            total_tax_revenue = lives_saved * lifetime_tax_revenue
            
            # Cost-effectiveness
            cost_per_life = self.program_cost / lives_saved if lives_saved > 0 else 0
            cost_per_daly = self.program_cost / dalys_averted if dalys_averted > 0 else 0
            cost_per_person_reached = self.program_cost / population
            
            # ROI
            roi_gross = total_economic_value / self.program_cost if self.program_cost > 0 else 0
            roi_tax = total_tax_revenue / self.program_cost if self.program_cost > 0 else 0
            
            # Net benefit
            net_benefit = total_economic_value - self.program_cost
            
            results[scenario_name] = {
                'effectiveness_rate': effectiveness,
                'lives_saved_annually': lives_saved,
                'dalys_averted': dalys_averted,
                'years_of_life_per_person': years_of_life,
                'work_years_per_person': work_years,
                'cost_per_life_saved_jpy': cost_per_life,
                'cost_per_life_saved_million': cost_per_life / 1_000_000,
                'cost_per_daly_jpy': cost_per_daly,
                'cost_per_daly_usd': cost_per_daly / 150,  # Approx exchange rate
                'cost_per_person_reached_jpy': cost_per_person_reached,
                'lifetime_value_per_person': {
                    'gross_earnings_jpy': lifetime_gross_earnings,
                    'gross_earnings_million': lifetime_gross_earnings / 1_000_000,
                    'tax_revenue_jpy': lifetime_tax_revenue,
                    'tax_revenue_million': lifetime_tax_revenue / 1_000_000
                },
                'aggregate_economic_impact': {
                    'total_economic_value_jpy': total_economic_value,
                    'total_economic_value_million': total_economic_value / 1_000_000,
                    'total_tax_revenue_jpy': total_tax_revenue,
                    'total_tax_revenue_million': total_tax_revenue / 1_000_000,
                    'net_benefit_jpy': net_benefit,
                    'net_benefit_million': net_benefit / 1_000_000
                },
                'return_on_investment': {
                    'roi_gross_earnings': roi_gross,
                    'roi_tax_revenue': roi_tax
                }
            }
        
        return results
    
    
    def assess_cost_effectiveness(self, cost_per_daly_usd):
        """
        Compare against WHO cost-effectiveness thresholds.
        
        Args:
            cost_per_daly_usd: Cost per DALY in USD
            
        Returns:
            dict: Assessment results
        """
        # WHO thresholds (using Japan's GDP per capita ~$34,000)
        highly_effective_threshold = 34_000
        cost_effective_threshold = 102_000  # 3× GDP per capita
        
        if cost_per_daly_usd < highly_effective_threshold:
            classification = "HIGHLY COST-EFFECTIVE"
            times_below_threshold = highly_effective_threshold / cost_per_daly_usd
        elif cost_per_daly_usd < cost_effective_threshold:
            classification = "COST-EFFECTIVE"
            times_below_threshold = cost_effective_threshold / cost_per_daly_usd
        else:
            classification = "ABOVE THRESHOLD"
            times_below_threshold = 0
        
        return {
            'classification': classification,
            'who_threshold_highly_effective_usd': highly_effective_threshold,
            'who_threshold_cost_effective_usd': cost_effective_threshold,
            'program_cost_per_daly_usd': cost_per_daly_usd,
            'times_below_threshold': times_below_threshold
        }


def generate_program_report(schools=145, workshops=97, hotline=9000, actual_budget=None,
                            youth_data_csv=None):
    """
    Generate complete impact report for YOUR program only.
    
    Args:
        schools: Schools reached (145)
        workshops: Workshops delivered (97)
        hotline: Annual hotline contacts (9,000)
        actual_budget: Your actual program cost (JPY). If None, calculates estimate.
        youth_data_csv: Path to master_cleaned_dataset.csv with youth suicide data
                       Expected columns: 'year', '年齢層' (with '10～19歳'), '人数_x'
    """
    print("\n" + "="*80)
    print("NONPROFIT PROGRAM COST-EFFECTIVENESS ANALYSIS")
    print("="*80)
    
    # Calculate program cost
    if actual_budget is None:
        cost_calc = NonprofitCostCalculator()
        cost_breakdown = cost_calc.calculate_total_cost()
        program_cost = cost_breakdown['total_program_cost_jpy']
        
        print("\nESTIMATED PROGRAM COST BREAKDOWN:")
        print(f"  Staff salaries: ¥{cost_breakdown['staff_costs_jpy']/1_000_000:.1f}M")
        print(f"  Benefits (15%): ¥{cost_breakdown['benefits_jpy']/1_000_000:.1f}M")
        print(f"  Operating costs: ¥{cost_breakdown['operating_costs_jpy']/1_000_000:.1f}M")
        print(f"  TOTAL ANNUAL COST: ¥{cost_breakdown['total_program_cost_million']:.1f}M")
        print("\n  (Adjust staff_costs in NonprofitCostCalculator to match your actual budget)")
    else:
        program_cost = actual_budget
        print(f"\nPROGRAM ANNUAL BUDGET: ¥{program_cost/1_000_000:.1f}M")
    
    # Initialize model with ACTUAL youth data
    model = ProgramImpactModel(program_cost, youth_data_path=youth_data_csv)
    
    # Display actual youth suicide statistics if loaded
    if model.youth_data:
        print("\n" + "="*80)
        print("ACTUAL YOUTH SUICIDE DATA (from your dataset)")
        print("="*80)
        print(f"  Data period: {model.data_years}")
        print(f"  Total youth suicides (10-19): {model.youth_data['total_suicides']:,}")
        print(f"  Annual average: {model.annual_youth_suicides:.1f} deaths/year")
        print(f"  Most recent year ({model.youth_data['most_recent_year']}): {model.recent_year_suicides} deaths")
        print(f"  Rate per 100,000: {model.youth_suicide_rate_per_100k:.2f}")
        print(f"  Data source: {model.youth_data['data_source']}")
    
    # Calculate reach
    reach = model.calculate_reach(schools, workshops, hotline)
    
    print("\n" + "="*80)
    print("PROGRAM REACH & COVERAGE")
    print("="*80)
    print(f"\nSchool-Based Workshops:")
    print(f"  Schools reached: {reach['schools_reached']:,} / {reach['total_schools_japan']:,}")
    print(f"  Coverage: {reach['school_coverage_pct']:.2f}% of national schools")
    print(f"  Workshops delivered: {reach['workshops_delivered']:,}")
    print(f"  Students reached: {reach['students_in_workshops']:,}")
    
    print(f"\nCrisis Hotline:")
    print(f"  Total contacts: {reach['hotline_contacts_raw']:,}")
    print(f"  Estimated unique individuals: {reach['unique_hotline_contacts']:,}")
    
    print(f"\nTotal Program Reach:")
    print(f"  Individuals reached: {reach['total_individuals_reached']:,}")
    print(f"  National student population: {reach['national_student_population']:,}")
    print(f"  Population coverage: {reach['population_coverage_pct']:.2f}%")
    
    expected_deaths = model.calculate_baseline_risk(reach['total_individuals_reached'])
    print(f"\nBaseline Risk (in YOUR reached population):")
    print(f"  Expected deaths (no intervention): {expected_deaths:.3f} annually")
    print(f"  Youth suicide rate (from your data): {model.youth_suicide_rate_per_100k:.2f} per 100,000")
    
    # Calculate impact
    impact = model.calculate_impact(reach)
    
    print("\n" + "="*80)
    print("COST-EFFECTIVENESS ANALYSIS")
    print("="*80)
    
    for scenario_name, results in impact.items():
        eff_pct = results['effectiveness_rate'] * 100
        
        print(f"\n{scenario_name.upper()} SCENARIO ({eff_pct:.0f}% effectiveness):")
        print(f"  Lives saved: {results['lives_saved_annually']:.3f} annually")
        print(f"  DALYs averted: {results['dalys_averted']:.1f} years")
        print(f"  Cost per life saved: ¥{results['cost_per_life_saved_million']:.1f}M")
        print(f"  Cost per DALY: ¥{results['cost_per_daly_jpy']:,.0f} (~${results['cost_per_daly_usd']:,.0f})")
        print(f"  Cost per person reached: ¥{results['cost_per_person_reached_jpy']:,.0f}")
        
        print(f"\n  Economic Value Saved:")
        print(f"    Total gross earnings: ¥{results['aggregate_economic_impact']['total_economic_value_million']:.1f}M")
        print(f"    Total tax revenue: ¥{results['aggregate_economic_impact']['total_tax_revenue_million']:.1f}M")
        print(f"    Net benefit: ¥{results['aggregate_economic_impact']['net_benefit_million']:.1f}M")
        
        print(f"\n  Return on Investment:")
        print(f"    ROI (gross earnings): {results['return_on_investment']['roi_gross_earnings']:.1f}x")
        print(f"    ROI (tax revenue): {results['return_on_investment']['roi_tax_revenue']:.1f}x")
        
        # WHO assessment
        assessment = model.assess_cost_effectiveness(results['cost_per_daly_usd'])
        print(f"\n  WHO Classification: {assessment['classification']}")
        if assessment['times_below_threshold'] > 0:
            print(f"  ({assessment['times_below_threshold']:.1f}x below WHO threshold)")
    
    print("\n" + "="*80)
    print("INTERPRETATION FOR GRANT PROPOSALS")
    print("="*80)
    
    moderate = impact['moderate']
    assessment = model.assess_cost_effectiveness(moderate['cost_per_daly_usd'])
    
    print(f"\nRecommended claim (moderate scenario):")
    print(f'  "Our program prevents {moderate["lives_saved_annually"]:.2f} deaths annually,')
    print(f'   averting {moderate["dalys_averted"]:.0f} DALYs at ¥{moderate["cost_per_daly_jpy"]:,.0f} per DALY')
    print(f'   (~${moderate["cost_per_daly_usd"]:,.0f} USD), {assessment["times_below_threshold"]:.0f}x below WHO\'s')
    print(f'   threshold for highly cost-effective interventions."')
    
    print(f"\nEconomic ROI:")
    print(f'  "Every ¥1 invested returns ¥{moderate["return_on_investment"]["roi_gross_earnings"]:.1f}')
    print(f'   in prevented productivity losses and ¥{moderate["return_on_investment"]["roi_tax_revenue"]:.1f}')
    print(f'   in preserved tax revenue."')
    
    # Export data
    output = {
        'program_parameters': {
            'schools_reached': schools,
            'workshops_delivered': workshops,
            'hotline_contacts': hotline,
            'program_cost_jpy': program_cost,
            'program_cost_million': program_cost / 1_000_000
        },
        'youth_suicide_data': model.youth_data if model.youth_data else "NOT_LOADED",
        'reach_metrics': reach,
        'baseline_risk': {
            'expected_deaths_no_intervention': expected_deaths,
            'suicide_rate_per_100k': model.youth_suicide_rate_per_100k
        },
        'impact_scenarios': impact,
        'who_assessment': {
            scenario: model.assess_cost_effectiveness(results['cost_per_daly_usd'])
            for scenario, results in impact.items()
        }
    }
    
    with open('nonprofit_impact_report.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=float)
    
    print("\n" + "="*80)
    print("Data exported to: nonprofit_impact_report.json")
    print("="*80 + "\n")
    
    return output


if __name__ == "__main__":
    results = generate_program_report(
        schools=145, 
        workshops=97, 
        hotline=9000,
        actual_budget=10_000_000,  # Replace with your actual budget, or set None to estimate
        youth_data_csv='../../data_clean/master_cleaned_dataset.csv'  # Path to your CSV
        
    )
    
    # Option 2: WITHOUT youth data (will show warning)
    # results = generate_program_report(
    #     schools=145, 
    #     workshops=97, 
    #     hotline=9000,
    #     actual_budget=10_000_000
    # )