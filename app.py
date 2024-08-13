import streamlit as st
from streamlit_option_menu import option_menu
from camera_recognize_ingredient_page import *
from input_ingredient_page import *
from recommend_random_recipe_page import *
from interested_recipe_list_page import *
from searched_recipe_history_list_page import *

# =========================================================================================================
# 세션 상태 변수

# 선택된 메뉴
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "메인"

# 카메라 활성화 상태
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False

# 탐지된 라벨 집합
if 'detected_label_set' not in st.session_state:
    st.session_state.detected_label_set = set()

# 인식 마치기 버튼 활성화 상태
if 'finish_recognizing_button' not in st.session_state:
    st.session_state.finish_recognizing_button = False

# 라벨 수정 페이지 활성화 상태
if 'modify_label_page' not in st.session_state:
    st.session_state.modify_label_page = False

# 라벨별 수정 버튼이 눌렸는지 여부, {라벨: 참/거짓}
if 'edit_label' not in st.session_state:
    st.session_state.edit_label = {}

# 레시피 검색 페이지 활성화 상태
if 'search_recipe_page' not in st.session_state:
    st.session_state.search_recipe_page = False

# "모든 재료가 포함된 레시피만 보기" 체크박스 상태
if 'include_all_ingredients' not in st.session_state:
    st.session_state.include_all_ingredients = False

# 레시피 데이터 프레임에서 정렬 기준이 되는 열 이름
if 'recipe_df_sort_by' not in st.session_state:
    st.session_state.recipe_df_sort_by = None

# 조리 가능한 레시피 존재 여부
if 'exist_cookable_recipe' not in st.session_state:
    st.session_state.exist_cookable_recipe = False

# 레시피 데이터 프레임에서 선택된 레시피 일련번호
if 'recipe_df_selected_number' not in st.session_state:
    st.session_state.recipe_df_selected_number = None

# 레시피 데이터 프레임에서 선택된 레시피 이름
if 'recipe_df_selected_name' not in st.session_state:
    st.session_state.recipe_df_selected_name = None

# 검색된 레시피 정보
if 'searched_recipe_info' not in st.session_state:
    st.session_state.searched_recipe_info = None

# 검색된 레시피 정보 가리기(다른 행 선택시)
if 'hide_searched_recipe_info' not in st.session_state:
    st.session_state.hide_searched_recipe_info = False

# 초기 랜덤 레시피 로드
if 'random_recipe' not in st.session_state:
    st.session_state.random_recipe = random_recipe()

# 관심 요리 리스트
if 'interested_recipe_list' not in st.session_state:
    st.session_state.interested_recipe_list = [] # 초기화X

# 관심 요리 메뉴에서 "레시피 보기" 페이지 활성화 상태
if 'load_interested_recipe_page' not in st.session_state:
    st.session_state.load_interested_recipe_page = False

# "레시피 보기" 버튼을 클릭한 레시피의 이름
if 'selected_interested_recipe_name' not in st.session_state:
    st.session_state.selected_interested_recipe_name = None

# 관심 요리 메뉴에서 "비슷한 레시피 추천 받기" 페이지 활성화 상태
if 'recommend_similar_recipe_page' not in st.session_state:
    st.session_state.recommend_similar_recipe_page = False

# "비슷한 레시피 추천 받기" 버튼을 클릭한 레시피의 일련번호
if 'selected_interested_recipe_number' not in st.session_state:
    st.session_state.selected_interested_recipe_number = None

# 레시피 검색 기록 리스트
if 'searched_recipe_history_list' not in st.session_state:
    st.session_state.searched_recipe_history_list = [] # 초기화X

# =========================================================================================================
# 함수

# 세션 상태 변수 초기화 함수
def reset_session_state():
    st.session_state.selected_menu = "메인"
    st.session_state.camera_running = False
    st.session_state.detected_label_set = set()
    st.session_state.finish_recognizing_button = False
    st.session_state.modify_label_page = False
    st.session_state.edit_label = {}
    st.session_state.search_recipe_page = False
    st.session_state.include_all_ingredients = False
    st.session_state.recipe_df_sort_by = None
    st.session_state.exist_cookable_recipe = False
    st.session_state.recipe_df_selected_number = None
    st.session_state.recipe_df_selected_name = None
    st.session_state.searched_recipe_info = None
    st.session_state.hide_searched_recipe_info = False
    st.session_state.random_recipe = random_recipe()
    st.session_state.load_interested_recipe_page = False
    st.session_state.selected_interested_recipe_name = None
    st.session_state.recommend_similar_recipe_page = False
    st.session_state.selected_interested_recipe_number = None

# 사이드바 메뉴 & 연결된 페이지
def run():
    sidebar_menu, connected_page = st.columns([1, 9])

    # 메뉴 보여주기
    with sidebar_menu:
        with st.sidebar:
            selected_menu = option_menu("메뉴",
                                        ["메인", "카메라 식재료 인식", "식재료 직접 입력",
                                         "무작위 요리 추천", "관심 요리 목록", "요리 검색 기록"],
                                        icons=['house', 'camera', 'pencil', 'shuffle', 'heart', 'clock-history'], # 각 메뉴에 아이콘 표시
                                        menu_icon="cast", 
                                        default_index=0)
            
            change_menu(selected_menu)
    
    # 연결된 페이지 보여주기
    with connected_page:
        if st.session_state.selected_menu == "메인":
            main_page()
            
        if st.session_state.selected_menu == "카메라 식재료 인식":
            camera_recognize_ingredient_page()
        
        if st.session_state.selected_menu == "식재료 직접 입력":
            input_ingredient_page()
        
        if st.session_state.selected_menu == "무작위 요리 추천":
            recommend_random_recipe_page()

        if st.session_state.selected_menu == "관심 요리 목록":
            interested_recipe_list_page()
        
        if st.session_state.selected_menu == "요리 검색 기록":
            searched_recipe_history_list_page()

# 선택된 메뉴 업데이트
def change_menu(selected_menu):
    # 현재 선택된 페이지가 변경된 경우에만 상태 초기화
    if st.session_state.selected_menu != selected_menu:
        reset_session_state() # 모든 세션 상태 변수 초기화
        st.session_state.selected_menu = selected_menu
        st.experimental_rerun() # 메인 모듈(app.py)부터 다시 실행

# 메인 페이지
def main_page():
    st.image('app_gui/main_icon.png', width=600)

    # 첫 화면 아래 설명글 첫번째
    st.markdown("""
        <style>
            .subtitle {
                font-size: 29px;
                font-family: 'Fira Code';
                font-weight: bold;
                color: #727421;
                background-color: #fdffeb;
                border: 10px outset #fdffb2;
                text-shadow: 3px  3px 0 #fff;
                margin: 50px 0px 50px 0px;
                border-radius: 8px;
                padding: 10px 0px 10px 0px;
                text-align: center;
            }
        </style>
        <p class=subtitle>
            갖고 있는 식재료를 보여주세요!<br>
            적합한 레시피를 추천해 드리겠습니다.
        </p>""", unsafe_allow_html=True)
    
    # 첫 화면 아래 설명글 두번째
    st.markdown("""
        <style>
            .explanation {
                font-size: 20px;
                color: #727421;
                font-weight: bold;
                background-color: #fdffeb;
                border: 10px outset #fdffb2;
                text-shadow: 2px  2px 0 #fff;
                font-family: 'Fira Code';
                text-align: center;  /* 가운데 정렬 */
                padding: 10px 40px 10px 40px;
                border-radius: 8px;
            }
        </style>
        <p class=explanation>
            왼쪽에서 메뉴를 선택하세요.
        </p>""", unsafe_allow_html=True)

# =========================================================================================================
# 앱 시작

st.set_page_config(
    page_title='MultiCampus AvengersEnsemble',
    page_icon='app_gui/title_icon.png'
)

# background
background = '''
    <style>
    .stApp {
        background-image: url("https://github.com/Seunghwan-Ji/final-project/blob/jin/app_gui/back_ground.png?raw=true");
        background-size: cover;
        background-position: center;
        min-height: 100vh;
    }
    .stApp > header {
        background-color: #f2e4d7;
        background-size: cover;
    }

    .st-emotion-cache-6qob1r {
        background-color: #dcd0c3;
        background-size: cover;
    }
    </style>
    '''

st.markdown(background, unsafe_allow_html=True)

# 이 모듈이 다른 모듈에 의해 임포트 되지않고 직접 실행되면 아래 함수 실행
if __name__ == "__main__":
    run()