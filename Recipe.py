import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity

recipe_df = pd.read_csv("C:/Users/hj/Desktop/FINAL/YHJ/final-project/labels_translation/preprocessed_kr_recipe.csv")
recipe_df = recipe_df[['요리명', '재료리스트', '조회수', '추천수', '스크랩수',
                       '요리타입', '음식분위기', '재료타입', '음식타입', '몇인분',
                       '요리난이도', '요리시간', '레시피일련번호']]

# 재료가 하나 이상 포함하되 많이 포함되는 순으로 추출하는 함수
def search_by_most_ingredients(detected_ingredients):
    # '포함된 재료' 열에 포함된 재료들을 담음
    recipe_df['포함된 재료'] = recipe_df['재료리스트'].apply(
        lambda x: ', '.join([ingredient for ingredient in detected_ingredients if ingredient in x])
    )
    
    # 포함된 재료의 개수를 세는 열을 추가
    recipe_df['포함된 재료 개수'] = recipe_df['포함된 재료'].apply(lambda x: len(x.split(', ')) if x else 0)
    
    # '포함된 재료 개수' 기준으로 내림차순 정렬
    search_results = recipe_df[recipe_df['포함된 재료 개수'] > 0].sort_values(by='포함된 재료 개수', ascending=False)
    
    # 열 순서를 지정하여 데이터프레임을 반환
    search_results = search_results[['요리명', '포함된 재료 개수', '포함된 재료', '재료리스트',
                                     '조회수', '추천수', '스크랩수', '요리타입', '음식분위기',
                                     '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간', '레시피일련번호']]
    
    return search_results

# 재료가 모두 포함된 행들 반환하는 함수
def search_all_include(detected_ingredients):
    # 모든 재료를 포함하는 행 필터링, all(): 위에서 인식된 재료 리스트 전부가 x에 포함되어있으면 true 반환
    search_results = recipe_df[recipe_df['재료리스트'].apply(lambda x: all(ingredient in x for ingredient in detected_ingredients))]
    return search_results

# 랜덤 추천
def search_random_recipe():
    # recipe_df의 행 수를 사용하여 랜덤 숫자 생성
    random_number = random.randint(0, recipe_df.shape[0] - 1) # 0부터 (행 수 - 1)까지의 숫자 생성
    search_results = recipe_df.iloc[random_number]
    return search_results

# 유사한 추천레시피 만들기
def search_similar_recipe(recipe_number):
    # 특징으로 사용할 열 선택
    select_columns = ['요리명', '재료리스트', '조회수', '요리타입', '음식분위기',
                        '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간', '레시피일련번호']

    # 추천 데이터 프레임 만들기
    recommend_df = recipe_df[select_columns]

    # 텍스트 벡터화
    text_vectorizer = CountVectorizer()

    # 범주형 인코딩
    categorical_encoder = OneHotEncoder(handle_unknown='ignore') # 존재하지 않는 새로운 범주가 데이터에 나타나면 새로운 범주는 무시

    # ColumnTransformer를 사용하여 텍스트와 범주형 변수 처리
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_vectorizer, '재료리스트'),
            ('cat', categorical_encoder, ['요리타입', '음식분위기', '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간'])
        ]
    )

    # 데이터 전처리 및 벡터화
    X = preprocessor.fit_transform(recommend_df)

    # 사용자가 사용한 적 있던 레시피를 따로 DataFrame으로 변환
    user_recipe_df = recommend_df[recommend_df['레시피일련번호'] == recipe_number]

    # 사용자 레시피 데이터만 전처리 및 벡터화
    user_recipe_vec = preprocessor.transform(user_recipe_df)

    # 기존 데이터프레임의 벡터화
    recommend_df_vec = preprocessor.transform(recommend_df)

    # 유사도 계산
    cosine_similarities = cosine_similarity(user_recipe_vec, recommend_df_vec).flatten()

    # 유사도에 따라 레시피 추천 (자기 자신 제외)
    # user_recipe_df의 인덱스를 제외하기 위해 +1 (인덱스 조정)
    similar_recipe_indices = cosine_similarities.argsort()[::-1][1:11]  # 유사도가 높은 상위 20개 레시피 추천

    recommended_recipes = recommend_df.iloc[similar_recipe_indices]

    # 추천된 레시피 출력
    return recommended_recipes