"""
Query engine for handling LLM interactions
"""

import ollama
import json
from typing import List
from data_manager import DataAnalyzer

class EnhancedQueryEngine:
    """Handles LLM interactions for Q&A"""
    def __init__(self, analyzer: DataAnalyzer):
        self.analyzer = analyzer
        self.model = "mistral"
        self.context = self._generate_context()

    def _generate_context(self) -> str:
        """Generate enhanced context for the LLM"""
        if not self.analyzer.data_loaded:
            return ""

        context = """You are a specialized pharmacy data analyst assistant. Use the following data to answer questions:

        Medications Database Summary:
        """
        # Add detailed medications summary
        meds_df = self.analyzer.medications_df
        context += f"\nTotal Medications: {len(meds_df)}"
        context += f"\nCategories: {', '.join(meds_df['category'].unique())}"
        context += f"\nTherapeutic Classes: {', '.join(meds_df['therapeutic_class'].unique())}"
        
        # Add price ranges
        context += f"\nPrice Ranges:"
        for category in meds_df['category'].unique():
            cat_prices = meds_df[meds_df['category'] == category]['base_price']
            context += f"\n- {category}: ${cat_prices.min():.2f} to ${cat_prices.max():.2f}"
        
        # Add coverage summary
        rules_df = self.analyzer.price_rules_df
        context += f"\n\nCoverage Summary:"
        for insurance in rules_df['insurance_type'].unique():
            covered_count = len(rules_df[
                (rules_df['insurance_type'] == insurance) & 
                (rules_df['coverage_status'] == 'Covered')
            ])
            context += f"\n- {insurance}: {covered_count} covered medications"
            
        return context

    def _analyze_price(self, medication_name: str) -> str:
        """Analyze pricing details for a specific medication"""
        med = self.analyzer.medications_df[
            self.analyzer.medications_df['name'].str.lower() == medication_name.lower()
        ]
        if med.empty:
            return "Medication not found."
            
        med = med.iloc[0]
        price_rules = self.analyzer.price_rules_df[
            self.analyzer.price_rules_df['medication_id'] == med['id']
        ]
        
        analysis = f"Price Analysis for {med['name']}:\n"
        analysis += f"Base Price: ${med['base_price']:.2f}\n"
        analysis += "\nInsurance Coverage:\n"
        
        for _, rule in price_rules.iterrows():
            final_price = med['base_price'] * (1 - rule['discount_percentage']/100)
            final_price = max(min(final_price, rule['max_copay']), rule['min_copay'])
            analysis += f"- {rule['insurance_type']}: ${final_price:.2f} "
            analysis += f"(Discount: {rule['discount_percentage']}%, Status: {rule['coverage_status']})\n"
            
        return analysis

    def _analyze_coverage(self, insurance_type: str) -> str:
        """Analyze coverage for a specific insurance type"""
        rules = self.analyzer.price_rules_df[
            self.analyzer.price_rules_df['insurance_type'].str.lower() == insurance_type.lower()
        ]
        
        if rules.empty:
            return f"No coverage information found for {insurance_type}."
            
        analysis = f"Coverage Analysis for {insurance_type}:\n\n"
        
        # Coverage status breakdown
        status_counts = rules['coverage_status'].value_counts()
        analysis += "Coverage Status Breakdown:\n"
        for status, count in status_counts.items():
            analysis += f"- {status}: {count} medications\n"
        
        # Average discount
        avg_discount = rules['discount_percentage'].mean()
        analysis += f"\nAverage Discount: {avg_discount:.1f}%\n"
        
        # Copay ranges
        analysis += f"Copay Ranges:\n"
        analysis += f"- Minimum: ${rules['min_copay'].min():.2f}\n"
        analysis += f"- Maximum: ${rules['max_copay'].max():.2f}\n"
        
        return analysis

    def _find_generic_alternatives(self, medication_name: str) -> str:
        """Find generic alternatives for a medication"""
        med = self.analyzer.medications_df[
            self.analyzer.medications_df['name'].str.lower() == medication_name.lower()
        ]
        
        if med.empty:
            return "Medication not found."
            
        med = med.iloc[0]
        if med['category'] == 'Generic':
            return f"{med['name']} is already a generic medication."
            
        if pd.isna(med.get('generic_equivalent')):
            return f"No generic alternative found for {med['name']}."
            
        generic = self.analyzer.medications_df[
            self.analyzer.medications_df['id'] == med['generic_equivalent']
        ].iloc[0]
        
        analysis = f"Generic Alternative for {med['name']}:\n"
        analysis += f"- Generic Name: {generic['name']}\n"
        analysis += f"- Price Comparison:\n"
        analysis += f"  * Brand Price: ${med['base_price']:.2f}\n"
        analysis += f"  * Generic Price: ${generic['base_price']:.2f}\n"
        analysis += f"  * Potential Savings: ${(med['base_price'] - generic['base_price']):.2f}\n"
        
        return analysis

    def _check_authorization_requirements(self, medication_name: str) -> str:
        """Check authorization requirements for a medication"""
        med = self.analyzer.medications_df[
            self.analyzer.medications_df['name'].str.lower() == medication_name.lower()
        ]
        
        if med.empty:
            return "Medication not found."
            
        med = med.iloc[0]
        policies = self.analyzer.policies_df[
            self.analyzer.policies_df['applicable_drugs'].apply(
                lambda x: med['id'] in json.loads(x)
            )
        ]
        
        analysis = f"Authorization Requirements for {med['name']}:\n\n"
        
        if not med['requires_prior_auth']:
            analysis += "This medication does not require prior authorization.\n"
            return analysis
            
        analysis += "Prior Authorization Required\n\n"
        
        if policies.empty:
            analysis += "No specific policy requirements found."
            return analysis
            
        for _, policy in policies.iterrows():
            analysis += f"Policy: {policy['name']}\n"
            analysis += f"Description: {policy['description']}\n"
            analysis += f"Required Documentation:\n"
            for doc in json.loads(policy['required_documentation']):
                analysis += f"- {doc}\n"
            analysis += f"\nOverride Conditions:\n"
            for condition in json.loads(policy['override_conditions']):
                analysis += f"- {condition}\n"
            analysis += "\n"
            
        return analysis

    def get_response(self, question: str) -> str:
        """Get enhanced response using specialized functions and LLM"""
        try:
            # Check for specialized queries first
            lower_question = question.lower()
            
            # Price analysis
            if "price" in lower_question or "cost" in lower_question:
                for med_name in self.analyzer.medications_df['name']:
                    if med_name.lower() in lower_question:
                        return self._analyze_price(med_name)
            
            # Coverage analysis
            if "coverage" in lower_question or "insurance" in lower_question:
                for insurance in ["Commercial", "Medicare", "Medicaid"]:
                    if insurance.lower() in lower_question:
                        return self._analyze_coverage(insurance)
            
            # Generic alternatives
            if "generic" in lower_question:
                for med_name in self.analyzer.medications_df['name']:
                    if med_name.lower() in lower_question:
                        return self._find_generic_alternatives(med_name)
            
            # Authorization requirements
            if "authorization" in lower_question or "requirements" in lower_question:
                for med_name in self.analyzer.medications_df['name']:
                    if med_name.lower() in lower_question:
                        return self._check_authorization_requirements(med_name)
            
            # Default to LLM response
            prompt = f"""
            Context:
            {self.context}
            
            Question: {question}
            
            Please provide a detailed answer based on the data provided.
            Include relevant statistics and comparisons when applicable.
            If the question cannot be answered with the available data, please say so.
            """

            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )

            return response['message']['content']

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def suggest_related_questions(self, current_question: str) -> List[str]:
        """Suggest related questions based on the current query"""
        related_questions = []
        lower_question = current_question.lower()
        
        # Add related questions based on topic
        if "price" in lower_question or "cost" in lower_question:
            related_questions.extend([
                "What are the cheapest medications in this category?",
                "How does this price compare to similar medications?",
                "Are there any generic alternatives available?"
            ])
            
        if "coverage" in lower_question or "insurance" in lower_question:
            related_questions.extend([
                "What are the coverage requirements?",
                "Which insurance type offers the best coverage?",
                "Are prior authorizations required?"
            ])
            
        if "generic" in lower_question:
            related_questions.extend([
                "What is the price difference between brand and generic?",
                "Are there any coverage restrictions for generics?",
                "Which medications have generic alternatives?"
            ])
            
        if "authorization" in lower_question or "requirements" in lower_question:
            related_questions.extend([
                "What documentation is needed?",
                "Are there any override conditions?",
                "How long does authorization typically last?"
            ])
            
        return related_questions[:3]  # Return top 3 related questions
