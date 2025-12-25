"""
Cognitive Resilience Testing
Track how stress affects cognitive performance - reaction time, attention, and decision-making
"""
import streamlit as st
import time
import random

def render_cognitive_testing_page():
    # Check if a test is active
    if 'active_test' in st.session_state and st.session_state.active_test:
        if st.session_state.active_test == 'stroop':
            render_stroop_test()
        elif st.session_state.active_test == 'reaction':
            render_reaction_test()
        elif st.session_state.active_test == 'memory':
            render_memory_test()
        return
    
    # Main view
    render_main_view()


def render_main_view():
    # Header
    st.markdown('<div style="text-align: center; margin-bottom: 30px;"><h2 style="color: #ec4899; font-size: 2.5rem; margin-bottom: 10px;">Cognitive Resilience Testing</h2><p style="color: #94a3b8; font-size: 0.95rem;">Track how stress affects cognitive performance - reaction time, attention, and decision-making</p></div>', unsafe_allow_html=True)
    
    # Three test cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%); border-radius: 16px; padding: 30px; text-align: center; margin: 10px 0;"><div style="font-size: 3rem; margin-bottom: 16px;">🧠</div><h3 style="color: white; margin-bottom: 12px;">Stroop Test</h3><div style="background: rgba(255,255,255,0.2); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 16px;">Medium</div><p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; line-height: 1.6; margin-bottom: 20px;">Color-word interference test measuring selective attention and processing speed</p><div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 20px;">⏱️ 2 min</div></div>', unsafe_allow_html=True)
        if st.button("▶ Start Test", key="start_stroop", use_container_width=True, type="primary"):
            start_test('stroop')
    
    with col2:
        st.markdown('<div style="background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%); border-radius: 16px; padding: 30px; text-align: center; margin: 10px 0;"><div style="font-size: 3rem; margin-bottom: 16px;">🎯</div><h3 style="color: white; margin-bottom: 12px;">Reaction Timer</h3><div style="background: rgba(255,255,255,0.2); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 16px;">Easy</div><p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; line-height: 1.6; margin-bottom: 20px;">Simple reaction time test - measures alertness and response latency</p><div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 20px;">⏱️ 1 min</div></div>', unsafe_allow_html=True)
        if st.button("▶ Start Test", key="start_reaction", use_container_width=True, type="primary"):
            start_test('reaction')
    
    with col3:
        st.markdown('<div style="background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%); border-radius: 16px; padding: 30px; text-align: center; margin: 10px 0;"><div style="font-size: 3rem; margin-bottom: 16px;">🔲</div><h3 style="color: white; margin-bottom: 12px;">Memory Matrix</h3><div style="background: rgba(255,255,255,0.2); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 16px;">Hard</div><p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; line-height: 1.6; margin-bottom: 20px;">Visual working memory test - track pattern recall under stress</p><div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 20px;">⏱️ 3 min</div></div>', unsafe_allow_html=True)
        if st.button("▶ Start Test", key="start_memory", use_container_width=True, type="primary"):
            start_test('memory')
    
    # Why Cognitive Testing section
    st.markdown('<div style="margin-top: 50px;"><h3 style="color: #a78bfa; margin-bottom: 20px;">Why Cognitive Testing?</h3></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background: linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%); border: 2px solid rgba(167, 139, 250, 0.3); border-radius: 16px; padding: 30px;"><h4 style="color: #cbd5e1; margin-bottom: 16px;">Stress → Brain Connection</h4><p style="color: #94a3b8; line-height: 1.8; margin-bottom: 20px;">Elevated cortisol and sympathetic activation directly impair prefrontal cortex function, affecting:</p><ul style="color: #cbd5e1; line-height: 2;"><li>Working memory capacity</li><li>Reaction time and alertness</li><li>Selective attention and impulse control</li><li>Decision-making quality</li></ul><p style="color: #94a3b8; line-height: 1.8; margin-top: 20px;">By tracking cognitive performance alongside physiological markers (HRV, GSR), you can see direct evidence of how stress affects brain function – not just how you feel, but how you think.</p></div>', unsafe_allow_html=True)


def start_test(test_name):
    """Initialize test"""
    st.session_state.active_test = test_name
    st.session_state.test_round = 1
    st.session_state.test_score = 0
    st.session_state.test_times = []
    st.session_state.test_complete = False
    
    if test_name == 'stroop':
        st.session_state.total_rounds = 10
        generate_stroop_question()
    elif test_name == 'reaction':
        st.session_state.total_rounds = 5
        st.session_state.waiting = True
        st.session_state.wait_start = time.time()
        st.session_state.wait_duration = random.uniform(2, 5)
    elif test_name == 'memory':
        st.session_state.total_rounds = 5
        st.session_state.memorize_phase = True
        st.session_state.pattern = random.sample(range(16), k=random.randint(5, 8))
        st.session_state.user_clicks = []
        st.session_state.memorize_start = time.time()
    
    st.rerun()


def render_stroop_test():
    """Render Stroop Color-Word Test"""
    if st.session_state.test_complete:
        render_stroop_results()
        return
    
    # Header
    st.markdown(f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h3 style="color: #ec4899;">Stroop Color-Word Test</h3><span style="color: #94a3b8;">Round {st.session_state.test_round}/{st.session_state.total_rounds}</span></div>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.test_round / st.session_state.total_rounds
    st.markdown(f'<div style="background: rgba(148, 163, 184, 0.2); border-radius: 8px; height: 8px; margin-bottom: 30px;"><div style="background: linear-gradient(90deg, #ec4899 0%, #a78bfa 100%); height: 100%; width: {progress*100}%; border-radius: 8px;"></div></div>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown('<p style="color: #cbd5e1; text-align: center; font-size: 1.1rem; margin-bottom: 40px;">Select the COLOR of the text (not what it says)</p>', unsafe_allow_html=True)
    
    # Display word
    word = st.session_state.stroop_word
    color = st.session_state.stroop_color
    color_name = st.session_state.stroop_color_name
    
    st.markdown(f'<div style="text-align: center; margin: 60px 0;"><h1 style="color: {color}; font-size: 5rem; font-weight: 900;">{word}</h1></div>', unsafe_allow_html=True)
    
    # Answer buttons
    col1, col2 = st.columns(2)
    
    colors = [
        ('RED', '#ef4444'),
        ('BLUE', '#3b82f6'),
        ('GREEN', '#10b981'),
        ('YELLOW', '#fbbf24')
    ]
    
    for i, (color_text, color_hex) in enumerate(colors):
        col = col1 if i < 2 else col2
        with col:
            if st.button(color_text, key=f"stroop_{color_text}", use_container_width=True):
                check_stroop_answer(color_text)
    
    # Score and Cancel
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<p style="color: #94a3b8;">Score: {st.session_state.test_score}/{st.session_state.test_round-1}</p>', unsafe_allow_html=True)
    with col2:
        if st.button("Cancel", use_container_width=True, type="secondary"):
            cancel_test()


def generate_stroop_question():
    """Generate a new Stroop question"""
    words = ['RED', 'BLUE', 'GREEN', 'YELLOW']
    colors = {
        'RED': '#ef4444',
        'BLUE': '#3b82f6',
        'GREEN': '#10b981',
        'YELLOW': '#fbbf24'
    }
    
    # Pick word and color (ensure they don't match for interference)
    word = random.choice(words)
    color_name = random.choice([c for c in words if c != word])
    color = colors[color_name]
    
    st.session_state.stroop_word = word
    st.session_state.stroop_color = color
    st.session_state.stroop_color_name = color_name
    st.session_state.stroop_start_time = time.time()


def check_stroop_answer(answer):
    """Check if answer is correct"""
    reaction_time = time.time() - st.session_state.stroop_start_time
    st.session_state.test_times.append(reaction_time)
    
    if answer == st.session_state.stroop_color_name:
        st.session_state.test_score += 1
    
    if st.session_state.test_round >= st.session_state.total_rounds:
        st.session_state.test_complete = True
    else:
        st.session_state.test_round += 1
        generate_stroop_question()
    
    st.rerun()


def render_stroop_results():
    """Show Stroop test results"""
    st.markdown('<h2 style="color: #ec4899; text-align: center; margin-bottom: 30px;">Test Complete!</h2>', unsafe_allow_html=True)
    
    accuracy = (st.session_state.test_score / st.session_state.total_rounds) * 100
    avg_time = sum(st.session_state.test_times) / len(st.session_state.test_times)
    
    st.markdown(f'<div style="text-align: center; margin: 40px 0;"><div style="color: #94a3b8; font-size: 1rem; margin-bottom: 10px;">Your Score</div><div style="color: #10b981; font-size: 4rem; font-weight: 900;">{st.session_state.test_score}/{st.session_state.total_rounds}</div><div style="color: #cbd5e1; font-size: 1.2rem; margin-top: 10px;">{accuracy:.0f}% Accuracy</div><div style="color: #94a3b8; font-size: 1rem; margin-top: 20px;">Average Response Time: {avg_time:.2f}s</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again", use_container_width=True, type="primary"):
            start_test('stroop')
    with col2:
        if st.button("Back to Tests", use_container_width=True, type="secondary"):
            cancel_test()


def render_reaction_test():
    """Render Reaction Time Test"""
    if st.session_state.test_complete:
        render_reaction_results()
        return
    
    # Header
    st.markdown(f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h3 style="color: #ec4899;">Reaction Time Test</h3><span style="color: #94a3b8;">Round {st.session_state.test_round}/{st.session_state.total_rounds}</span></div>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.test_round / st.session_state.total_rounds
    st.markdown(f'<div style="background: rgba(148, 163, 184, 0.2); border-radius: 8px; height: 8px; margin-bottom: 30px;"><div style="background: linear-gradient(90deg, #ec4899 0%, #a78bfa 100%); height: 100%; width: {progress*100}%; border-radius: 8px;"></div></div>', unsafe_allow_html=True)
    
    # Check if it's time to show green
    if st.session_state.waiting:
        elapsed = time.time() - st.session_state.wait_start
        if elapsed >= st.session_state.wait_duration:
            st.session_state.waiting = False
            st.session_state.go_time = time.time()
            st.rerun()
        
        # Show red waiting screen
        st.markdown('<div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); border: 3px solid #ef4444; border-radius: 16px; padding: 100px; text-align: center; margin: 40px 0;"><div style="font-size: 4rem; margin-bottom: 20px;">⏱️</div><h2 style="color: #fca5a5; font-size: 2rem;">Wait for green...</h2></div>', unsafe_allow_html=True)
        
        if st.button("Cancel", use_container_width=True, type="secondary"):
            cancel_test()
        
        time.sleep(0.1)
        st.rerun()
    else:
        # Show green go screen
        st.markdown('<div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); border: 3px solid #10b981; border-radius: 16px; padding: 100px; text-align: center; margin: 40px 0;"><h1 style="color: #6ee7b7; font-size: 3rem; font-weight: 900;">CLICK NOW!</h1></div>', unsafe_allow_html=True)
        
        if st.button("CLICK!", use_container_width=True, type="primary"):
            reaction_time = (time.time() - st.session_state.go_time) * 1000  # Convert to ms
            st.session_state.test_times.append(reaction_time)
            
            if st.session_state.test_round >= st.session_state.total_rounds:
                st.session_state.test_complete = True
            else:
                st.session_state.test_round += 1
                st.session_state.waiting = True
                st.session_state.wait_start = time.time()
                st.session_state.wait_duration = random.uniform(2, 5)
            
            st.rerun()


def render_reaction_results():
    """Show Reaction test results"""
    st.markdown('<h2 style="color: #ec4899; text-align: center; margin-bottom: 30px;">Test Complete!</h2>', unsafe_allow_html=True)
    
    avg_time = sum(st.session_state.test_times) / len(st.session_state.test_times)
    
    rating = "Excellent" if avg_time < 250 else "Good" if avg_time < 350 else "Fair"
    rating_color = "#10b981" if avg_time < 250 else "#f59e0b" if avg_time < 350 else "#ef4444"
    
    st.markdown(f'<div style="text-align: center; margin: 40px 0;"><div style="color: #94a3b8; font-size: 1rem; margin-bottom: 10px;">Average Reaction Time</div><div style="color: #06b6d4; font-size: 4rem; font-weight: 900;">{avg_time:.0f}ms</div><div style="color: {rating_color}; font-size: 1.2rem; margin-top: 10px;">{rating}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: #cbd5e1; margin-top: 30px;">Individual Times:</h4>', unsafe_allow_html=True)
    for i, t in enumerate(st.session_state.test_times, 1):
        st.markdown(f'<p style="color: #94a3b8;">Round {i}: {t:.0f}ms</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again", use_container_width=True, type="primary"):
            start_test('reaction')
    with col2:
        if st.button("Back to Tests", use_container_width=True, type="secondary"):
            cancel_test()


def render_memory_test():
    """Render Visual Memory Matrix Test"""
    if st.session_state.test_complete:
        render_memory_results()
        return
    
    # Header
    st.markdown(f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h3 style="color: #ec4899;">Visual Memory Matrix</h3><span style="color: #94a3b8;">Memorize: 3s</span></div>', unsafe_allow_html=True)
    
    if st.session_state.memorize_phase:
        # Show pattern for 3 seconds
        elapsed = time.time() - st.session_state.memorize_start
        if elapsed >= 3:
            st.session_state.memorize_phase = False
            st.rerun()
        
        st.markdown('<p style="color: #cbd5e1; text-align: center; margin-bottom: 30px;">Remember the pattern...</p>', unsafe_allow_html=True)
        
        # Display 4x4 grid with pattern
        grid_html = '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; max-width: 400px; margin: 40px auto;">'
        for i in range(16):
            if i in st.session_state.pattern:
                grid_html += '<div style="background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%); aspect-ratio: 1; border-radius: 12px;"></div>'
            else:
                grid_html += '<div style="background: rgba(71, 85, 105, 0.5); aspect-ratio: 1; border-radius: 12px;"></div>'
        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        
        time.sleep(0.1)
        st.rerun()
    else:
        # Recall phase
        st.markdown('<p style="color: #cbd5e1; text-align: center; margin-bottom: 30px;">Click the purple squares...</p>', unsafe_allow_html=True)
        
        # Display clickable grid
        cols = st.columns(4)
        for i in range(16):
            col = cols[i % 4]
            with col:
                is_clicked = i in st.session_state.user_clicks
                bg_color = "linear-gradient(135deg, #a78bfa 0%, #ec4899 100%)" if is_clicked else "rgba(71, 85, 105, 0.5)"
                
                if st.button("", key=f"mem_{i}", use_container_width=True):
                    if i in st.session_state.user_clicks:
                        st.session_state.user_clicks.remove(i)
                    else:
                        st.session_state.user_clicks.append(i)
                    st.rerun()
        
        # Submit and Cancel
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit", use_container_width=True, type="primary"):
                # Calculate score
                correct = len(set(st.session_state.user_clicks) & set(st.session_state.pattern))
                total = len(st.session_state.pattern)
                st.session_state.test_score = correct
                st.session_state.test_total = total
                st.session_state.test_complete = True
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True, type="secondary"):
                cancel_test()


def render_memory_results():
    """Show Memory test results"""
    st.markdown('<h2 style="color: #ec4899; text-align: center; margin-bottom: 30px;">Test Complete!</h2>', unsafe_allow_html=True)
    
    accuracy = (st.session_state.test_score / st.session_state.test_total) * 100
    
    rating = "Excellent" if accuracy >= 90 else "Good" if accuracy >= 70 else "Fair"
    rating_color = "#10b981" if accuracy >= 90 else "#f59e0b" if accuracy >= 70 else "#ef4444"
    
    st.markdown(f'<div style="text-align: center; margin: 40px 0;"><div style="color: #94a3b8; font-size: 1rem; margin-bottom: 10px;">Your Score</div><div style="color: #10b981; font-size: 4rem; font-weight: 900;">{st.session_state.test_score}/{st.session_state.test_total}</div><div style="color: #cbd5e1; font-size: 1.2rem; margin-top: 10px;">{accuracy:.1f}% Accuracy</div><div style="color: {rating_color}; font-size: 1rem; margin-top: 10px;">{rating}</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again", use_container_width=True, type="primary"):
            start_test('memory')
    with col2:
        if st.button("Back to Tests", use_container_width=True, type="secondary"):
            cancel_test()


def cancel_test():
    """Cancel current test and return to main view"""
    st.session_state.active_test = None
    st.session_state.test_complete = False
    st.rerun()
