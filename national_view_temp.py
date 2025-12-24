def render_national_view_simple():
    """Render National View with city-level statistics - Simple version"""
    
    st.markdown("### 🌍 National Resilience - All Cities (Ireland)")
    
    # National Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average RQ Score", "66.3")
    
    with col2:
        st.metric("Active Users", "12,847")
    
    with col3:
        st.metric("Participating Cities", "6")
    
    st.markdown("---")
    
    # Cities
    st.markdown("### Cities")
    
    cities = [
        ("Dublin", "1.4M", 64.2),
        ("Cork", "210K", 68.9),
        ("Galway", "85K", 70.1),
        ("Limerick", "95K", 62.5),
        ("Waterford", "54K", 67.3),
        ("Other", "Various", 65.8)
    ]
    
    for name, pop, rq in cities:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{name}** ({pop})")
        with col2:
            st.write(f"**{rq}**")
