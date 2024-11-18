"""
Main Streamlit application for Pharmacy Data Q&A
"""

import streamlit as st
import pandas as pd
from data_manager import DataAnalyzer
from query_engine import EnhancedQueryEngine
from typing import Dict
import plotly.express as px

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "💬 Q&A Chat"
    if 'show_related' not in st.session_state:
        st.session_state.show_related = True

def render_sidebar(analyzer: DataAnalyzer):
    """Render sidebar with data summary and navigation"""
    with st.sidebar:
        st.header("📊 Pharmacy Data Assistant")
        
        # Navigation
        st.subheader("Navigation")
        view_options = {
            "chat": "💬 Q&A Chat",
            "analytics": "📈 Analytics Dashboard",
            "data": "🔍 Data Explorer"
        }
        selected_view = st.radio("Select View", list(view_options.values()))
        st.session_state.current_view = selected_view
        
        # Data Summary
        st.subheader("Data Summary")
        summary = analyzer.get_data_summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Medications", summary["total_medications"])
            st.metric("Total Policies", summary["total_policies"])
        with col2:
            st.metric("Average Price", f"${summary['avg_base_price']:.2f}")
        
        with st.expander("Medication Categories", expanded=False):
            for category in summary["medication_categories"]:
                st.write(f"• {category}")
                
        with st.expander("Therapeutic Classes", expanded=False):
            for th_class in summary["therapeutic_classes"]:
                st.write(f"• {th_class}")
                
        with st.expander("Insurance Types", expanded=False):
            for insurance in summary["insurance_types"]:
                st.write(f"• {insurance}")

def render_chat_view(query_engine: EnhancedQueryEngine):
    """Render the Q&A chat interface"""
    st.header("💬 Pharmacy Data Q&A")
    
    # Sample questions
    st.subheader("Sample Questions")
    sample_questions = [
        "What is the most expensive medication?",
        "How many medications require prior authorization?",
        "What is the average price of generic medications?",
        "Which insurance type has the best coverage?",
        "Tell me about specialty medications",
        "What medications have generic alternatives?"
    ]
    
    # Create columns for sample questions
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        if cols[i % 2].button(f"📝 {question}"):
            with st.spinner("Analyzing..."):
                response = query_engine.get_response(question)
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": response
                })
                
                # Get related questions
                if st.session_state.show_related:
                    related = query_engine.suggest_related_questions(question)
                    st.session_state.chat_history[-1]["related"] = related
    
    # Custom question input
    st.subheader("Ask Your Question")
    with st.form(key="question_form"):
        user_question = st.text_input("Type your question here:", key="question_input")
        col1, col2 = st.columns([1, 4])
        submit_button = col1.form_submit_button("Ask Question")
        col2.checkbox("Show related questions", key="show_related", 
                     value=st.session_state.show_related)
    
    if submit_button and user_question:
        with st.spinner("Analyzing..."):
            response = query_engine.get_response(user_question)
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": response
            })
            
            # Get related questions if enabled
            if st.session_state.show_related:
                related = query_engine.suggest_related_questions(user_question)
                st.session_state.chat_history[-1]["related"] = related
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q: {chat['question']}", expanded=(i == 0)):
                st.markdown(chat['answer'])
                if "related" in chat and st.session_state.show_related:
                    st.markdown("---")
                    st.markdown("**Related Questions:**")
                    for rel_q in chat['related']:
                        if st.button(f"🔄 {rel_q}", key=f"rel_{i}_{rel_q}"):
                            with st.spinner("Analyzing..."):
                                response = query_engine.get_response(rel_q)
                                st.session_state.chat_history.append({
                                    "question": rel_q,
                                    "answer": response
                                })

def render_analytics_view(analyzer: DataAnalyzer):
    """Render the analytics dashboard"""
    st.header("📈 Analytics Dashboard")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs([
        "Price Analysis",
        "Coverage Analysis",
        "Authorization Analysis"
    ])
    
    with tab1:
        st.subheader("Price Distribution and Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                analyzer.generate_price_distribution_chart(),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                analyzer.generate_price_trend_chart(),
                use_container_width=True
            )
            
    with tab2:
        st.subheader("Insurance Coverage Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                analyzer.generate_coverage_chart(),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                analyzer.generate_insurance_coverage_chart(),
                use_container_width=True
            )
            
    with tab3:
        st.subheader("Authorization Requirements")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                analyzer.generate_prior_auth_analysis(),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                analyzer.generate_therapeutic_class_chart(),
                use_container_width=True
            )

def render_data_explorer(analyzer: DataAnalyzer):
    """Render the data explorer view"""
    st.header("🔍 Data Explorer")
    
    # Create tabs for different datasets
    tab1, tab2, tab3 = st.tabs(["Medications", "Price Rules", "Policies"])
    
    with tab1:
        st.subheader("Medications Database")
        
        # Filters for medications
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_categories = st.multiselect(
                "Filter by Category",
                options=analyzer.medications_df['category'].unique()
            )
        with col2:
            selected_classes = st.multiselect(
                "Filter by Therapeutic Class",
                options=analyzer.medications_df['therapeutic_class'].unique()
            )
        with col3:
            price_range = st.slider(
                "Price Range",
                min_value=float(analyzer.medications_df['base_price'].min()),
                max_value=float(analyzer.medications_df['base_price'].max()),
                value=(float(analyzer.medications_df['base_price'].min()),
                      float(analyzer.medications_df['base_price'].max()))
            )
        
        # Apply filters
        filtered_meds = analyzer.medications_df.copy()
        if selected_categories:
            filtered_meds = filtered_meds[
                filtered_meds['category'].isin(selected_categories)
            ]
        if selected_classes:
            filtered_meds = filtered_meds[
                filtered_meds['therapeutic_class'].isin(selected_classes)
            ]
        filtered_meds = filtered_meds[
            (filtered_meds['base_price'] >= price_range[0]) &
            (filtered_meds['base_price'] <= price_range[1])
        ]
        
        st.dataframe(
            filtered_meds,
            column_config={
                "base_price": st.column_config.NumberColumn(
                    "Base Price",
                    format="$%.2f"
                )
            },
            use_container_width=True
        )
        
    with tab2:
        st.subheader("Price Rules")
        
        # Filters for price rules
        col1, col2 = st.columns(2)
        with col1:
            selected_insurance = st.multiselect(
                "Filter by Insurance",
                options=analyzer.price_rules_df['insurance_type'].unique()
            )
        with col2:
            selected_status = st.multiselect(
                "Filter by Coverage Status",
                options=analyzer.price_rules_df['coverage_status'].unique()
            )
        
        # Apply filters
        filtered_rules = analyzer.price_rules_df.copy()
        if selected_insurance:
            filtered_rules = filtered_rules[
                filtered_rules['insurance_type'].isin(selected_insurance)
            ]
        if selected_status:
            filtered_rules = filtered_rules[
                filtered_rules['coverage_status'].isin(selected_status)
            ]
        
        st.dataframe(filtered_rules, use_container_width=True)
        
    with tab3:
        st.subheader("Policies")
        st.dataframe(analyzer.policies_df, use_container_width=True)

def main():
    # Page config
    st.set_page_config(
        page_title="Pharmacy Data Assistant",
        page_icon="💊",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    try:
        # Initialize components
        analyzer = DataAnalyzer()
        
        # Load data
        with st.spinner("Loading data..."):
            if not analyzer.load_data():
                st.error("Failed to load data. Please check your data files.")
                return
            
        # Initialize query engine
        query_engine = EnhancedQueryEngine(analyzer)
        
        # Render sidebar
        render_sidebar(analyzer)
        
        # Render main content based on selected view
        if st.session_state.current_view == "💬 Q&A Chat":
            render_chat_view(query_engine)
        elif st.session_state.current_view == "📈 Analytics Dashboard":
            render_analytics_view(analyzer)
        else:
            render_data_explorer(analyzer)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")

if __name__ == "__main__":
    main()
