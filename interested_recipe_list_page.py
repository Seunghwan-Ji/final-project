import streamlit as st
from load_interested_recipe_page import *
from recommend_similar_recipe_page import *

def show_interested_recipe_list():
    st.markdown("""
        <style>
            .stButton > button {
                font-size: 15px;
                background-color: #fdffeb;
                color: #727421;
                text-align: center;
                border: 8px outset #fdffb2;
                border-radius: 8px;
                margin: 5px 0px 0px 0px;
            }
            h1#afcbc26e {
                color: #727421;
                text-shadow: 3px  3px 0 #fff;
            }
            .custom-image {
                border: 5px inset #fdffb2;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("관심 요리 목록")
        
    # 관심 요리 목록이 비어있는지 확인
    if not st.session_state.interested_recipe_list:
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
                관심 요리 목록이 비어있습니다.
            </p>""", unsafe_allow_html=True)
    else:
        num_columns = 3
        cols = st.columns(num_columns)
        
        # 각 레시피 이름과 이미지 URL을 보여주고 삭제 기능 추가
        for index, (recipe_number, recipe_name, photo_url) in enumerate(st.session_state.interested_recipe_list):
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
                    st.session_state.selected_interested_recipe_name = recipe_name
                    st.experimental_rerun()

                # 비슷한 레시피 추천 받기 버튼 추가
                if st.button("비슷한 레시피 추천 받기", key=f"recommend_{index}", use_container_width=True):
                    st.session_state.recommend_similar_recipe_page = True
                    st.session_state.selected_interested_recipe_number = recipe_number
                    st.write(f"'{recipe_name}' 와 비슷한 레시피를 추천받는 기능을 여기에 구현하세요.")
                    st.experimental_rerun()

                # 삭제 버튼 추가
                if f"delete_{index}_clicked" not in st.session_state:
                    st.session_state[f"delete_{index}_clicked"] = False

                if st.session_state[f"delete_{index}_clicked"]:
                    # 삭제 확인 메시지
                    st.write(f"'{recipe_name}' 요리를 삭제하시겠습니까?")
                    
                    # "예" 버튼
                    if st.button("예", key=f"confirm_delete_{index}", use_container_width=True):
                        # 관심 요리 목록에서 해당 요리 삭제
                        st.session_state.interested_recipe_list.pop(index)
                        st.session_state[f"delete_{index}_clicked"] = False # 클릭 상태 초기화
                        st.experimental_rerun()  # 페이지를 새로 고침하여 변경사항 반영
                    
                    # "아니오" 버튼
                    if st.button("아니오", key=f"cancel_delete_{index}", use_container_width=True):
                        st.session_state[f"delete_{index}_clicked"] = False
                        st.experimental_rerun()

                else:
                    if st.button("삭제", key=f"delete_{index}", use_container_width=True):
                        st.session_state[f"delete_{index}_clicked"] = True
                        st.experimental_rerun()

def interested_recipe_list_page():
    if st.session_state.load_interested_recipe_page:
        load_interested_recipe_page(st.session_state.selected_interested_recipe_name)
    elif st.session_state.recommend_similar_recipe_page:
        recipe_number = st.session_state.selected_interested_recipe_number
        recommend_similar_recipe_page(recipe_number)
    else:
        show_interested_recipe_list()
