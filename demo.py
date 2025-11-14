"""
Interactive Demo Application
Streamlit app for exploring cultural bias in LLMs
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

import config
from scenarios import ALL_SCENARIOS, get_scenario_by_id
from prompt_constructor import PromptConstructor
from llm_interface import LLMInterface
from response_parser import ResponseParser
from evaluator import CulturalEvaluator

# Page config
st.set_page_config(
    page_title="Cultural Bias in LLMs",
    page_icon="🌍",
    layout="wide"
)

# Initialize components
@st.cache_resource
def get_components():
    return {
        'prompt_constructor': PromptConstructor(),
        'llm_interface': LLMInterface(),
        'parser': ResponseParser(),
        'evaluator': CulturalEvaluator()
    }

components = get_components()


def main():
    st.title("🌍 Cultural Bias in Large Language Models")
    st.markdown("""
    This interactive demo explores how different LLMs respond to culturally-ambiguous scenarios
    when prompted to adopt different cultural perspectives.
    """)
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # Scenario selection
    scenario_options = {f"{s.id}: {s.category}" : s.id for s in ALL_SCENARIOS}
    selected_scenario_label = st.sidebar.selectbox(
        "Select Scenario",
        options=list(scenario_options.keys())
    )
    selected_scenario_id = scenario_options[selected_scenario_label]
    scenario = get_scenario_by_id(selected_scenario_id)
    
    # Model selection
    selected_models = st.sidebar.multiselect(
        "Select Models",
        options=list(config.MODELS.keys()),
        default=["gpt-4"]
    )
    
    # Culture selection
    selected_cultures = st.sidebar.multiselect(
        "Select Cultures",
        options=list(config.CULTURAL_CONTEXTS.keys()),
        default=["baseline", "US", "Japan"]
    )
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Scenario")
        st.info(scenario.get_prompt_text())
        st.caption(f"Category: {scenario.category}")
        st.caption(f"Dimensions: {', '.join(scenario.cultural_dimensions)}")
    
    with col2:
        st.subheader("🎯 Instructions")
        st.markdown("""
        1. Select a scenario from the sidebar
        2. Choose which models to test
        3. Choose which cultures to compare
        4. Click "Generate Responses" below
        5. View and compare the culturally-contextualized responses
        """)
    
    # Generate button
    if st.button("🚀 Generate Responses", type="primary"):
        if not selected_models:
            st.error("Please select at least one model")
            return
        if not selected_cultures:
            st.error("Please select at least one culture")
            return
        
        generate_and_display_responses(
            scenario,
            selected_models,
            selected_cultures,
            components
        )


def generate_and_display_responses(scenario, models, cultures, components):
    """Generate and display responses for all combinations"""
    
    st.subheader("🤖 Model Responses")
    
    results = []
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(models) * len(cultures)
    current = 0
    
    for model in models:
        for culture in cultures:
            status_text.text(f"Generating response for {model} × {culture}...")
            
            try:
                # Generate response
                system_prompt, user_prompt = components['prompt_constructor'].build_complete_prompt(
                    scenario, culture
                )
                response_text = components['llm_interface'].call_model(
                    model, system_prompt, user_prompt
                )
                
                # Parse response
                parsed = components['parser'].parse_response(response_text)
                
                # Evaluate
                metrics = components['evaluator'].evaluate_response(
                    parsed, culture, scenario.cultural_dimensions
                )
                
                results.append({
                    'model': model,
                    'culture': culture,
                    'response': response_text,
                    'parsed': parsed,
                    'metrics': metrics
                })
                
            except Exception as e:
                st.error(f"Error with {model} × {culture}: {str(e)}")
            
            current += 1
            progress_bar.progress(current / total)
    
    status_text.text("✅ All responses generated!")
    progress_bar.empty()
    
    # Display results
    display_results(results, cultures, models)


def display_results(results, cultures, models):
    """Display results in organized tabs"""
    
    tabs = st.tabs(["💬 Responses", "📊 Analysis", "🎯 Metrics"])
    
    with tabs[0]:
        display_responses_tab(results, cultures, models)
    
    with tabs[1]:
        display_analysis_tab(results)
    
    with tabs[2]:
        display_metrics_tab(results)


def display_responses_tab(results, cultures, models):
    """Display response comparison"""
    st.subheader("Response Comparison")
    
    # Create comparison view
    for culture in cultures:
        st.markdown(f"### {culture}")
        
        cols = st.columns(len(models))
        
        for idx, model in enumerate(models):
            result = next((r for r in results if r['model'] == model and r['culture'] == culture), None)
            
            if result:
                with cols[idx]:
                    st.markdown(f"**{model}**")
                    
                    with st.expander("View Full Response"):
                        st.text(result['response'])
                    
                    if result['parsed'].parse_success:
                        st.success("✅ Parsed successfully")
                        st.markdown(f"**Decision:** {result['parsed'].decision}")
                        st.markdown(f"**Top Values:**")
                        for value in result['parsed'].top_values:
                            st.markdown(f"- {value}")
                    else:
                        st.warning("⚠️ Parse errors")
        
        st.divider()


def display_analysis_tab(results):
    """Display analysis charts"""
    st.subheader("Cultural Differentiation Analysis")
    
    # Prepare data for plotting
    data = []
    for result in results:
        data.append({
            'Model': result['model'],
            'Culture': result['culture'],
            'Decision': result['parsed'].decision,
            'Cultural Alignment': result['metrics'].cultural_alignment_score
        })
    
    df = pd.DataFrame(data)
    
    # Plot 1: Cultural alignment by model and culture
    fig1 = px.bar(
        df,
        x='Culture',
        y='Cultural Alignment',
        color='Model',
        barmode='group',
        title='Cultural Alignment Scores',
        labels={'Cultural Alignment': 'Alignment Score (0-10)'}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Plot 2: Decision distribution
    fig2 = px.histogram(
        df,
        x='Culture',
        color='Decision',
        title='Decision Distribution by Culture',
        barmode='group'
    )
    st.plotly_chart(fig2, use_container_width=True)


def display_metrics_tab(results):
    """Display detailed metrics"""
    st.subheader("Detailed Metrics")
    
    # Create metrics table
    metrics_data = []
    for result in results:
        metrics = result['metrics']
        metrics_data.append({
            'Model': result['model'],
            'Culture': result['culture'],
            'Cultural Alignment': f"{metrics.cultural_alignment_score:.2f}",
            'Consistency': f"{metrics.consistency_score:.2f}",
            'Differentiation': f"{metrics.cultural_differentiation_score:.2f}",
            'Stereotype Score': f"{metrics.stereotype_score:.2f}"
        })
    
    df = pd.DataFrame(metrics_data)
    st.dataframe(df, use_container_width=True)
    
    # Radar chart for overall comparison
    if len(results) > 0:
        st.subheader("Model Comparison Radar Chart")
        
        fig = go.Figure()
        
        for model in set(r['model'] for r in results):
            model_results = [r for r in results if r['model'] == model]
            
            metrics = ['cultural_alignment_score', 'consistency_score', 
                      'cultural_differentiation_score', 'stereotype_score']
            
            values = [
                sum(r['metrics'].cultural_alignment_score for r in model_results) / len(model_results),
                sum(r['metrics'].consistency_score for r in model_results) / len(model_results),
                sum(r['metrics'].cultural_differentiation_score for r in model_results) / len(model_results),
                sum(r['metrics'].stereotype_score for r in model_results) / len(model_results)
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=['Alignment', 'Consistency', 'Differentiation', 'Low Stereotypes'],
                fill='toself',
                name=model
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
