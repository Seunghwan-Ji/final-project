import streamlit as st
from search_recipe_page import *

def recommend_random_recipe_page():
    st.markdown("""
                <style>
                    .stButton > button {
                        font-size: 20px;
                        background-color: #fdffeb;
                        color: #727421;
                        text-align: center;
                        border: 8px outset #fdffb2;
                        border-radius: 8px;
                    }
                </style>
                """, unsafe_allow_html=True)
    
    st.image("app_gui/random_title.png", width=700)
    
    _, col1, _ = st.columns([3, 10, 1])

    with col1:
        st.image("app_gui/random_icon.png", width=400)

    subheader = st.markdown(f"""
            <style>
                .subheader {{
                    font-size: 20px;
                    background-color: #fdffeb;
                    color: #727421;
                    text-align: center;
                    border: 10px outset #fdffb2;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    margin: 0px 0px 50px 50px;
                    }}
            </style>
            <p class=subheader>
                요리 비서가 추천 드리는 레시피는 <br> <strong>{st.session_state.random_recipe['요리명']}</strong> 입니다 !
            </p>""", unsafe_allow_html=True)
    
    # 결과 프레임 출력
    st.write(st.session_state.random_recipe.to_frame().T.set_index('요리명')) # 세로로 보여지는 시리즈를 프레임으로 바꾸고 전치

    # '다시 추천' 버튼 추가
    if st.button("다시 추천"):
        st.session_state.random_recipe = random_recipe() # 새로운 랜덤 레시피 로드
        if st.session_state.searched_recipe_info:
            st.session_state.hide_searched_recipe_info = True
        
        st.experimental_rerun() # 페이지 새로고침
    
    recipe_name = st.session_state.random_recipe['요리명'] # 시리즈
    st.session_state.recipe_df_selected_number = st.session_state.random_recipe['레시피일련번호'] # 시리즈
    search_recipe(recipe_name=recipe_name, random_recipe=True)
