import streamlit as st
from labels_modify_page import *
from search_recipe_page import *

def text_input():
    if st.session_state.labels_modify_page:
        input_labels_modify_page()
    elif st.session_state.search_recipe_page:
        # 레시피 검색 페이지 진입
        search_recipe_page()
    
        if st.session_state.cook:
            # 요리 안내
            cook()