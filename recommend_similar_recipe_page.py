import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from search_recipe_page import *

def display_recipes_with_checkboxes(similar_recipe_df):
    # button CSS
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #fdffeb;
            color: #727421;
            font-size: 25px;
            font-weight: bold;
            border: 7px outset #fdffb2;
        }
        
        .stButton>button:hover {
            background-color: #ffffD3;
            border: 7px outset #FFFF41;
        }
        
    </style>
    """, unsafe_allow_html=True)
    
    back_button = st.empty()

    st.markdown(f"""
    <style>
        .header {{
            font-size: 25px;
            background-color: #fdffeb;
            color: #727421;
            text-align: center;
            border: 5px dotted #fdffb2;
            text-shadow: 3px  0px 0 #fff;
            border-radius: 8px;
            width: auto;
            }}
    </style>
    <p class=header>
        아래의 레시피 중 하나를 체크해주세요.
    </p>""", unsafe_allow_html=True)
    
    if not similar_recipe_df.empty: # 빈 df인지 확인
        gb = GridOptionsBuilder.from_dataframe(similar_recipe_df)
        gb.configure_selection('single', use_checkbox=True)
        grid_options = gb.build()

        grid_response = AgGrid(
            similar_recipe_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            height=400,
            width='100%',
            theme='alpine',
        )

        selected_row = grid_response['selected_rows']
        
        if selected_row is not None:
            recipe_number = selected_row['레시피일련번호'].iloc[0]
            recipe_name = selected_row['요리명'].iloc[0]
            if (st.session_state.recipe_df_selected_number is None) or (
                st.session_state.recipe_df_selected_number != recipe_number):
                st.session_state.recipe_df_selected_number = recipe_number
                st.session_state.recipe_df_selected_name = recipe_name

                if st.session_state.searched_recipe_info: # 검색된 레시피 정보가 있는지 확인
                    st.session_state.hide_searched_recipe_info = True
    else:
        st.write("비슷한 레시피를 찾지 못했습니다.")
    
    if st.session_state.recipe_df_selected_number is None:
        if back_button.button("뒤로 가기"):
            st.session_state.recommend_similar_recipe_page = False
            st.experimental_rerun()

def recommend_similar_recipe_page(recipe_number):
    if st.session_state.similar_recipe_df is None:
        st.session_state.similar_recipe_df = search_similar_recipe(recipe_number) # 유사도 계산으로 추출된 df 반환
    
    if st.session_state.similar_recipe_df is not None:
        display_recipes_with_checkboxes(st.session_state.similar_recipe_df) # df 표시

    if st.session_state.recipe_df_selected_name:
        search_recipe(recipe_name=st.session_state.recipe_df_selected_name) # 이 함수에서 클릭된 행에대한 처리 시작