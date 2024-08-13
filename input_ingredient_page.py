import streamlit as st
from modify_label_page import *
from search_recipe_page import *

def input_ingredient_page():
    if st.session_state.search_recipe_page:
        # 레시피 검색 페이지 진입
        search_recipe_page()

        if st.session_state.recipe_df_selected_name:
            search_recipe(recipe_name=st.session_state.recipe_df_selected_name)
    else:
        modify_label_page()
