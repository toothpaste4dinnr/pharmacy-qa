"""
Data management and analysis components
"""

import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class EnhancedDataManager:
    @staticmethod
    def create_expanded_sample_data():
        """Create expanded sample data with more medications and insights"""
        # Create data directory
        Path('data').mkdir(exist_ok=True)
        
        # Expanded medications data
        medications = [
            # Generic Medications
            {'id': 'MED001', 'name': 'Lisinopril', 'category': 'Generic', 'base_price': 15.99, 'manufacturer': 'Generic Pharma Co', 'ndc_code': '12345-678-90', 'quantity_limit': 30, 'requires_prior_auth': False, 'active': True, 'therapeutic_class': 'ACE Inhibitor'},
            {'id': 'MED002', 'name': 'Metformin', 'category': 'Generic', 'base_price': 12.99, 'manufacturer': 'Generic Pharma Co', 'ndc_code': '12345-678-91', 'quantity_limit': 60, 'requires_prior_auth': False, 'active': True, 'therapeutic_class': 'Antidiabetic'},
            {'id': 'MED003', 'name': 'Amlodipine', 'category': 'Generic', 'base_price': 18.99, 'manufacturer': 'Generic Pharma Co', 'ndc_code': '12345-678-92', 'quantity_limit': 30, 'requires_prior_auth': False, 'active': True, 'therapeutic_class': 'Calcium Channel Blocker'},
            
            # Brand Name Medications
            {'id': 'MED004', 'name': 'Lipitor', 'category': 'Brand', 'base_price': 145.99, 'manufacturer': 'Pfizer', 'ndc_code': '98765-432-10', 'generic_equivalent': 'MED005', 'requires_prior_auth': True, 'active': True, 'therapeutic_class': 'Statin'},
            {'id': 'MED005', 'name': 'Atorvastatin', 'category': 'Generic', 'base_price': 25.99, 'manufacturer': 'Generic Pharma Co', 'ndc_code': '11111-222-33', 'quantity_limit': 30, 'requires_prior_auth': False, 'active': True, 'therapeutic_class': 'Statin'},
            {'id': 'MED006', 'name': 'Januvia', 'category': 'Brand', 'base_price': 425.99, 'manufacturer': 'Merck', 'ndc_code': '98765-432-11', 'requires_prior_auth': True, 'active': True, 'therapeutic_class': 'Antidiabetic'},
            
            # Specialty Medications
            {'id': 'MED007', 'name': 'Humira', 'category': 'Specialty', 'base_price': 5250.99, 'manufacturer': 'AbbVie', 'ndc_code': '77777-888-99', 'requires_prior_auth': True, 'active': True, 'therapeutic_class': 'TNF Inhibitor'},
            {'id': 'MED008', 'name': 'Enbrel', 'category': 'Specialty', 'base_price': 4890.99, 'manufacturer': 'Amgen', 'ndc_code': '77777-888-98', 'requires_prior_auth': True, 'active': True, 'therapeutic_class': 'TNF Inhibitor'},
            
            # Controlled Substances
            {'id': 'MED009', 'name': 'Adderall XR', 'category': 'Controlled', 'base_price': 225.99, 'manufacturer': 'Shire', 'ndc_code': '33333-444-55', 'requires_prior_auth': True, 'quantity_limit': 30, 'controlled_substance_schedule': 'II', 'active': True, 'therapeutic_class': 'Stimulant'},
            {'id': 'MED010', 'name': 'Xanax', 'category': 'Controlled', 'base_price': 125.99, 'manufacturer': 'Pfizer', 'ndc_code': '33333-444-56', 'requires_prior_auth': True, 'quantity_limit': 30, 'controlled_substance_schedule': 'IV', 'active': True, 'therapeutic_class': 'Benzodiazepine'}
        ]
        
        # Expanded price rules data
        price_rules = [
            # Commercial Insurance Rules
            {'medication_id': 'MED001', 'insurance_type': 'Commercial', 'discount_percentage': 80.0, 'min_copay': 5.0, 'max_copay': 25.0, 'coverage_status': 'Covered', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 1},
            {'medication_id': 'MED004', 'insurance_type': 'Commercial', 'discount_percentage': 70.0, 'min_copay': 30.0, 'max_copay': 75.0, 'coverage_status': 'Prior Authorization Required', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 3},
            {'medication_id': 'MED007', 'insurance_type': 'Commercial', 'discount_percentage': 60.0, 'min_copay': 100.0, 'max_copay': 500.0, 'coverage_status': 'Prior Authorization Required', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 4},
            
            # Medicare Rules
            {'medication_id': 'MED001', 'insurance_type': 'Medicare', 'discount_percentage': 85.0, 'min_copay': 3.0, 'max_copay': 20.0, 'coverage_status': 'Covered', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 1},
            {'medication_id': 'MED004', 'insurance_type': 'Medicare', 'discount_percentage': 75.0, 'min_copay': 25.0, 'max_copay': 65.0, 'coverage_status': 'Step Therapy Required', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 3},
            
            # Medicaid Rules
            {'medication_id': 'MED001', 'insurance_type': 'Medicaid', 'discount_percentage': 90.0, 'min_copay': 1.0, 'max_copay': 15.0, 'coverage_status': 'Covered', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 1},
            {'medication_id': 'MED007', 'insurance_type': 'Medicaid', 'discount_percentage': 95.0, 'min_copay': 3.0, 'max_copay': 25.0, 'coverage_status': 'Prior Authorization Required', 'effective_date': '2024-01-01', 'expiration_date': '2024-12-31', 'tier': 4}
        ]
        
        # Expanded policies data
        policies = [
            {
                'id': 'POL001',
                'name': 'Generic First Policy',
                'description': 'Requires trial of generic alternatives before brand name drugs',
                'effective_date': '2024-01-01',
                'expiration_date': '2024-12-31',
                'required_documentation': json.dumps(['Previous generic trial', 'Adverse reaction documentation']),
                'applicable_drugs': json.dumps(['MED004', 'MED006']),
                'insurance_types': json.dumps(['Commercial', 'Medicare']),
                'override_conditions': json.dumps(['Documented allergy to generic', 'Treatment failure with generic'])
            },
            {
                'id': 'POL002',
                'name': 'Specialty Authorization Policy',
                'description': 'Requirements for specialty medication coverage',
                'effective_date': '2024-01-01',
                'expiration_date': '2024-12-31',
                'required_documentation': json.dumps(['Diagnosis confirmation', 'Lab results', 'Specialist consultation']),
                'applicable_drugs': json.dumps(['MED007', 'MED008']),
                'insurance_types': json.dumps(['Commercial', 'Medicare', 'Medicaid']),
                'override_conditions': json.dumps(['Urgent need', 'Continuing therapy'])
            },
            {
                'id': 'POL003',
                'name': 'Controlled Substance Policy',
                'description': 'Guidelines for controlled substance prescriptions',
                'effective_date': '2024-01-01',
                'expiration_date': '2024-12-31',
                'required_documentation': json.dumps(['Diagnosis', 'Drug screening', 'Treatment plan']),
                'applicable_drugs': json.dumps(['MED009', 'MED010']),
                'insurance_types': json.dumps(['Commercial', 'Medicare', 'Medicaid']),
                'override_conditions': json.dumps(['Palliative care', 'Cancer treatment'])
            }
        ]
        
        # Save expanded datasets
        pd.DataFrame(medications).to_csv('data/medications.csv', index=False)
        pd.DataFrame(price_rules).to_csv('data/price_rules.csv', index=False)
        pd.DataFrame(policies).to_csv('data/policies.csv', index=False)

class DataAnalyzer:
    """Handles data loading and analysis"""
    def __init__(self):
        self.medications_df = None
        self.price_rules_df = None
        self.policies_df = None
        self.data_loaded = False

    def load_data(self):
        """Load data from CSV files"""
        try:
            # Create sample data if files don't exist
            if not all(Path(f'data/{file}').exists() for file in 
                      ['medications.csv', 'price_rules.csv', 'policies.csv']):
                EnhancedDataManager.create_expanded_sample_data()
            
            self.medications_df = pd.read_csv('data/medications.csv')
            self.price_rules_df = pd.read_csv('data/price_rules.csv')
            self.policies_df = pd.read_csv('data/policies.csv')
            self.data_loaded = True
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False

    def get_data_summary(self) -> Dict:
        """Generate summary statistics of the data"""
        if not self.data_loaded:
            return {}

        return {
            "total_medications": len(self.medications_df),
            "medication_categories": self.medications_df['category'].unique().tolist(),
            "avg_base_price": self.medications_df['base_price'].mean(),
            "total_policies": len(self.policies_df),
            "insurance_types": self.price_rules_df['insurance_type'].unique().tolist(),
            "therapeutic_classes": self.medications_df['therapeutic_class'].unique().tolist()
        }

    def generate_price_distribution_chart(self):
        """Create price distribution visualization"""
        fig = px.box(self.medications_df, 
                    x='category', 
                    y='base_price',
                    title='Medication Price Distribution by Category')
        fig.update_layout(showlegend=True)
        return fig

    def generate_coverage_chart(self):
        """Create coverage status visualization"""
        coverage_counts = self.price_rules_df['coverage_status'].value_counts()
        fig = px.pie(values=coverage_counts.values, 
                    names=coverage_counts.index,
                    title='Coverage Status Distribution')
        return fig

    def generate_therapeutic_class_chart(self):
        """Create therapeutic class distribution visualization"""
        class_counts = self.medications_df['therapeutic_class'].value_counts()
        fig = px.pie(values=class_counts.values,
                     names=class_counts.index,
                     title='Distribution by Therapeutic Class')
        return fig

    def generate_price_trend_chart(self):
        """Create price comparison across categories"""
        fig = px.bar(self.medications_df,
                     x='name',
                     y='base_price',
                     color='category',
                     title='Medication Prices by Category',
                     labels={'base_price': 'Base Price ($)', 'name': 'Medication'})
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    def generate_insurance_coverage_chart(self):
        """Create insurance coverage analysis"""
        coverage_data = self.price_rules_df.groupby(
            ['insurance_type', 'coverage_status']
        ).size().reset_index(name='count')
        fig = px.bar(coverage_data,
                     x='insurance_type',
                     y='count',
                     color='coverage_status',
                     title='Coverage Status by Insurance Type',
                     barmode='group')
        return fig

    def generate_prior_auth_analysis(self):
        """Create prior authorization requirement analysis"""
        auth_by_category = self.medications_df.groupby(
            ['category', 'requires_prior_auth']
        ).size().reset_index(name='count')
        fig = px.bar(auth_by_category,
                     x='category',
                     y='count',
                     color='requires_prior_auth',
                     title='Prior Authorization Requirements by Category',
                     barmode='group',
                     labels={'requires_prior_auth': 'Requires Prior Auth'})
        return fig
