"""
Community Challenge Arena
Compete globally, earn rewards, and dominate the leaderboard 🏆
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render_community_challenge_arena_page():
    # Check if viewing a specific challenge
    if 'selected_challenge' in st.session_state and st.session_state.selected_challenge:
        render_challenge_detail_page(st.session_state.selected_challenge)
        return
    
    # Main Arena Page
    render_main_arena()


def render_main_arena():
    # Header
    st.markdown('<div style="text-align: center; margin-bottom: 20px;"><h2 style="background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; margin-bottom: 10px;">🏆 Community Challenge Arena ⚔️</h2><p style="color: #94a3b8; font-size: 0.95rem;">Compete globally, earn rewards, and dominate the leaderboard 🏆</p></div>', unsafe_allow_html=True)
    
    # Top buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        st.button("🏆 27 Active Challenges", use_container_width=True, type="secondary")
    with col3:
        st.button("🎯 Join Challenge", use_container_width=True, type="primary")
    
    # Your Stats Panel
    st.markdown('<div style="background: linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%); border: 2px solid rgba(167, 139, 250, 0.4); border-radius: 16px; padding: 20px; margin: 20px 0;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;"><div><div style="color: #a78bfa; font-weight: 700; font-size: 1.2rem;">👤 Your Stats</div><div style="color: #94a3b8; font-size: 0.85rem;">Ranked #642</div></div><div style="color: #06b6d4; font-size: 2.5rem; font-weight: 900;">8,450 XP</div></div></div>', unsafe_allow_html=True)
    
    # 5 Stat Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    stats = [
        ("🔥", "Streak", "8", "days"),
        ("🏆", "Wins", "12", "contest"),
        ("⚡", "Completed", "27", "challenges"),
        ("🌟", "Badges", "4", "starred"),
        ("🎯", "In Total", "50", "87 started")
    ]
    
    for col, (icon, title, value, subtitle) in zip([col1, col2, col3, col4, col5], stats):
        with col:
            st.markdown(f'<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 16px; text-align: center;"><div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px;">{icon} {title}</div><div style="color: #e2e8f0; font-size: 1.8rem; font-weight: 900;">{value}</div><div style="color: #64748b; font-size: 0.7rem;">{subtitle}</div></div>', unsafe_allow_html=True)
    
    # Active Challenges Section
    st.markdown('<div style="margin-top: 40px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><div><h3 style="color: #f59e0b; margin: 0;">⚡ Active Challenges</h3><p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Join now and compete for epic prizes! 🔥</p></div></div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("View All Challenges", use_container_width=True, type="secondary"):
            st.info("Viewing all challenges...")
    
    # Challenge Cards (2x2 grid)
    col1, col2 = st.columns(2)
    
    with col1:
        render_challenge_card(
            "Weekly Warrior",
            "🔥",
            "Complete 5 sessions this week",
            "linear-gradient(135deg, #f97316 0%, #fbbf24 100%)",
            "Medium",
            "#fbbf24",
            "3/5",
            "Gold Badge",
            "+250 XP • Gold Badge",
            "2d 14h",
            "#f97316",
            "weekly_warrior"
        )
        
        render_challenge_card(
            "Zen Champion",
            "🧘",
            "Complete 10 breathing sessions",
            "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
            "Beginner",
            "#10b981",
            "7/10",
            "Diamond Badge",
            "+1000 XP • Diamond Badge",
            "7d 2h",
            "#06b6d4",
            "zen_champion"
        )
    
    with col2:
        render_challenge_card(
            "Recovery Master",
            "🌙",
            "Achieve HRV >70 for 3 days",
            "linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)",
            "Hard",
            "#ef4444",
            "1/3",
            "Platinum Badge",
            "+500 XP • Platinum Badge",
            "5d 8h",
            "#a78bfa",
            "recovery_master"
        )
        
        render_challenge_card(
            "Morning Routine",
            "☀️",
            "Log sessions before 9 AM for 7 days",
            "linear-gradient(135deg, #f97316 0%, #ef4444 100%)",
            "Easy",
            "#10b981",
            "4/7",
            "Silver Badge",
            "+150 XP • Silver Badge",
            "3d 4h",
            "#f97316",
            "morning_routine"
        )
    
    # Global Leaderboard
    st.markdown('<div style="margin-top: 40px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><div><h3 style="color: #f59e0b; margin: 0;">🏆 Global Leaderboard</h3><p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Top performers this week</p></div><div style="display: flex; gap: 10px;"><span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">Live Updates</span></div></div></div>', unsafe_allow_html=True)
    
    # Leaderboard entries
    leaderboard = [
        (1, "Sarah M.", "Ireland", "GOLD", "89.2", "12,450 XP", "🥇"),
        (2, "James L.", "USA", "GOLD", "87.3", "11,890 XP", "🥈"),
        (3, "Emma K.", "Netherlands", "GOLD", "86.5", "11,420 XP", "🥉"),
        (4, "Liam D.", "Ireland", "", "85.8", "11,200 XP", ""),
        (5, "Sophie D.", "France", "", "84.7", "10,840 XP", ""),
        (6, "Alex W.", "Germany", "", "83.9", "10,340 XP", ""),
        (7, "Mia R.", "Australia", "", "82.4", "9,890 XP", ""),
        (8, "Noah P.", "Ireland", "", "81.6", "9,450 XP", ""),
        (9, "Olivia C.", "Spain", "", "80.2", "9,100 XP", ""),
        (10, "YOU", "India", "", "78.2", "8,450 XP", "")
    ]
    
    for rank, name, location, badge, sri, xp, trophy in leaderboard:
        is_user = name == "YOU"
        bg_color = "rgba(6, 182, 212, 0.15)" if is_user else "rgba(30, 41, 59, 0.8)"
        border_color = "rgba(6, 182, 212, 0.4)" if is_user else "rgba(148, 163, 184, 0.2)"
        
        badge_html = f'<span style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; padding: 2px 8px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; margin-left: 8px;">{badge}</span>' if badge else ""
        
        st.markdown(f'<div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 12px; padding: 16px; margin: 10px 0; display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 15px;"><div style="color: #94a3b8; font-weight: 700; font-size: 1.2rem; min-width: 30px;">{rank}</div><div style="display: flex; align-items: center; gap: 10px;"><div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">{name[0]}</div><div><div style="color: #e2e8f0; font-weight: 700;">{name} {badge_html}</div><div style="color: #94a3b8; font-size: 0.75rem;">{location}</div></div></div></div><div style="display: flex; align-items: center; gap: 20px;"><div style="text-align: right;"><div style="color: #10b981; font-weight: 700;">SRI {sri}</div><div style="color: #94a3b8; font-size: 0.75rem;">{xp}</div></div><div style="font-size: 1.5rem;">{trophy}</div></div></div>', unsafe_allow_html=True)
    
    # Live Activity Feed
    st.markdown('<div style="margin-top: 40px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h3 style="color: #10b981; margin: 0;">📊 Live Activity Feed</h3><span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">LIVE</span></div></div>', unsafe_allow_html=True)
    
    activities = [
        ("Sarah M. just completed Recovery Master 🌙", "2m ago"),
        ("Liam D. reached 85-day streak 🔥", "15m ago"),
        ("Emma K. achieved 4% of 85 🎯", "1hr ago"),
        ("Alex W. joined Weekly Warrior 🔥", "3m ago")
    ]
    
    for activity, time in activities:
        st.markdown(f'<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 8px; padding: 12px; margin: 8px 0; display: flex; justify-content: space-between;"><span style="color: #cbd5e1; font-size: 0.9rem;">{activity}</span><span style="color: #64748b; font-size: 0.75rem;">{time}</span></div>', unsafe_allow_html=True)
    
    # Weekly Performance Chart
    st.markdown('<h3 style="color: #06b6d4; margin-top: 40px;">📈 Your Weekly Performance</h3>', unsafe_allow_html=True)
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sri_scores = [45, 52, 58, 54, 62, 68, 65]
    xp_earned = [120, 145, 180, 160, 210, 250, 220]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=sri_scores, mode='lines+markers', name='SRI Score', line=dict(color='#06b6d4', width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=days, y=xp_earned, mode='lines+markers', name='XP Earned', line=dict(color='#a78bfa', width=3), marker=dict(size=8), yaxis='y2'))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        height=350,
        xaxis=dict(title="", gridcolor='rgba(148, 163, 184, 0.1)'),
        yaxis=dict(title="SRI Score", gridcolor='rgba(148, 163, 184, 0.1)', title_font=dict(color='#06b6d4')),
        yaxis2=dict(title="XP Earned", overlaying='y', side='right', gridcolor='rgba(148, 163, 184, 0.1)', title_font=dict(color='#a78bfa')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(color='#cbd5e1'),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Total Prize Pool
    st.markdown('<div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.05) 100%); border: 2px solid rgba(245, 158, 11, 0.4); border-radius: 16px; padding: 24px; margin: 30px 0; text-align: center;"><div style="color: #f59e0b; font-weight: 700; font-size: 1rem; margin-bottom: 8px;">💰 Total Prize Pool</div><div style="color: #f59e0b; font-size: 3rem; font-weight: 900;">€1,850</div><div style="color: #94a3b8; font-size: 0.9rem;">Real rewards this month!</div></div>', unsafe_allow_html=True)
    
    # Bottom Stats Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 20px; text-align: center;"><div style="color: #3b82f6; font-size: 0.85rem; margin-bottom: 8px;">👥 Active Users</div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">17,377</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; text-align: center;"><div style="color: #10b981; font-size: 0.85rem; margin-bottom: 8px;">📈 Avg SRI</div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">70.2</div><div style="color: #10b981; font-size: 0.75rem;">+5.3%</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(167, 139, 250, 0.3); border-radius: 12px; padding: 20px; text-align: center;"><div style="color: #a78bfa; font-size: 0.85rem; margin-bottom: 8px;">⏱️ Avg Recovery Time</div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">7m</div></div>', unsafe_allow_html=True)
    
    # Regional Competition Chart
    st.markdown('<h3 style="color: #10b981; margin-top: 40px;">🌍 Regional Competition</h3>', unsafe_allow_html=True)
    
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Oceania']
    values = [75, 82, 95, 78, 92]
    colors_regional = ['#f97316', '#f97316', '#10b981', '#f97316', '#10b981']
    
    fig2 = go.Figure(data=[go.Bar(x=regions, y=values, marker=dict(color=colors_regional))])
    
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        height=300,
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)'),
        font=dict(color='#cbd5e1'),
        showlegend=False,
        margin=dict(l=50, r=50, t=20, b=50)
    )
    
    st.plotly_chart(fig2, use_container_width=True)


def render_challenge_card(title, icon, subtitle, gradient, difficulty, diff_color, progress, badge, reward, countdown, button_color, challenge_id):
    """Render a single challenge card with vibrant gradient"""
    
    # Build HTML for challenge card
    html = f'<div style="background: {gradient}; border-radius: 16px; padding: 20px; margin: 16px 0; position: relative; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">'
    
    # Header with icon and badges
    html += f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">'
    html += f'<div style="font-size: 2rem;">{icon}</div>'
    html += f'<div style="display: flex; gap: 8px;">'
    html += f'<span style="background: rgba(236, 72, 153, 0.9); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;">In Progress</span>'
    html += f'</div></div>'
    
    # Title and subtitle
    html += f'<div style="color: white; font-weight: 900; font-size: 1.4rem; margin-bottom: 6px;">{title}</div>'
    html += f'<div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin-bottom: 16px;">{subtitle}</div>'
    
    # Difficulty badge
    html += f'<div style="margin-bottom: 12px;"><span style="background: rgba(255,255,255,0.2); color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700;">Difficulty: </span><span style="background: {diff_color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; margin-left: 6px;">{difficulty}</span></div>'
    
    # Progress and reward
    html += f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">'
    html += f'<div><div style="color: rgba(255,255,255,0.8); font-size: 0.75rem;">Progress</div><div style="color: white; font-weight: 700; font-size: 1.1rem;">{progress} • {badge}</div></div>'
    html += f'<div style="text-align: right;"><div style="color: rgba(255,255,255,0.8); font-size: 0.75rem;">Reward</div><div style="color: white; font-weight: 700; font-size: 0.9rem;">{reward}</div></div>'
    html += f'</div>'
    
    # Countdown
    html += f'<div style="display: flex; justify-content: space-between; align-items: center;">'
    html += f'<div style="color: white; font-size: 0.85rem;">⏱️ Ends in <strong>{countdown}</strong></div>'
    html += f'</div>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Join Challenge button
    if st.button(f"⚡ Join Challenge", key=f"join_{challenge_id}", use_container_width=True, type="primary"):
        st.session_state.selected_challenge = challenge_id
        st.rerun()


def render_challenge_detail_page(challenge_id):
    """Render individual challenge detail page"""
    
    # Challenge data
    challenges = {
        "weekly_warrior": {
            "title": "Weekly Warrior",
            "icon": "🔥",
            "description": "Complete 5 biofeedback sessions this week to earn the Gold Badge and boost your resilience score!",
            "gradient": "linear-gradient(135deg, #f97316 0%, #fbbf24 100%)",
            "difficulty": "Medium",
            "reward": "+250 XP • Gold Badge",
            "progress": 3,
            "total": 5,
            "participants": 1247
        },
        "recovery_master": {
            "title": "Recovery Master",
            "icon": "🌙",
            "description": "Achieve HRV >70 for 3 consecutive days to master your recovery and earn the Platinum Badge!",
            "gradient": "linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)",
            "difficulty": "Hard",
            "reward": "+500 XP • Platinum Badge",
            "progress": 1,
            "total": 3,
            "participants": 892
        },
        "zen_champion": {
            "title": "Zen Champion",
            "icon": "🧘",
            "description": "Complete 10 breathing sessions to achieve zen mastery and earn the Diamond Badge!",
            "gradient": "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
            "difficulty": "Beginner",
            "reward": "+1000 XP • Diamond Badge",
            "progress": 7,
            "total": 10,
            "participants": 2156
        },
        "morning_routine": {
            "title": "Morning Routine",
            "icon": "☀️",
            "description": "Log biofeedback sessions before 9 AM for 7 days to establish a powerful morning routine!",
            "gradient": "linear-gradient(135deg, #f97316 0%, #ef4444 100%)",
            "difficulty": "Easy",
            "reward": "+150 XP • Silver Badge",
            "progress": 4,
            "total": 7,
            "participants": 1834
        }
    }
    
    challenge = challenges.get(challenge_id, challenges["weekly_warrior"])
    
    # Back button
    if st.button("← Back to Arena", type="secondary"):
        st.session_state.selected_challenge = None
        st.rerun()
    
    # Challenge Header
    st.markdown(f'<div style="background: {challenge["gradient"]}; border-radius: 16px; padding: 40px; margin: 20px 0; text-align: center;"><div style="font-size: 4rem; margin-bottom: 16px;">{challenge["icon"]}</div><h1 style="color: white; font-size: 2.5rem; margin-bottom: 12px;">{challenge["title"]}</h1><p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; max-width: 600px; margin: 0 auto;">{challenge["description"]}</p><div style="margin-top: 20px;"><span style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 12px; font-size: 0.9rem; font-weight: 700; margin-right: 10px;">Difficulty: {challenge["difficulty"]}</span><span style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 12px; font-size: 0.9rem; font-weight: 700;">Reward: {challenge["reward"]}</span></div></div>', unsafe_allow_html=True)
    
    # Your Progress
    progress_percent = (challenge["progress"] / challenge["total"]) * 100
    st.markdown(f'<h3 style="color: #06b6d4; margin-top: 30px;">📊 Your Progress</h3><div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 20px; margin: 16px 0;"><div style="display: flex; justify-content: space-between; margin-bottom: 12px;"><span style="color: #cbd5e1; font-weight: 700;">{challenge["progress"]} / {challenge["total"]} completed</span><span style="color: #10b981; font-weight: 700;">{progress_percent:.0f}%</span></div><div style="background: rgba(148, 163, 184, 0.2); border-radius: 8px; height: 12px; overflow: hidden;"><div style="background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%); height: 100%; width: {progress_percent}%; transition: width 0.3s;"></div></div></div>', unsafe_allow_html=True)
    
    # Participants
    st.markdown(f'<h3 style="color: #a78bfa; margin-top: 30px;">👥 Participants</h3><div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 20px; margin: 16px 0; text-align: center;"><div style="color: #e2e8f0; font-size: 2.5rem; font-weight: 900;">{challenge["participants"]}</div><div style="color: #94a3b8; font-size: 0.9rem;">Active participants</div></div>', unsafe_allow_html=True)
    
    # Join/Leave button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Leave Challenge", use_container_width=True, type="secondary"):
            st.success("Left challenge successfully!")
