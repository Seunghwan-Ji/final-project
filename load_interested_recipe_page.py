import streamlit as st
from Cook import *
from search_recipe_page import *

def load_interested_recipe_page(recipe_name, call_from_history_menu=False):
    st.markdown("""
        <style>
            .stButton > button {
                font-size: 20px;
                background-color: #fdffeb;
                color: #727421;
                text-align: center;
                border: 8px outset #fdffb2;
                border-radius: 8px;
                margin: 5px 0px 0px 0px;
            }
        """, unsafe_allow_html=True)
    
    if st.button("뒤로 가기"):
        st.session_state.load_interested_recipe_page = False
        
        if st.session_state.searched_recipe_info: # 검색된 레시피 정보가 있는지 확인
            st.session_state.searched_recipe_info = None
        
        st.experimental_rerun()
    
    st.image("app_gui/random_recipe_icon.png", width=700)
    
    if not st.session_state.searched_recipe_info:
        status_placeholder = st.empty() # 빈 자리표시자 생성
        status_placeholder.text("로드 중입니다...")
        
        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.searched_recipe_info = recipe_info
        else:
            st.session_state.searched_recipe_info = None
            st.text(f"'{recipe_name}' 레시피의 시각적인 정보를 찾지 못했습니다.")
        
        # 로드되면 텍스트 제거
        status_placeholder.empty()

    # 레시피 로드하기
    if st.session_state.searched_recipe_info:
        search_result(recipe_name, call_from_history_menu)
