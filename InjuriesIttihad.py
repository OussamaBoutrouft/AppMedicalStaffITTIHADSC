# app.py - AL ITTIHAD SC LIBYA - Injury Management System
# Manual Data Entry | Clinical Dashboard | Load Monitoring | Risk Profile

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Try to import plotly with error handling
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly is not available. Charts will be disabled. Please install plotly: pip install plotly")

# Page configuration
st.set_page_config(
    page_title="AL ITTIHAD SC LIBYA - Injury Management System",
    page_icon="🦁",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Barlow:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Barlow', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0a2e1c 0%, #1a472a 60%, #0d3b22 100%);
        padding: 2rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        text-align: center;
        position: relative;
    }
    
    .club-title {
        font-family: 'Barlow Condensed', sans-serif;
        color: #ffd700;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 4px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
    
    .club-subtitle {
        font-family: 'Barlow Condensed', sans-serif;
        color: #ffd700;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 2px;
        margin-top: -5px;
    }
    
    .subtitle {
        color: #d4edda;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .risk-card-critique {
        background: linear-gradient(135deg, #7b1d1d 0%, #dc3545 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff6b6b;
    }
    
    .risk-card-eleve {
        background: linear-gradient(135deg, #6d3a00 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 5px solid #ffaa5c;
    }
    
    .risk-card-modere {
        background: linear-gradient(135deg, #856404 0%, #ffc107 100%);
        color: #1a1a1a;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 5px solid #ffe08a;
    }
    
    .risk-card-faible {
        background: linear-gradient(135deg, #1a4a2e 0%, #28a745 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 5px solid #6fcf97;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f0f4f0;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Data file
DATA_FILE = "injuries_manual.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

# Initialize session state
if 'injuries' not in st.session_state:
    st.session_state.injuries = load_data()

# Header with AL ITTIHAD SC LIBYA
st.markdown("""
<div class="main-header">
    <div class="club-title">🦁 AL ITTIHAD SC LIBYA</div>
    <div class="club-subtitle">SPORTS MEDICINE DEPARTMENT</div>
    <div class="subtitle">Injury Management System | Clinical Dashboard | Load Monitoring | Risk Profile</div>
    <div class="subtitle" style="font-size:0.75rem; color:#ffc107;">Manual Data Entry - Medical Staff Interface</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR - DATE NAVIGATION
# ──────────────────────────────────────────────────────────────
st.sidebar.markdown("### 📅 DATE NAVIGATION")
st.sidebar.markdown("---")

# Extract unique dates
if st.session_state.injuries:
    dates_list = sorted(list(set([i.get('date', '') for i in st.session_state.injuries if i.get('date')])), reverse=True)
    
    if dates_list:
        selected_date = st.sidebar.selectbox(
            "📆 Select Date",
            options=dates_list,
            format_func=lambda x: f"📅 {x}"
        )
        
        # Filter data by selected date
        filtered_by_date = [i for i in st.session_state.injuries if i.get('date') == selected_date]
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### 📊 Summary for {selected_date}")
        st.sidebar.markdown(f"**Total injuries:** {len(filtered_by_date)}")
        
        contact_count = sum(1 for i in filtered_by_date if i.get('injury_category') == 'Contact')
        non_contact_count = sum(1 for i in filtered_by_date if i.get('injury_category') == 'Non-Contact')
        st.sidebar.markdown(f"**🤕 Contact:** {contact_count}")
        st.sidebar.markdown(f"**🏃 Non-Contact:** {non_contact_count}")
        
        severity_counts = {}
        for i in filtered_by_date:
            sev = i.get('severity', 'Unknown')
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        st.sidebar.markdown("**⚠️ Severity:**")
        for sev, count in severity_counts.items():
            st.sidebar.markdown(f"- {sev}: {count}")
    else:
        selected_date = None
        filtered_by_date = []
else:
    selected_date = None
    filtered_by_date = []

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Clinical Protocols")
st.sidebar.markdown("""
- **MEAT**: Movement, Exercise, Analgesia, Treatment
- **RICE**: Rest, Ice, Compression, Elevation
- **Contact**: Direct impact injuries
- **Non-Contact**: No external contact
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏥 AL ITTIHAD SC LIBYA")
st.sidebar.markdown("*Medical Staff Only*")

# ──────────────────────────────────────────────────────────────
# MAIN CONTENT - ADD NEW INJURY
# ──────────────────────────────────────────────────────────────
st.header("➕ ADD NEW INJURY RECORD")
st.markdown("*Manual entry by medical staff*")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        player_name = st.text_input("👤 Player Name", placeholder="Enter player full name")
    
    with col2:
        injury_date = st.date_input("📅 Injury Date", datetime.today())
    
    with col3:
        # Custom injury type - the doctor writes their own!
        custom_injury = st.text_input("🩺 Injury Diagnosis", placeholder="e.g., Hamstring Strain, ACL, Ankle Sprain...")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        injury_category = st.selectbox(
            "🏥 Injury Category",
            ["Contact", "Non-Contact"]
        )
    
    with col5:
        severity = st.select_slider(
            "⚠️ Severity Level",
            options=["Mild", "Moderate", "Severe", "Critical"],
            value="Moderate"
        )
    
    with col6:
        risk_level = st.select_slider(
            "📊 Risk Level",
            options=["Low", "Medium", "High", "Very High"],
            value="Medium"
        )
    
    col7, col8 = st.columns(2)
    
    with col7:
        meat = st.selectbox("🍖 MEAT Protocol", ["Yes", "No", "Partial", "Not Applicable"])
    
    with col8:
        rice = st.selectbox("🧊 RICE Protocol", ["Yes", "No", "Partial", "Not Applicable"])
    
    # Additional clinical notes
    clinical_notes = st.text_area("📝 Clinical Notes", placeholder="Additional observations, treatment plan, return to play estimate...", height=80)
    
    # Submit button
    if st.button("💾 SAVE INJURY RECORD", type="primary", use_container_width=True):
        if player_name and custom_injury:
            new_injury = {
                "id": len(st.session_state.injuries) + 1,
                "name": player_name,
                "date": injury_date.strftime("%Y-%m-%d"),
                "injury_type": custom_injury,
                "injury_category": injury_category,
                "severity": severity,
                "meat": meat,
                "rice": rice,
                "risk": risk_level,
                "clinical_notes": clinical_notes,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.injuries.append(new_injury)
            save_data(st.session_state.injuries)
            st.success(f"✅ Injury record for {player_name} saved successfully!")
            st.rerun()
        elif not player_name:
            st.error("❌ Please enter player name!")
        elif not custom_injury:
            st.error("❌ Please enter injury diagnosis!")

st.markdown("---")

# ──────────────────────────────────────────────────────────────
# MAIN TABLE - INJURIES DATABASE
# ──────────────────────────────────────────────────────────────
st.header("📋 INJURIES DATABASE")

if filtered_by_date and selected_date:
    df_display = pd.DataFrame(filtered_by_date)
    
    # Select and rename columns for display
    display_cols = ['name', 'date', 'injury_type', 'injury_category', 'severity', 'meat', 'rice', 'risk']
    display_names = ['Player Name', 'Date', 'Injury Diagnosis', 'Category', 'Severity', 'MEAT', 'RICE', 'Risk']
    
    available_cols = [col for col in display_cols if col in df_display.columns]
    if available_cols:
        df_table = df_display[available_cols].copy()
        df_table.columns = display_names[:len(available_cols)]
        
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True
        )
        
        # Show clinical notes for selected injury
        if len(df_display) > 0:
            st.markdown("#### 📝 Clinical Notes Details")
            for idx, injury in df_display.iterrows():
                if injury.get('clinical_notes'):
                    with st.expander(f"👤 {injury['name']} - {injury['injury_type']} - {injury['date']}"):
                        st.write(injury['clinical_notes'])
else:
    st.info("👈 Select a date from the sidebar to view injury records or add new injuries above")

st.markdown("---")

# ──────────────────────────────────────────────────────────────
# CLINICAL DASHBOARD TABS
# ──────────────────────────────────────────────────────────────

if st.session_state.injuries and PLOTLY_AVAILABLE:
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Clinical Dashboard",
        "📈 Load Monitoring",
        "🎯 Risk Profile",
        "📋 Injured Players Analysis"
    ])
    
    # ─── TAB 1: Clinical Dashboard ───
    with tab1:
        st.header("Clinical Dashboard - AL ITTIHAD SC LIBYA")
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_injuries = len(st.session_state.injuries)
        unique_players = len(set(i.get('name', '') for i in st.session_state.injuries))
        critical_count = sum(1 for i in st.session_state.injuries if i.get('severity') == 'Critical')
        high_risk_count = sum(1 for i in st.session_state.injuries if i.get('risk') in ['High', 'Very High'])
        
        with col1:
            st.metric("📊 Total Injuries", total_injuries)
        with col2:
            st.metric("👥 Players Affected", unique_players)
        with col3:
            st.metric("🚨 Critical Cases", critical_count)
        with col4:
            st.metric("⚠️ High Risk", high_risk_count)
        
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Injuries by Category")
            category_counts = {}
            for i in st.session_state.injuries:
                cat = i.get('injury_category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            if category_counts:
                fig_pie = px.pie(
                    values=list(category_counts.values()),
                    names=list(category_counts.keys()),
                    title="Contact vs Non-Contact Injuries",
                    color_discrete_sequence=['#dc3545', '#28a745'],
                    hole=0.3
                )
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Injuries by Severity")
            severity_counts = {}
            for i in st.session_state.injuries:
                sev = i.get('severity', 'Unknown')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            if severity_counts:
                colors_sev = {'Mild': '#28a745', 'Moderate': '#ffc107', 'Severe': '#fd7e14', 'Critical': '#dc3545'}
                fig_bar = px.bar(
                    x=list(severity_counts.keys()),
                    y=list(severity_counts.values()),
                    title="Severity Distribution",
                    color=list(severity_counts.keys()),
                    color_discrete_map=colors_sev,
                    labels={'x': 'Severity', 'y': 'Count'}
                )
                fig_bar.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Injury Diagnoses")
            injury_type_counts = {}
            for i in st.session_state.injuries:
                inj_type = i.get('injury_type', 'Unknown')
                injury_type_counts[inj_type] = injury_type_counts.get(inj_type, 0) + 1
            
            if injury_type_counts:
                top_injuries = dict(sorted(injury_type_counts.items(), key=lambda x: x[1], reverse=True)[:5])
                fig_horiz = px.bar(
                    x=list(top_injuries.values()),
                    y=list(top_injuries.keys()),
                    orientation='h',
                    title="Most Common Injuries",
                    color=list(top_injuries.values()),
                    color_continuous_scale='Reds',
                    labels={'x': 'Number of Cases', 'y': 'Injury Type'}
                )
                fig_horiz.update_layout(height=400)
                st.plotly_chart(fig_horiz, use_container_width=True)
        
        with col2:
            st.subheader("Risk Distribution")
            risk_counts = {}
            for i in st.session_state.injuries:
                risk = i.get('risk', 'Unknown')
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
            
            if risk_counts:
                risk_order = ['Low', 'Medium', 'High', 'Very High']
                risk_colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#fd7e14', 'Very High': '#dc3545'}
                available_risks = [r for r in risk_order if r in risk_counts]
                fig_risk = px.pie(
                    values=[risk_counts.get(r, 0) for r in available_risks],
                    names=available_risks,
                    title="Risk Level Distribution",
                    color=available_risks,
                    color_discrete_map=risk_colors
                )
                fig_risk.update_layout(height=400)
                st.plotly_chart(fig_risk, use_container_width=True)
    
    # ─── TAB 2: Load Monitoring ───
    with tab2:
        st.header("Load Monitoring Analysis")
        st.caption("Based on injury frequency and severity patterns")
        
        # Injuries over time
        st.subheader("📅 Injury Timeline")
        
        # Group injuries by date
        date_counts = {}
        for i in st.session_state.injuries:
            date = i.get('date', '')
            if date:
                date_counts[date] = date_counts.get(date, 0) + 1
        
        if date_counts:
            dates_sorted = sorted(date_counts.keys())
            counts_sorted = [date_counts[d] for d in dates_sorted]
            
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=dates_sorted,
                y=counts_sorted,
                mode='lines+markers',
                name='Injuries',
                line=dict(color='#dc3545', width=2),
                marker=dict(size=8, color='#dc3545')
            ))
            fig_line.update_layout(
                title="Number of Injuries Over Time",
                xaxis_title="Date",
                yaxis_title="Number of Injuries",
                height=450
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Player load analysis
        st.subheader("👥 Player Injury Load")
        
        player_counts = {}
        for i in st.session_state.injuries:
            player = i.get('name', '')
            if player:
                player_counts[player] = player_counts.get(player, 0) + 1
        
        if player_counts:
            top_players = dict(sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            
            fig_player = px.bar(
                x=list(top_players.values()),
                y=list(top_players.keys()),
                orientation='h',
                title="Players with Most Injuries",
                color=list(top_players.values()),
                color_continuous_scale='OrRd',
                labels={'x': 'Number of Injuries', 'y': 'Player'}
            )
            fig_player.update_layout(height=500)
            st.plotly_chart(fig_player, use_container_width=True)
        
        # Severity over time
        st.subheader("⚠️ Severity Trend Over Time")
        
        severity_score = {'Mild': 1, 'Moderate': 2, 'Severe': 3, 'Critical': 4}
        
        severity_over_time = []
        for i in st.session_state.injuries:
            date = i.get('date')
            sev = i.get('severity', 'Moderate')
            if date:
                severity_over_time.append({
                    'Date': date,
                    'Severity Score': severity_score.get(sev, 2),
                    'Player': i.get('name', ''),
                    'Injury': i.get('injury_type', '')
                })
        
        if severity_over_time:
            df_sev = pd.DataFrame(severity_over_time)
            df_sev['Date'] = pd.to_datetime(df_sev['Date'])
            df_pivot = df_sev.groupby('Date')['Severity Score'].mean().reset_index()
            
            fig_heat = px.bar(
                df_pivot,
                x='Date',
                y='Severity Score',
                title="Average Severity Score Over Time (1=Mild, 4=Critical)",
                color='Severity Score',
                color_continuous_scale='RdYlGn_r',
                labels={'Severity Score': 'Severity Level'}
            )
            fig_heat.update_layout(height=400)
            st.plotly_chart(fig_heat, use_container_width=True)
    
    # ─── TAB 3: Risk Profile ───
    with tab3:
        st.header("Risk Profile Analysis")
        
        # Player selection
        all_players_list = sorted(list(set(i.get('name', '') for i in st.session_state.injuries if i.get('name'))))
        if all_players_list:
            selected_risk_player = st.selectbox("Select Player for Risk Profile", all_players_list, key="risk_player_sel")
            
            if selected_risk_player:
                player_injuries = [i for i in st.session_state.injuries if i.get('name') == selected_risk_player]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Injuries", len(player_injuries))
                with col2:
                    high_risk_count_player = sum(1 for i in player_injuries if i.get('risk') in ['High', 'Very High'])
                    st.metric("High Risk Injuries", high_risk_count_player)
                with col3:
                    severe_count = sum(1 for i in player_injuries if i.get('severity') in ['Severe', 'Critical'])
                    st.metric("Severe/Critical", severe_count)
                
                # Risk radar chart
                st.subheader(f"Risk Profile - {selected_risk_player}")
                
                injury_risk_scores = {}
                for injury in player_injuries:
                    inj_type = injury.get('injury_type', 'Unknown')
                    risk_score = {'Low': 25, 'Medium': 50, 'High': 75, 'Very High': 100}.get(injury.get('risk', 'Medium'), 50)
                    if inj_type not in injury_risk_scores:
                        injury_risk_scores[inj_type] = []
                    injury_risk_scores[inj_type].append(risk_score)
                
                if injury_risk_scores:
                    risk_avg = {k: sum(v)/len(v) for k, v in injury_risk_scores.items()}
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=list(risk_avg.values()),
                        theta=list(risk_avg.keys()),
                        fill='toself',
                        fillcolor='rgba(220,53,69,0.3)',
                        line=dict(color='#dc3545', width=2),
                        name=f"{selected_risk_player} - Risk Profile"
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                tickvals=[25, 50, 75, 100],
                                ticktext=['Low', 'Medium', 'High', 'Very High']
                            )
                        ),
                        title=f"Injury-Specific Risk Profile for {selected_risk_player}",
                        height=500,
                        showlegend=True
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                # Timeline
                st.subheader(f"Injury Timeline - {selected_risk_player}")
                player_timeline = []
                for injury in sorted(player_injuries, key=lambda x: x.get('date', '')):
                    player_timeline.append({
                        'Date': injury.get('date', ''),
                        'Injury': injury.get('injury_type', ''),
                        'Severity': injury.get('severity', ''),
                        'Risk': injury.get('risk', '')
                    })
                
                if player_timeline:
                    df_timeline = pd.DataFrame(player_timeline)
                    st.dataframe(df_timeline, use_container_width=True, hide_index=True)
            
            # Global risk matrix
            st.subheader("📊 Global Risk Matrix - AL ITTIHAD SC LIBYA")
            
            risk_by_severity = {}
            for i in st.session_state.injuries:
                risk = i.get('risk', 'Unknown')
                sev = i.get('severity', 'Unknown')
                key = f"{risk} - {sev}"
                risk_by_severity[key] = risk_by_severity.get(key, 0) + 1
            
            if risk_by_severity:
                df_matrix = pd.DataFrame(list(risk_by_severity.items()), columns=['Risk-Severity Combination', 'Count'])
                st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    
    # ─── TAB 4: Injured Players Analysis ───
    with tab4:
        st.header("Injured Players Analysis - AL ITTIHAD SC LIBYA")
        
        all_players_list = sorted(list(set(i.get('name', '') for i in st.session_state.injuries if i.get('name'))))
        if all_players_list:
            selected_analysis_player = st.selectbox("Select Player for Detailed Analysis", all_players_list, key="analysis_player_sel")
            
            if selected_analysis_player:
                player_injuries = [i for i in st.session_state.injuries if i.get('name') == selected_analysis_player]
                
                st.subheader(f"🏥 Complete Injury History - {selected_analysis_player}")
                
                # Summary cards
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Episodes", len(player_injuries))
                with col2:
                    contact_count_p = sum(1 for i in player_injuries if i.get('injury_category') == 'Contact')
                    st.metric("Contact Injuries", contact_count_p)
                with col3:
                    non_contact_p = sum(1 for i in player_injuries if i.get('injury_category') == 'Non-Contact')
                    st.metric("Non-Contact", non_contact_p)
                with col4:
                    risk_values = {'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4}
                    avg_risk = sum(risk_values.get(i.get('risk', 'Medium'), 2) for i in player_injuries) / len(player_injuries)
                    st.metric("Avg Risk Score", f"{avg_risk:.1f}/4")
                
                # Detailed table
                df_player = pd.DataFrame(player_injuries)
                display_player_cols = ['date', 'injury_type', 'injury_category', 'severity', 'meat', 'rice', 'risk', 'clinical_notes']
                available_cols = [col for col in display_player_cols if col in df_player.columns]
                if available_cols:
                    st.dataframe(df_player[available_cols], use_container_width=True, hide_index=True)
                
                # Charts
                st.subheader(f"Injury Distribution - {selected_analysis_player}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    player_injury_types = {}
                    for i in player_injuries:
                        inj = i.get('injury_type', 'Unknown')
                        player_injury_types[inj] = player_injury_types.get(inj, 0) + 1
                    
                    if player_injury_types:
                        fig_player_pie = px.pie(
                            values=list(player_injury_types.values()),
                            names=list(player_injury_types.keys()),
                            title=f"Injury Types for {selected_analysis_player}",
                            hole=0.3
                        )
                        fig_player_pie.update_layout(height=400)
                        st.plotly_chart(fig_player_pie, use_container_width=True)
                
                with col2:
                    player_severity = {}
                    for i in player_injuries:
                        sev = i.get('severity', 'Unknown')
                        player_severity[sev] = player_severity.get(sev, 0) + 1
                    
                    if player_severity:
                        fig_player_sev = px.bar(
                            x=list(player_severity.keys()),
                            y=list(player_severity.values()),
                            title=f"Severity Distribution for {selected_analysis_player}",
                            color=list(player_severity.keys()),
                            color_discrete_map={'Mild': '#28a745', 'Moderate': '#ffc107', 'Severe': '#fd7e14', 'Critical': '#dc3545'}
                        )
                        fig_player_sev.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig_player_sev, use_container_width=True)
            
            # Global players summary
            st.subheader("📊 All Players Summary - AL ITTIHAD SC LIBYA")
            
            players_summary = []
            for player in all_players_list:
                player_data = [i for i in st.session_state.injuries if i.get('name') == player]
                players_summary.append({
                    'Player': player,
                    'Total Injuries': len(player_data),
                    'Contact': sum(1 for i in player_data if i.get('injury_category') == 'Contact'),
                    'Non-Contact': sum(1 for i in player_data if i.get('injury_category') == 'Non-Contact'),
                    'Critical/Severe': sum(1 for i in player_data if i.get('severity') in ['Severe', 'Critical']),
                    'High/Very High Risk': sum(1 for i in player_data if i.get('risk') in ['High', 'Very High'])
                })
            
            if players_summary:
                df_summary = pd.DataFrame(players_summary)
                st.dataframe(df_summary, use_container_width=True, hide_index=True)
                
                # Export button
                csv_summary = df_summary.to_csv(index=False)
                st.download_button(
                    label="📥 Export Players Summary to CSV",
                    data=csv_summary,
                    file_name=f"al_ittihad_players_summary_{datetime.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No players found. Add some injuries first!")

elif st.session_state.injuries and not PLOTLY_AVAILABLE:
    st.warning("⚠️ Plotly is not installed. Charts are disabled. Please add 'plotly' to your requirements.txt file.")
    
    # Show basic data without charts
    st.header("Injuries Database - Basic View")
    df_all = pd.DataFrame(st.session_state.injuries)
    st.dataframe(df_all, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# EXPORT & CLEAR DATA
# ──────────────────────────────────────────────────────────────
if st.session_state.injuries:
    st.markdown("---")
    col_export, col_clear = st.columns(2)
    
    with col_export:
        export_df_all = pd.DataFrame(st.session_state.injuries)
        csv_all = export_df_all.to_csv(index=False)
        st.download_button(
            label="📥 Export All Injuries to CSV",
            data=csv_all,
            file_name=f"al_ittihad_all_injuries_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col_clear:
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.injuries = []
            save_data([])
            st.success("All data cleared!")
            st.rerun()

# Footer
st.markdown("---")
st.markdown("### ℹ️ Clinical Guidelines - AL ITTIHAD SC LIBYA")
col_meat, col_rice = st.columns(2)
with col_meat:
    st.markdown("**🍖 MEAT Protocol**")
    st.markdown("- **M**ovement: Early active mobilization")
    st.markdown("- **E**xercise: Specific strengthening")
    st.markdown("- **A**nalgesia: Pain management")
    st.markdown("- **T**reatment: Continue active care")
with col_rice:
    st.markdown("**🧊 RICE Protocol**")
    st.markdown("- **R**est: Protect from further injury")
    st.markdown("- **I**ce: Apply cold therapy")
    st.markdown("- **C**ompression: Reduce swelling")
    st.markdown("- **E**levation: Above heart level")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #1a472a; font-weight: 600;'>AL ITTIHAD SC LIBYA - Sports Medicine Department © 2024</p>", unsafe_allow_html=True)
