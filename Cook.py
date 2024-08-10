import requests
from bs4 import BeautifulSoup

def get_valid_recipe_url(recipe_name):
    # 검색 페이지 URL
    search_url = f"https://www.10000recipe.com/recipe/list.html?q={recipe_name}"
    search_response = requests.get(search_url)
    search_soup = BeautifulSoup(search_response.content, 'html.parser')

    # 검색 결과에서 유효한 레시피 링크를 찾기
    for i in range(1, 41):  # 첫 페이지 40개의 결과중 동영상이 포함된 레시피 찾기
        recipe_link = search_soup.select_one(f'#contents_area_full > ul > ul > li:nth-child({i}) > div.common_sp_thumb > a')
        if recipe_link and recipe_link.find('span'):
            recipe_url = "https://www.10000recipe.com" + recipe_link['href']
            return recipe_url
    
    # 동영상이 포함된 레시피가 없는 경우, 첫 번째 레시피 링크 반환
    recipe_link = search_soup.select_one(f'#contents_area_full > ul > ul > li:nth-child(1) > div.common_sp_thumb > a')
    if recipe_link and recipe_link.find('img'):
        recipe_url = "https://www.10000recipe.com" + recipe_link['href']
        return recipe_url

    return None

def get_recipe_info(recipe_url):
    recipe_response = requests.get(recipe_url)
    recipe_soup = BeautifulSoup(recipe_response.content, 'html.parser')

    # 요리 사진
    photo_url = recipe_soup.select_one('#main_thumbs')['src']

    # 재료
    ingredients = []
    ingredient_number = 2
    while True:
        # 이 동적태그를 2부터 대입해서 순회한다.
        ingredient_li = recipe_soup.select_one(f'#divConfirmedMaterialArea > ul > li:nth-child({ingredient_number})')
        if not ingredient_li:
            break # 다음 태그가 존재하지 않으면 대입을 멈추고 빠져나간다.
        ingredients.append(ingredient_li.get_text(strip=True))
        ingredient_number += 1
    ingredients_text = "\n".join(ingredients).replace("구매", "") # 재료 텍스트 옆에 "구매" 텍스트를 지운다.

    # 요리 영상
    video_iframe = recipe_soup.select_one('#ifrmRecipeVideo')
    video_url = None
    if video_iframe:
        video_url = video_iframe.get('org_src')

    # 조리 순서
    steps = []
    step_number = 1 # 조리 단계, 동적 태그의 시작값
    while True:
        step_descr = recipe_soup.select_one(f'#stepdescr{step_number}') # 이 동적태그를 1부터 대입해서 순회한다.

        if not step_descr:
            break # 다음 태그가 존재하지 않으면 대입을 멈추고 빠져나간다.
        
        step_text = step_descr.get_text() # 조리설명 텍스트(메인설명 + 부연설명)
        # print('==' * 50)
        # print('step_text:')
        # print(step_text)

        # 이 작업은 메인설명 텍스트와 부연설명 텍스트들이 가로로 이어져있는 형태를
        # 줄바꿈 문자를 연결해 세로로 이어주는 역할을한다.
        p_tags = step_descr.select('p') # step_descr 태그안에 p 태그가 존재한다, p 태그는 메인설명 밑에 부연설명하는 텍스트이다.
        if p_tags:
            sub_text = ""
            for p_tag in p_tags:
                p_text = p_tag.get_text() # 부연설명 텍스트
                sub_text += ("\n" + p_text) # 부연설명 텍스트끼리 줄바꿈 문자로 연결해 저장해둔다.
                # print('\nsub_text:')
                # print(sub_text)

                parts = step_text.rsplit(p_text, 1) # 조리설명 텍스트에서 현재 부연설명 텍스트를 제거한다.(메인설명 텍스트만 남기기 위해서다.)
                # print('\nparts:')
                # print(parts)
                step_text = "".join(parts) # 수정한 조리설명 텍스트를 업데이트한다.(스플릿은 리스트형태로 만드므로 조인으로 리스트를 벗긴다.)
                # print('\nstep_text:')
                # print(step_text)
            
            step_text += ("\n" + sub_text) # 메인설명 텍스트만 남은 문장에 저장해둔 부연설명들을 추가해준다.
            # print('\nstep_text:')
            # print(step_text)
        
        # 조리 이미지
        step_img = recipe_soup.select_one(f'#stepimg{step_number} > img')
        step_image_url = step_img['src'] if step_img else None

        steps.append({
            "text": step_text,
            "image_url": step_image_url
        })
        step_number += 1

    # 팁/주의사항
    tips = recipe_soup.select_one('#obx_recipe_step_start > dl > dd')
    tips_text = tips.get_text() if tips else "팁/주의사항이 없습니다."

    return {
        "photo_url": photo_url,
        "ingredients": ingredients_text,
        "video_url": video_url,
        "steps": steps,
        "tips": tips_text
    }