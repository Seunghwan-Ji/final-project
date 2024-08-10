import streamlit as st
from Recipe import *
from Cook import *

# 검색 모드가 활성화된 경우
def search_recipe_page(): # 데이터 프레임
    # button CSS
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #fdffeb;
            color: #727421;
            font-size: 25px;
            font-weight: bold;
            width: 100%;
            border: 7px outset #fdffb2;
        }
        .stButton>button:hover {
            background-color: #ffffD3;
            border: 7px outset #FFFF41;
        }
        </style>
    </style>
    """, unsafe_allow_html=True)
    
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
        {", ".join(st.session_state.detected_labels)}
    </p>
    """, unsafe_allow_html=True)
    
    # checkbox CSS
    st.markdown("""
        <style>
            .stCheckbox > label {
                font-size: 20px;
                font-weight: bold;
                color: #4f704b;
                background-color: #fdffeb;
                padding: 5px;
                border-radius: 8px;
                border: 5px dotted #fdffb2;
                display: flex;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit 체크박스 생성
    st.session_state.all_ingredients_include = st.checkbox("모든 재료를 포함한 레시피 보기")

    col1, col2, col3 = st.columns([5, 5, 5])

    # 버튼 클릭 처리
    with col1:
        if st.button("추천순"):
            st.session_state.recipe_df_sort_by = ("추천수", "추천순")
            
    with col2:
        if st.button("조회순"):
            st.session_state.recipe_df_sort_by = ("조회수", "조회순")
    
    with col3:
        if st.button("스크랩순"):
            st.session_state.recipe_df_sort_by = ("스크랩수", "스크랩순")

    if st.session_state.recipe_df_sort_by:
        if st.session_state.all_ingredients_include:
            # 모든 재료가 포함된 레시피 추천
            recipe_results = search_all_include(st.session_state.detected_labels)
        else:
            # 인식한 식재료 중 하나라도 포함된 레시피 추천
            recipe_results = search_include_at_least_one(st.session_state.detected_labels)
        
        if recipe_results.shape[0] > 0:
            recipe_results = recipe_results.sort_values(by=st.session_state.recipe_df_sort_by[0], ascending=False)
            recipe_results = recipe_results.set_index('요리명') # '요리명' 열을 인덱스로 전환

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
                        width: 300px;
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
            st.write(recipe_results)
            st.session_state.cook = True
        else:
            st.write("검색 결과가 없습니다.")
    
    if st.session_state.cook == False:
        if st.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.labels_modify_page = True
            
            if st.session_state.selected_recipe: # 검색 내역 확인
                st.session_state.hide_random_recipe_details = True # 검색 내역 숨기기
            
            st.experimental_rerun()

def cook(random_recipe=False, recipe_name=None): # 스크래핑
    st.image("app_gui/show_recipe.png")
    
    if not random_recipe:
        st.markdown("""
            <style>
                .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-d7.st-d8.st-d9.st-da.st-db.st-ev.st-ew.st-dc {
                    border: 5px dotted #fef8ad;
                    height: 200px
                    border-radius: 10px;
                    padding: 10px 10px 10px 10px;
                    font-size: 30px;
                    color: #333;
                    background-color: #f9f9f9;
                    width: 100%;
                }
                .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-f7.st-f8.st-f9.st-fa.st-db.st-ev.st-ew.st-dc {
                    border: 5px dotted #f2a653;
                    height: 200px
                    border-radius: 10px;
                    padding: 10px 10px 10px 10px;
                    font-size: 30px;
                    color: #333;
                    background-color: #f9f9f9;
                    width: 100%;
                }
            </style>""",
            unsafe_allow_html=True)   
        
        # 검색 기능
        recipe_name = st.text_input("")
        return_button, search_button = st.columns([5, 5])
    
    clicked = False
    if not random_recipe:
        if search_button.button("검색"):
            if recipe_name:
                st.session_state.hide_random_recipe_details = False
                clicked = True
                status_placeholder = st.empty() # 빈 자리표시자 생성
                status_placeholder.text("검색 중입니다...")
                
        if return_button.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.labels_modify_page = True
            if st.session_state.selected_recipe: # 검색 내역 확인
                st.session_state.hide_random_recipe_details = True # 검색 내역 숨기기
            st.experimental_rerun()
    elif random_recipe:
        if st.button(f"'{recipe_name}' 레시피 상세안내 보기"):
            st.session_state.hide_random_recipe_details = False
            clicked = True
            status_placeholder = st.empty() # 빈 자리표시자 생성
            status_placeholder.text("로드 중입니다...")

    if clicked:
        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.selected_recipe = recipe_info
        else:
            st.session_state.selected_recipe = None
            st.text(f"'{recipe_name}' 레시피의 시각적인 정보를 찾지 못했습니다.")
        
        # 검색 완료 후 텍스트 제거
        status_placeholder.empty()

    # 검색 결과 표시
    if st.session_state.selected_recipe and not st.session_state.hide_random_recipe_details:
        # 요리 이름
        st.markdown(f"""
            <style>
                .recipe_name {{
                    font-size: 20px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #727421;
                    border-radius: 8px;
                    background-color: #fdffeb;
                    border: 10px double #fdffb2;
                    text-shadow: 3px  3px 0 #fff;
                    text-align: center;
                    padding: 4px 0px 4px 0px;
                    margin: 1px 0px 10px 0px;
                    }}
            </style>
            <p class=recipe_name>
                {recipe_name}
            </p>
                            """, unsafe_allow_html=True)

        # 요리된 사진
        st.image(st.session_state.selected_recipe["photo_url"])
        
        # 재료
        st.markdown(f"""
            <style>
                .ingredient_1 {{
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
                    margin: 200px 0px 10px 0px;
                    }}
            </style>
            <p class=ingredient_1>
                재료
            </p>
            
        """, unsafe_allow_html=True)
        
        # 재료 목록
        ingredients2 = "<br>".join(list(st.session_state.selected_recipe["ingredients"].split("\n")))
        
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
                    background-color: #fdffeb;
                    border: 10px double #fdffb2;
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
        if st.session_state.selected_recipe["video_url"]:
            st.video(st.session_state.selected_recipe["video_url"])
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
                    background-color: #fdffeb;
                    border: 10px double #fdffb2;
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
        for step in st.session_state.selected_recipe["steps"]:
            if step["image_url"]:
                html_steps += f"<img src='{step['image_url']}' class=step-image /> <br>"
            if step["text"]:
                text_str = "<br>".join(step['text'].split("\n"))
                html_steps += f"<p class=cooking1>{text_str}</p>"

        # 팁/주의사항
        tips = st.session_state.selected_recipe.get("tips", "")
        st.markdown(f"""
        <head>
            <style>
                .cooking1 {{
                    font-size: 20px;
                    color: #8887f7;
                    font-family: 'Fira Code', monospace;
                    font-weight: bold;
                    border-radius: 8px;
                    background-color: #fae5fd;
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

def random_cook(random_recipe=False, recipe_name=None):
    if not random_recipe:
        st.markdown("""
            <style>
                .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-d7.st-d8.st-d9.st-da.st-db.st-ev.st-ew.st-dc {
                    border: 5px dotted #e3a9fa;
                    height: 200px
                    border-radius: 10px;
                    padding: 10px 10px 10px 10px;
                    font-size: 30px;
                    color: #B761B4;
                    background-color: #f9f9f9;
                    width: 100%;
                }
                .st-ct.st-bn.st-cu.st-bq.st-cx.st-cy.st-cz.st-d0.st-d1.st-d2.st-d3.st-d4.st-eu.st-d6.st-ar.st-ak.st-an.st-al.st-am.st-cd.st-ck.st-cl.st-cm.st-cn.st-co.st-f7.st-f8.st-f9.st-fa.st-db.st-ev.st-ew.st-dc {
                    border: 5px dotted #e3a9fa;
                    height: 200px
                    border-radius: 10px;
                    padding: 10px 10px 10px 10px;
                    font-size: 30px;
                    color: #B761B4;
                    background-color: #f9f9f9;
                    width: 100%;
                }
            </style>""",
            unsafe_allow_html=True)   
        # 검색 기능
        recipe_name = st.text_input("")
        return_button, search_button = st.columns([5, 5])
    clicked = False
    if not random_recipe:
        if search_button.button("검색"):
            if recipe_name:
                st.session_state.hide_random_recipe_details = False
                clicked = True
                status_placeholder = st.empty() # 빈 자리표시자 생성
                status_placeholder.text("검색 중입니다...")
                
        if return_button.button("뒤로 가기"):
            st.session_state.search_recipe_page = False
            st.session_state.labels_modify_page = True
            if st.session_state.selected_recipe: # 검색 내역 확인
                st.session_state.hide_random_recipe_details = True # 검색 내역 숨기기
            st.experimental_rerun()
    elif random_recipe:
        if st.button(f"{recipe_name} 레시피 상세안내 보기"):
            st.image("app_gui/random_recipe_icon.png", width=700)
            st.session_state.hide_random_recipe_details = False
            clicked = True
            status_placeholder = st.empty() # 빈 자리표시자 생성
            status_placeholder.text("로드 중입니다...")

    if clicked:
        recipe_url = get_valid_recipe_url(recipe_name)
        if recipe_url:
            recipe_info = get_recipe_info(recipe_url)
            st.session_state.selected_recipe = recipe_info
        else:
            st.session_state.selected_recipe = None
            st.text(f"'{recipe_name}' 레시피의 시각적인 정보를 찾지 못했습니다.")
        
        # 검색 완료 후 텍스트 제거
        status_placeholder.empty()

    # 검색 결과 표시
    if st.session_state.selected_recipe and not st.session_state.hide_random_recipe_details:
        
        # 요리 이름
        st.markdown(f"""
            <style>
                .recipe_name {{
                    font-size: 20px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #B761B4;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 10px double #e3a9fa;
                    text-shadow: 3px  3px 0 #fff;
                    text-align: center;
                    padding: 4px 0px 4px 0px;
                    margin: 1px 0px 10px 0px;
                    }}
            </style>
            <p class=recipe_name>
                {recipe_name}
            </p>
                            """, unsafe_allow_html=True)

        # 요리된 사진
        st.image(st.session_state.selected_recipe["photo_url"])
        
        # 재료
        st.markdown(f"""
            <style>
                .ingredient_1 {{
                    font-size: 30px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #B761B4;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 10px double #e3a9fa;
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
        ingredients2 = "<br>".join(list(st.session_state.selected_recipe["ingredients"].split("\n")))
        
        st.markdown(f"""
            <style>
                .ingredients2 {{
                    font-size: 20px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #B761B4;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 5px dotted  #e3a9fa;
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
                    color: #B761B4;
                    background-color: #FAECFE;
                    border: 10px double #e3a9fa;
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
        if st.session_state.selected_recipe["video_url"]:
            st.video(st.session_state.selected_recipe["video_url"])
        else:
            st.warning("요리 영상이 없습니다.")

        # 조리 순서
        st.markdown(f"""
            <style>
                .cooking {{
                    font-size: 30px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #B761B4;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 10px double #e3a9fa;
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
        

        for step in st.session_state.selected_recipe["steps"]:
            if step["image_url"]:
                html_steps += f"<img src='{step['image_url']}' class=step-image /> <br>"
            if step["text"]:
                text_str = "<br>".join(step['text'].split("\n"))
                html_steps += f"<p class=cooking1>{text_str}</p>"


        # 팁/주의사항
        tips = st.session_state.selected_recipe.get("tips", "")
        st.markdown(f"""
        <head>
            <style>
                .cooking1 {{
                    font-size: 20px;
                    color: #B761B4;
                    font-family: 'Fira Code', monospace;
                    font-weight: bold;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 5px dotted #e3a9fa;
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
                    color: #B761B4;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    margin-top: 30px;
                }}
                .tips {{
                    font-size: 30px;
                    font-family: 'Fira Code';
                    font-weight: bold;
                    color: #B761B4;
                    border-radius: 8px;
                    background-color: #FAECFE;
                    border: 10px double #e3a9fa;
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