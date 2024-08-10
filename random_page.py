import streamlit as st
from search_recipe_page import *

def random_page():
    st.markdown("""
                <style>
                    .stButton > button {
                        font-size: 20px;
                        background-color: #FAECFE;
                        color: #B761B4;
                        text-align: center;
                        border: 8px outset #e3a9fa;
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
                    background-color: #FAECFE;
                    color: #B761B4;
                    text-align: center;
                    border: 10px outset #e3a9fa;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    margin: 0px 0px 50px 50px;
                    }}
            </>
            <p class=subheader>
                요리 비서가 추천 드리는 레시피는 <br> <strong>{st.session_state.random_recipe['요리명']}</strong> 입니다 !
            </p>""", unsafe_allow_html=True)
   # 결과 프레임 출력
    st.write(st.session_state.random_recipe.to_frame().T.set_index('요리명')) # 세로로 보여지는 시리즈를 프레임으로 바꾸고 전치

    # '다시 추천' 버튼 추가
    if st.button("다시 추천"):
        st.session_state.random_recipe = random_recipe() # 새로운 랜덤 레시피 로드
        st.session_state.hide_random_recipe_details = True # 상세안내 목록 숨기기
        st.experimental_rerun() # 페이지 새로고침
    
    random_cook(random_recipe=True, recipe_name=st.session_state.random_recipe['요리명'])