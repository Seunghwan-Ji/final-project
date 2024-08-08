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
        ingredient_li = recipe_soup.select_one(f'#divConfirmedMaterialArea > ul > li:nth-child({ingredient_number})')
        if not ingredient_li:
            break
        ingredients.append(ingredient_li.get_text(strip=True))
        ingredient_number += 1
    ingredients_text = "\n".join(ingredients).replace("구매", "")

    # 요리 영상
    video_iframe = recipe_soup.select_one('#ifrmRecipeVideo')
    video_url = None
    if video_iframe:
        video_url = video_iframe.get('org_src')

    # 조리 순서
    steps = []
    step_number = 1
    while True:
        step_descr = recipe_soup.select_one(f'#stepdescr{step_number}')

        if not step_descr:
            break
        
        step_text = step_descr.get_text()

        p_tags = step_descr.select('p')
        if p_tags:
            sub_text = ""
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                sub_text += ("\n" + p_text)

                parts = step_text.rsplit(p_text, 1)
                step_text = "".join(parts)
            step_text += ("\n" + sub_text)
        
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