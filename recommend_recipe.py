import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity


# pip install scikit-learn
# 레시피 가져오기
recipe_df = pd.read_csv("C:/Users/Seunghwan/Desktop/데이터/preprocessed_kr_recipe.csv")
recipe_df = recipe_df[['레시피일련번호', '요리명', '조회수', '추천수', '스크랩수',
                       '재료리스트', '요리타입', '음식분위기', '재료타입', '음식타입',
                       '몇인분', '요리난이도', '요리시간']]
# 결측치 제거
recipe_df.dropna(inplace=True)

# ?? 견과류 부분 삭제
recipe_df.drop(recipe_df[recipe_df['재료타입']=='??견과류'].index, inplace=True)

# 차/?슘?술 부분 삭제
recipe_df.drop(recipe_df[recipe_df['음식타입']=='차/?슘?술'].index, inplace=True)

# 특징으로 사용할 열 선택
select_columns = ['레시피일련번호', '조회수', '요리명', '요리타입', '음식분위기',
                    '재료타입', '음식타입', '몇인분', '요리난이도', '요리시간','재료리스트']

# 추천 데이터 프레임 만들기
recommend_df = recipe_df[select_columns]

# 유사한 추천레시피 만들기
def recommend_recipe(recipe_number):
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