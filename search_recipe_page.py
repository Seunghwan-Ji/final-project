import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from Recipe import *
from Cook import *

def search_recipe_page():
    col1, _ = st.columns([3, 8])
    
    # button CSS
    st.markdown("""
        <style>
        .st-emotion-cache-1vt4y43.ef3psqc12 {
            background-color: #fdffeb;
            color: #727421;
            font-size: 25px;
            font-weight: bold;
            width: 100%;
            height: 50px;
            border: 7px outset #fdffb2;
        }
        .st-emotion-cache-1vt4y43.ef3psqc12:hover {
            background-color: #ffffD3;
            border: 7px outset #FFFF41;
        }
    </style>
    """, unsafe_allow_html=True)

    back_button = col1.empty()

    st.image("app_gui/user.png", width=650)
    
    st.markdown(f"""
        <style>
            .user_ingredients {{
            font-size: 30px;
            font-family: 'Fira Code';
            font-weight: bold;
            color: #727421;
            border-radius: 8px;
            background-color: #fdffeb;
            border: 5px dotted  #fdffb2;
            text-shadow: 3px  3px 0 #fff;
            text-align: center;
            padding: 5px 5px 5px 5px;
            margin: 50px 0px 50px 0px;
            }}
        </style>
    <p class=user_ingredients>
        {", ".join(st.session_state.detected_label_set)}
    </p>
    """, unsafe_allow_html=True)
    
    # checkbox CSS
    st.markdown("""
        <style>
            .stCheckbox > label {
                font-size: 20px;
                font-weight: bold;
                color: #727421;
                background-color: #fdffeb;
                padding: 5px;
                border-radius: 8px;
                border: 5px dotted #fdffb2;
                display: flex;
                align-items: center;
            }
        </>
    """, unsafe_allow_html=True)

    # Streamlit 체크박스 생성
    st.session_state.include_all_ingredients = st.checkbox("모든 재료를 포함한 레시피 보기")

    # 열 정의
    if not st.session_state.include_all_ingredients:
        col1, _, col2, _, col3, _, col4 = st.columns([6, 1.5, 4, 2, 4, 2, 5])
        with col1:
            if st.button("재료 포함순", help="재료가 많이 포함된 순서"):
                st.session_state.recipe_df_sort_by = (None, "재료가 많이 포함된순")
        
        with col2:
            if st.button("추천순", help="추천수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("추천수", "추천순")
                
        with col3:
            if st.button("조회순", help="조회수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("조회수", "조회순")
        
        with col4:
            if st.button("스크랩순", help="스크랩수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("스크랩수", "스크랩순")
    else:
        if st.session_state.recipe_df_sort_by == (None, "재료가 많이 포함된순"):
            st.session_state.recipe_df_sort_by = ("추천수", "추천순") # 이 경우엔 추천순을 기본값으로 적용

        col1, col2, col3 = st.columns([5, 5, 5])
        with col1:
            if st.button("추천순", help="추천수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("추천수", "추천순")

        # 기존 버튼들
        with col2:
            if st.button("조회순", help="조회수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("조회수", "조회순")
                
        with col3:
            if st.button("스크랩순", help="스크랩수가 많은 순서"):
                st.session_state.recipe_df_sort_by = ("스크랩수", "스크랩순")

    if st.session_state.recipe_df_sort_by:
        check_exist_cookable_recipe()

    if st.session_state.recipe_df_selected_number is None:
        if back_button.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.modify_label_page = True
            st.session_state.recipe_df_sort_by = None
            st.experimental_rerun()
  
def check_exist_cookable_recipe():
    if st.session_state.include_all_ingredients:
        # 모든 재료가 포함된 행 추출
        recipe_results = search_all_include(st.session_state.detected_label_set)
    else:
        # 재료가 많이 포함된 순으로 행 추출
        recipe_results = search_by_most_ingredients(st.session_state.detected_label_set)
    
    if recipe_results.shape[0] > 0:
        if st.session_state.recipe_df_sort_by != (None, "재료가 많이 포함된순"):
            recipe_results = recipe_results.sort_values(by=st.session_state.recipe_df_sort_by[0], ascending=False)
            # recipe_results = recipe_results.set_index('요리명') # '요리명' 열을 인덱스로 전환

        st.markdown(f"""
            <style>
                .recipe_subheader {{
                    font-size: 25px;
                    background-color: #fdffeb;
                    color: #727421;
                    text-align: center;
                    text-shadow: 3px  0px 0 #fff;
                    border-radius: 8px;
                    margin: 50px 0px 10px 0px;
                    border: 2px outset #fdffb2;
                    width: 500px;
                    }}
            </style>
            <p class=recipe_subheader>
                {st.session_state.recipe_df_sort_by[1]} 레시피🧑‍🍳
            </p>""", unsafe_allow_html=True)
        
        st.markdown("""
                    <style>
                        .dvn-scroller.glideDataEditor {
                            border: 10px outset #fdffb2;
                        }
                    </style>
                    """,  unsafe_allow_html=True)

        # st_aggrid를 사용하여 데이터프레임을 표시하고 행을 선택할 수 있도록 설정
        gb = GridOptionsBuilder.from_dataframe(recipe_results)
        gb.configure_selection(selection_mode="single", use_checkbox=True)
        grid_options = gb.build()

        grid_response = AgGrid(
            recipe_results,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            height=400,
            width='100%',
            theme='alpine',
        )

        selected_row = grid_response['selected_rows'] # 데이터 프레임에서 사용자가 클릭한 행의 정보(df 형태이다.)

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
        st.write("보유하신 재료로 조리 가능한 레시피가 없습니다.")

def search_recipe(recipe_name=None, random_recipe=False):
    clicked = False
    if recipe_name:
        st.image("app_gui/random_recipe_icon.png")

        col1, col2 = st.columns([3, 7])
        
        if not random_recipe:
            if col1.button("뒤로 가기"):
                st.session_state.search_recipe_page = False
                st.session_state.modify_label_page = True
                st.session_state.recipe_df_sort_by = None
                st.session_state.recipe_df_selected_name = None
                st.session_state.recommend_similar_recipe_page = False
                st.session_state.selected_interested_recipe_number = None
                st.session_state.recipe_df_selected_number = None
                
                if st.session_state.searched_recipe_info: # 검색된 레시피 정보가 있는지 확인
                    st.session_state.searched_recipe_info = None
                
                st.experimental_rerun()

        if col2.button(f"'{recipe_name}' 레시피 상세안내 보기"):
            clicked = True
            status_placeholder = st.empty() # 빈 자리표시자 생성
            status_placeholder.text("로드 중입니다...")
    else:
        st.image("app_gui/show_recipe.png")
        
        # 검색 기능
        recipe_name = st.text_input("")
        return_button, search_button = st.columns([5, 5])
        if search_button.button("검색"):
            if recipe_name:
                clicked = True
                status_placeholder = st.empty() # 빈 자리표시자 생성
                status_placeholder.text("검색 중입니다...")
        
        if return_button.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.modify_label_page = True
            st.session_state.recipe_df_sort_by = None
            st.session_state.recipe_df_selected_name = None
            
            if st.session_state.searched_recipe_info: # 검색된 레시피 정보가 있는지 확인
                st.session_state.searched_recipe_info = None
            
            st.experimental_rerun()

    if clicked:
        st.session_state.hide_searched_recipe_info = False
        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.searched_recipe_info = recipe_info
        else:
            st.session_state.searched_recipe_info = None
            st.text(f"'{recipe_name}' 레시피의 시각적인 정보를 찾지 못했습니다.")
        
        # 검색 완료 후 텍스트 제거
        status_placeholder.empty()

    # 검색 결과 표시
    if not st.session_state.hide_searched_recipe_info and st.session_state.searched_recipe_info:
        search_result(recipe_name)

def search_result(recipe_name, call_from_history_menu=False):
    recipe_number = st.session_state.recipe_df_selected_number
    photo_url = st.session_state.searched_recipe_info["photo_url"]
    searched_recipe = (recipe_number, recipe_name, photo_url)
    
    # "요리 검색 기록" 메뉴에 저장
    if searched_recipe not in st.session_state.searched_recipe_history_list:
        st.session_state.searched_recipe_history_list.append(searched_recipe)
    
    if not st.session_state.load_interested_recipe_page or call_from_history_menu:
        # "관심 요리 목록에 추가하기" 버튼
        if st.button("관심 요리 목록에 추가하기", use_container_width=True):
            if searched_recipe not in st.session_state.interested_recipe_list:
                st.session_state.interested_recipe_list.append(searched_recipe)
                st.success(f"'{recipe_name}' 이(가) 관심 요리 목록에 추가되었습니다!")
            else:
                st.success("이미 추가된 요리입니다.")

    # 요리 이름
    st.markdown(f"""
        <style>
            .recipe_name {{
                font-size: 30px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                border-radius: 8px;
                background-color: #ffff9e;
                border: 10px double #ffd655;
                text-shadow: 3px  3px 0 #fff;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 50px 0px 10px 0px;
                }}
        </style>
        <p class=recipe_name>
            {recipe_name}
        </p>
                        """, unsafe_allow_html=True)

    # 요리된 사진
    st.image(st.session_state.searched_recipe_info["photo_url"])
    
    # 재료
    st.markdown(f"""
        <style>
            .ingredient_1 {{
                font-size: 30px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                border-radius: 8px;
                background-color: #ffff9e;
                border: 10px double #ffd655;
                text-shadow: 3px  3px 0 #fff;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 200px 0px 10px 0px;
                }}
        </style>
        <p class=ingredient_1>
            재료
        </p>
        
    """, unsafe_allow_html=True)
    
    # 재료 목록
    ingredients2 = "<br>".join(list(st.session_state.searched_recipe_info["ingredients"].split("\n")))
    
    st.markdown(f"""
        <style>
            .ingredients2 {{
                font-size: 20px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                border-radius: 8px;
                background-color: #fdffeb;
                border: 5px dotted  #fdffb2;
                text-shadow: 3px  3px 0 #fff;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 1px 0px 200px 0px;
                }}
        </style>
        <p class=ingredients2>
            {ingredients2}
        </p>
                """, unsafe_allow_html=True)
    
    # 요리 영상
    st.markdown(f"""
        <style>
            .video {{
                font-size: 30px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                background-color: #ffff9e;
                border: 10px double #ffd655;
                text-shadow: 3px  3px 0 #fff;
                border-radius: 8px;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 20px 0px 10px 0px;
                }}
        </style>
        <p class=video>
            요리 영상
        </p>
    """, unsafe_allow_html=True)

    if st.session_state.searched_recipe_info["video_url"]:
        st.video(st.session_state.searched_recipe_info["video_url"])
    else:
        st.warning("요리 영상이 없습니다.")

    # 조리 순서
    st.markdown(f"""
        <style>
            .cooking {{
                font-size: 30px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                border-radius: 8px;
                background-color: #ffff9e;
                border: 10px double #ffd655;
                text-shadow: 3px  3px 0 #fff;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 200px 0px 20px 0px;
                }}
        </style>
        <p class=cooking>
            조리 순서
        </p>
    """, unsafe_allow_html=True)

    # HTML 문자열 생성
    html_steps = ""
    for step in st.session_state.searched_recipe_info["steps"]:
        if step["image_url"]:
            html_steps += f"<img src='{step['image_url']}' class=step-image /> <br>"
        if step["text"]:
            text_str = "<br>".join(step['text'].split("\n"))
            html_steps += f"<p class=cooking1>{text_str}</p>"

    # 팁/주의사항
    tips = st.session_state.searched_recipe_info.get("tips", "")
    st.markdown(f"""
    <head>
        <style>
            .cooking1 {{
                font-size: 20px;
                color: #727421;
                font-family: 'Fira Code', monospace;
                font-weight: bold;
                border-radius: 8px;
                background-color: #fdffeb;
                border: 5px dotted #fdffb2;
                text-shadow: 3px 3px 0 #fff;
                text-align: center;
                padding: 5px 5px 5px 5px;
                margin: 10px 0 200px 0;
            }}
            .step-image {{
                width: 100%;
                max-width: 600px;
                margin: 100px 0px 0px 0px;
            }}
            .tips-section {{
                font-size: 20px;
                color: #727421;
                font-family: 'Fira Code';
                font-weight: bold;
                margin-top: 30px;
            }}
            .tips {{
                font-size: 30px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                border-radius: 8px;
                background-color: #fdffeb;
                border: 10px double #fdffb2;
                text-shadow: 3px  3px 0 #fff;
                text-align: center;
                padding: 4px 0px 4px 0px;
                margin: 200px 0px 20px 0px;
            }}
        </style>
    </head>
    <body>
        <div>
            {html_steps}
        </div>
            <h3 class = tips>팁/주의사항</h3>
        <p class='tips-section'>
        {tips}
        </p>
    </body>
    """, unsafe_allow_html=True)
