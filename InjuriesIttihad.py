# app.py - AL ITTIHAD SC LIBYA - Injury Management System
# CORRECTED VERSION - No KeyError

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

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

# Header
st.markdown("""
<div class="main-header">
    <div class="club-title">🦁 AL ITTIHAD SC LIBYA</div>
    <div class="club-subtitle">SPORTS MEDICINE DEPARTMENT</div>
    <div class="subtitle">Injury Management System | Clinical Dashboard | Load Monitoring | Risk Profile</div>
    <div class="subtitle" style="font-size:0.75rem; color:#ffc107;">Manual Data Entry - Medical Staff Interface</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
st.sidebar.markdown("### 📅 DATE NAVIGATION")
st.sidebar.markdown("---")

if st.session_state.injuries:
    dates_list = sorted(list(set([i.get('date', '') for i in st.session_state.injuries if i.get('date')])), reverse=True)
    
    if dates_list:
        selected_date = st.sidebar.selectbox(
            "📆 Select Date",
            options=dates_list,
            format_func=lambda x: f"📅 {x}"
        )
        
        filtered_by_date = [i for i in st.session_state.injuries if i.get('date') == selected_date]
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### 📊 Summary for {selected_date}")
        st.sidebar.markdown(f"**Total injuries:** {len(filtered_by_date)}")
        
        contact_count = sum(1 for i in filtered_by_date if i.get('injury_category') == 'Contact')
        non_contact_count = sum(1 for i in filtered_by_date if i.get('injury_category') == 'Non-Contact')
        st.sidebar.markdown(f"**🤕 Contact:** {contact_count}")
        st.sidebar.markdown(f"**🏃 Non-Contact:** {non_contact_count}")
    else:
        selected_date = None
        filtered_by_date = []
else:
    selected_date = None
    filtered_by_date = []

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗑️ REMOVE PLAYER")
st.sidebar.markdown("Select a player to remove all their records")

if st.session_state.injuries:
    all_players_for_remove = sorted(list(set([i.get('name', '') for i in st.session_state.injuries if i.get('name')])))
    if all_players_for_remove:
        player_to_remove = st.sidebar.selectbox("Select Player to Remove", all_players_for_remove, key="remove_player")
        
        if st.sidebar.button("🗑️ REMOVE PLAYER", type="secondary"):
            st.session_state.injuries = [i for i in st.session_state.injuries if i.get('name') != player_to_remove]
            save_data(st.session_state.injuries)
            st.sidebar.success(f"✅ {player_to_remove} removed successfully!")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Clinical Protocols")
st.sidebar.markdown("""
- **MEAT**: Movement, Exercise, Analgesia, Treatment
- **RICE**: Rest, Ice, Compression, Elevation
- **Contact**: Direct impact injuries
- **Non-Contact**: No external contact
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Risk Score Scale (0-10)")
st.sidebar.markdown("""
- **0-2**: Low Risk
- **3-5**: Medium Risk  
- **6-8**: High Risk
- **9-10**: Very High Risk
""")

# ──────────────────────────────────────────────────────────────
# ADD NEW INJURY
# ──────────────────────────────────────────────────────────────
st.header("➕ ADD NEW INJURY RECORD")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        player_name = st.text_input("👤 Player Name", placeholder="Enter player full name")
    
    with col2:
        injury_date = st.date_input("📅 Injury Date", datetime.today())
    
    with col3:
        custom_injury = st.text_input("🩺 Injury Diagnosis", placeholder="e.g., Hamstring Strain, ACL, Ankle Sprain...")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        injury_category = st.selectbox("🏥 Injury Category", ["Contact", "Non-Contact"])
    
    with col5:
        severity = st.select_slider("⚠️ Severity Level", options=["Mild", "Moderate", "Severe", "Critical"], value="Moderate")
    
    with col6:
        risk_score = st.slider("📊 Risk Score (0-10)", min_value=0, max_value=10, value=5, step=1)
        if risk_score <= 2:
            risk_label = "Low"
        elif risk_score <= 5:
            risk_label = "Medium"
        elif risk_score <= 8:
            risk_label = "High"
        else:
            risk_label = "Very High"
        st.caption(f"Risk Level: **{risk_label}**")
    
    col7, col8 = st.columns(2)
    
    with col7:
        meat = st.selectbox("🍖 MEAT Protocol", ["Yes", "No", "Partial", "Not Applicable"])
    
    with col8:
        rice = st.selectbox("🧊 RICE Protocol", ["Yes", "No", "Partial", "Not Applicable"])
    
    clinical_notes = st.text_area("📝 Clinical Notes", placeholder="Additional observations, treatment plan...", height=80)
    
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
                "risk_score": risk_score,
                "risk_label": risk_label,
                "clinical_notes": clinical_notes,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.injuries.append(new_injury)
            save_data(st.session_state.injuries)
            st.success(f"✅ Injury record for {player_name} saved! Risk Score: {risk_score}/10")
            st.rerun()
        elif not player_name:
            st.error("❌ Please enter player name!")
        elif not custom_injury:
            st.error("❌ Please enter injury diagnosis!")

st.markdown("---")

# ──────────────────────────────────────────────────────────────
# MAIN TABLE
# ──────────────────────────────────────────────────────────────
st.header("📋 INJURIES DATABASE")

if filtered_by_date and selected_date:
    # Create DataFrame WITHOUT renaming columns for internal use
    df_display = pd.DataFrame(filtered_by_date)
    
    # Display columns with original names
    display_cols = ['name', 'date', 'injury_type', 'injury_category', 'severity', 'meat', 'rice', 'risk_score', 'risk_label']
    available_cols = [col for col in display_cols if col in df_display.columns]
    
    if available_cols:
        # For display only, create a renamed version
        display_df = df_display[available_cols].copy()
        display_df.columns = ['Player Name', 'Date', 'Injury Diagnosis', 'Category', 'Severity', 'MEAT', 'RICE', 'Risk Score', 'Risk Level']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Remove specific injury section - USING ORIGINAL DATAFRAME
        st.markdown("#### 🗑️ Remove Specific Injury")
        
        # Create options from original dataframe with original column names
        injury_options = []
        injury_data_store = []  # Store the actual injury data for removal
        
        for idx, row in df_display.iterrows():
            option_text = f"{row['name']} - {row['injury_type']} - {row['date']}"
            injury_options.append(option_text)
            injury_data_store.append({
                'name': row['name'],
                'injury_type': row['injury_type'],
                'date': row['date']
            })
        
        if injury_options:
            injury_to_remove = st.selectbox("Select injury to remove", injury_options, key="remove_injury_sidebar")
            
            if st.button("🗑️ REMOVE THIS INJURY", type="secondary"):
                # Find the selected injury
                for idx, option in enumerate(injury_options):
                    if option == injury_to_remove:
                        injury_data = injury_data_store[idx]
                        # Remove from session state
                        st.session_state.injuries = [i for i in st.session_state.injuries if not (
                            i.get('name') == injury_data['name'] and 
                            i.get('injury_type') == injury_data['injury_type'] and 
                            i.get('date') == injury_data['date']
                        )]
                        save_data(st.session_state.injuries)
                        st.success("✅ Injury removed successfully!")
                        st.rerun()
else:
    st.info("👈 Select a date from the sidebar to view injury records")

st.markdown("---")

# ──────────────────────────────────────────────────────────────
# DASHBOARD TABS
# ──────────────────────────────────────────────────────────────

if st.session_state.injuries:
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Clinical Dashboard",
        "📈 Load Monitoring", 
        "🎯 Risk Profile",
        "📋 Injured Players Analysis"
    ])
    
    # TAB 1: Clinical Dashboard
    with tab1:
        st.header("Clinical Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Injuries", len(st.session_state.injuries))
        with col2:
            unique_players = len(set(i.get('name', '') for i in st.session_state.injuries))
            st.metric("👥 Players Affected", unique_players)
        with col3:
            critical_count = sum(1 for i in st.session_state.injuries if i.get('severity') == 'Critical')
            st.metric("🚨 Critical Cases", critical_count)
        with col4:
            high_risk_count = sum(1 for i in st.session_state.injuries if i.get('risk_score', 0) >= 6)
            st.metric("⚠️ High Risk (6-10)", high_risk_count)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Injuries by Category")
            category_counts = {}
            for i in st.session_state.injuries:
                cat = i.get('injury_category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            if category_counts:
                fig, ax = plt.subplots(figsize=(6, 4))
                colors_cat = ['#dc3545' if c == 'Contact' else '#28a745' for c in category_counts.keys()]
                ax.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', colors=colors_cat, startangle=90)
                ax.set_title('Contact vs Non-Contact Injuries')
                st.pyplot(fig)
                plt.close()
        
        with col2:
            st.subheader("Injuries by Severity")
            severity_counts = {}
            for i in st.session_state.injuries:
                sev = i.get('severity', 'Unknown')
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            if severity_counts:
                fig, ax = plt.subplots(figsize=(6, 4))
                colors_sev = {'Mild': '#28a745', 'Moderate': '#ffc107', 'Severe': '#fd7e14', 'Critical': '#dc3545'}
                bar_colors = [colors_sev.get(s, '#6c757d') for s in severity_counts.keys()]
                ax.bar(severity_counts.keys(), severity_counts.values(), color=bar_colors)
                ax.set_xlabel('Severity')
                ax.set_ylabel('Count')
                ax.set_title('Severity Distribution')
                st.pyplot(fig)
                plt.close()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Injury Diagnoses")
            injury_counts = {}
            for i in st.session_state.injuries:
                inj = i.get('injury_type', 'Unknown')
                injury_counts[inj] = injury_counts.get(inj, 0) + 1
            
            if injury_counts:
                top5 = dict(sorted(injury_counts.items(), key=lambda x: x[1], reverse=True)[:5])
                fig, ax = plt.subplots(figsize=(6, 5))
                ax.barh(list(top5.keys()), list(top5.values()), color='#dc3545')
                ax.set_xlabel('Number of Cases')
                ax.set_title('Most Common Injuries')
                ax.invert_yaxis()
                st.pyplot(fig)
                plt.close()
        
        with col2:
            st.subheader("Risk Score Distribution (0-10)")
            risk_scores = [i.get('risk_score', 0) for i in st.session_state.injuries]
            
            if risk_scores:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.hist(risk_scores, bins=10, range=(0, 10), color='#fd7e14', edgecolor='white', alpha=0.7)
                ax.set_xlabel('Risk Score')
                ax.set_ylabel('Number of Injuries')
                ax.set_title('Risk Score Distribution')
                ax.set_xticks(range(0, 11))
                st.pyplot(fig)
                plt.close()
    
    # TAB 2: Load Monitoring
    with tab2:
        st.header("Load Monitoring Analysis")
        
        st.subheader("📅 Injury Timeline")
        date_counts = {}
        for i in st.session_state.injuries:
            date = i.get('date', '')
            if date:
                date_counts[date] = date_counts.get(date, 0) + 1
        
        if date_counts:
            dates_sorted = sorted(date_counts.keys())
            counts_sorted = [date_counts[d] for d in dates_sorted]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates_sorted, counts_sorted, marker='o', linewidth=2, color='#dc3545', markersize=8)
            ax.set_xlabel('Date')
            ax.set_ylabel('Number of Injuries')
            ax.set_title('Injuries Over Time')
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
            plt.close()
        
        st.subheader("👥 Player Injury Load")
        player_counts = {}
        for i in st.session_state.injuries:
            player = i.get('name', '')
            if player:
                player_counts[player] = player_counts.get(player, 0) + 1
        
        if player_counts:
            top_players = dict(sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(list(top_players.keys()), list(top_players.values()), color='#fd7e14')
            ax.set_xlabel('Number of Injuries')
            ax.set_title('Players with Most Injuries')
            ax.invert_yaxis()
            st.pyplot(fig)
            plt.close()
        
        st.subheader("📊 Average Risk Score by Player (0-10)")
        player_avg_risk = {}
        for i in st.session_state.injuries:
            player = i.get('name', '')
            risk = i.get('risk_score', 0)
            if player:
                if player not in player_avg_risk:
                    player_avg_risk[player] = []
                player_avg_risk[player].append(risk)
        
        if player_avg_risk:
            avg_risks = {p: sum(scores)/len(scores) for p, scores in player_avg_risk.items()}
            top_risk_players = dict(sorted(avg_risks.items(), key=lambda x: x[1], reverse=True)[:10])
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors_risk = ['#dc3545' if v >= 6 else '#fd7e14' if v >= 3 else '#28a745' for v in top_risk_players.values()]
            ax.barh(list(top_risk_players.keys()), list(top_risk_players.values()), color=colors_risk)
            ax.set_xlabel('Average Risk Score (0-10)')
            ax.set_title('Average Risk Score by Player')
            ax.invert_yaxis()
            st.pyplot(fig)
            plt.close()
    
    # TAB 3: Risk Profile
    with tab3:
        st.header("Risk Profile Analysis")
        
        all_players = sorted(list(set(i.get('name', '') for i in st.session_state.injuries if i.get('name'))))
        if all_players:
            selected_player = st.selectbox("Select Player", all_players)
            
            if selected_player:
                player_injuries = [i for i in st.session_state.injuries if i.get('name') == selected_player]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Injuries", len(player_injuries))
                with col2:
                    avg_risk = sum(i.get('risk_score', 0) for i in player_injuries) / len(player_injuries) if player_injuries else 0
                    st.metric("Average Risk Score", f"{avg_risk:.1f}/10")
                with col3:
                    high_risk = sum(1 for i in player_injuries if i.get('risk_score', 0) >= 6)
                    st.metric("High Risk Injuries (6-10)", high_risk)
                
                st.subheader(f"Injury History - {selected_player}")
                df_player = pd.DataFrame(player_injuries)
                display_cols = ['date', 'injury_type', 'severity', 'risk_score', 'risk_label']
                available = [c for c in display_cols if c in df_player.columns]
                if available:
                    df_player_display = df_player[available].copy()
                    df_player_display.columns = ['Date', 'Injury', 'Severity', 'Risk Score', 'Risk Level']
                    st.dataframe(df_player_display, use_container_width=True, hide_index=True)
                
                if len(player_injuries) > 1:
                    st.subheader(f"Risk Score Trend - {selected_player}")
                    injuries_sorted = sorted(player_injuries, key=lambda x: x.get('date', ''))
                    dates = [i.get('date', '') for i in injuries_sorted]
                    risks = [i.get('risk_score', 0) for i in injuries_sorted]
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(dates, risks, marker='o', linewidth=2, color='#dc3545', markersize=8)
                    ax.axhline(y=6, color='orange', linestyle='--', label='High Risk Threshold (6)')
                    ax.axhline(y=3, color='green', linestyle='--', label='Medium Risk Threshold (3)')
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Risk Score (0-10)')
                    ax.set_title(f'Risk Score Evolution - {selected_player}')
                    ax.set_ylim(0, 10)
                    ax.legend()
                    ax.tick_params(axis='x', rotation=45)
                    st.pyplot(fig)
                    plt.close()
    
    # TAB 4: Injured Players Analysis
    with tab4:
        st.header("Injured Players Analysis")
        
        all_players = sorted(list(set(i.get('name', '') for i in st.session_state.injuries if i.get('name'))))
        
        players_summary = []
        for player in all_players:
            player_data = [i for i in st.session_state.injuries if i.get('name') == player]
            avg_risk = sum(i.get('risk_score', 0) for i in player_data) / len(player_data) if player_data else 0
            players_summary.append({
                'Player': player,
                'Total Injuries': len(player_data),
                'Contact': sum(1 for i in player_data if i.get('injury_category') == 'Contact'),
                'Non-Contact': sum(1 for i in player_data if i.get('injury_category') == 'Non-Contact'),
                'Critical/Severe': sum(1 for i in player_data if i.get('severity') in ['Severe', 'Critical']),
                'Avg Risk Score': f"{avg_risk:.1f}/10",
                'High Risk Injuries': sum(1 for i in player_data if i.get('risk_score', 0) >= 6)
            })
        
        if players_summary:
            df_summary = pd.DataFrame(players_summary)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
            
            col_csv, col_remove_all = st.columns(2)
            
            with col_csv:
                csv_summary = df_summary.to_csv(index=False)
                st.download_button(
                    label="📥 Export Summary to CSV",
                    data=csv_summary,
                    file_name=f"players_summary_{datetime.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col_remove_all:
                if st.button("🗑️ REMOVE ALL PLAYERS DATA", type="secondary"):
                    st.session_state.injuries = []
                    save_data([])
                    st.success("All players data removed!")
                    st.rerun()

# ──────────────────────────────────────────────────────────────
# EXPORT ALL DATA
# ──────────────────────────────────────────────────────────────
if st.session_state.injuries:
    st.markdown("---")
    
    export_df = pd.DataFrame(st.session_state.injuries)
    csv_data = export_df.to_csv(index=False)
    st.download_button(
        label="📥 Export All Injuries to CSV",
        data=csv_data,
        file_name=f"all_injuries_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("### ℹ️ Clinical Guidelines")
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
st.markdown("### 📊 Risk Score Scale (0-10)")
col_scale1, col_scale2, col_scale3, col_scale4 = st.columns(4)
with col_scale1:
    st.markdown("🟢 **0-2: Low Risk**")
with col_scale2:
    st.markdown("🟡 **3-5: Medium Risk**")
with col_scale3:
    st.markdown("🟠 **6-8: High Risk**")
with col_scale4:
    st.markdown("🔴 **9-10: Very High Risk**")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #1a472a; font-weight: 600;'>AL ITTIHAD SC LIBYA - Sports Medicine Department © 2024</p>", unsafe_allow_html=True)
