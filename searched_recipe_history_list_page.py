import streamlit as st
from load_interested_recipe_page import *

def show_searched_recipe_history_list():
    st.markdown("""
        <style>
            .stButton > button {
                font-size: 20px;
                background-color: #fdffeb;
                color: #727421;
                text-align: center;
                border: 5px outset #fdffb2;
                border-radius: 8px;
                margin: 5px 0px 0px 0px;
            }
            .custom-image {
                border: 5px inset #fdffb2;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            h1 {
                color: #727421;
                text-shadow: 3px  3px 0 #fff;
            }   
        </style>
        <h1> 레시피 검색 기록 </h1>
    """, unsafe_allow_html=True)
        
    # 관심 요리 목록이 비어있는지 확인
    if not st.session_state.searched_recipe_history_list:
        st.markdown(f"""
            <style>
                .subheader {{
                    font-size: 20px;
                    background-color: #fdffeb;
                    color: #727421;
                    text-align: center;
                    border: 5px dotted #fdffb2;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    width: auto;
                    }}
            </style>
            <p class=subheader>
                검색 기록이 없습니다.
            </p>""", unsafe_allow_html=True)
    else:
        num_columns = 3
        cols = st.columns(num_columns)
        
        # 각 레시피 이름과 이미지 URL을 보여주고 삭제 기능 추가
        for index, (recipe_number, recipe_name, photo_url) in enumerate(st.session_state.searched_recipe_history_list):
            col_index = index % num_columns  # 열 인덱스 계산
            
            with cols[col_index]:  # 해당 열에 내용 추가
                # 레시피 이름 표시
                st.markdown(f"##### {recipe_name}")  # 제목으로 레시피 이름 표시
                
                # 이미지 표시
                st.markdown(f"""
                    <style>
                        .custom-image {{
                            height: 200px;  /* 원하는 높이로 조절 */
                            width: 200px;    /* 원하는 너비로 조절 */
                        }}
                    </style>
                    <img src="{photo_url}" class="custom-image" />
                """, unsafe_allow_html=True)
                
                # 레시피 보기 버튼 추가
                if st.button("레시피 보기", key=f"view_{index}", use_container_width=True):
                    st.session_state.load_interested_recipe_page = True
                    st.session_state.recipe_df_selected_number = recipe_number
                    st.session_state.selected_interested_recipe_name = recipe_name
                    st.experimental_rerun()

                # 삭제 버튼 추가
                if f"delete_history_{index}_clicked" not in st.session_state:
                    st.session_state[f"delete_history_{index}_clicked"] = False

                if st.session_state[f"delete_history_{index}_clicked"]:
                    # 삭제 확인 메시지
                    st.write(f"'{recipe_name}' 요리 검색 기록을 삭제하시겠습니까?")
                    
                    # "예" 버튼
                    if st.button("예", key=f"confirm_delete_{index}", use_container_width=True):
                        # 관심 요리 목록에서 해당 요리 삭제
                        st.session_state.searched_recipe_history_list.pop(index)
                        st.session_state[f"delete_history_{index}_clicked"] = False # 클릭 상태 초기화
                        st.experimental_rerun()  # 페이지를 새로 고침하여 변경사항 반영
                    
                    # "아니오" 버튼
                    if st.button("아니오", key=f"cancel_delete_{index}", use_container_width=True):
                        st.session_state[f"delete_history_{index}_clicked"] = False
                        st.experimental_rerun()

                else:
                    if st.button("삭제", key=f"delete_{index}", use_container_width=True):
                        st.session_state[f"delete_history_{index}_clicked"] = True
                        st.experimental_rerun()

def searched_recipe_history_list_page():
    if st.session_state.load_interested_recipe_page:
        load_interested_recipe_page(st.session_state.selected_interested_recipe_name, call_from_history_menu=True)
    else:
        show_searched_recipe_history_list()
