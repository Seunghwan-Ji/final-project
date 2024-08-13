import pandas as pd
import random

recipe_df = pd.read_csv("C:/Users/Seunghwan/Desktop/데이터/preprocessed_kr_recipe.csv")
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
def random_recipe():
    # recipe_df의 행 수를 사용하여 랜덤 숫자 생성
    random_number = random.randint(0, recipe_df.shape[0] - 1) # 0부터 (행 수 - 1)까지의 숫자 생성
    search_results = recipe_df.iloc[random_number]
    return search_results
