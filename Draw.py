import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# opencv는 한글 텍스트를 출력하지 못한다.
# def draw(image, boxes, confidences, labels):
#     print("\n최종 결정:")
#     if len(boxes) > 0:
#         for box, conf, label in zip(boxes, confidences, labels):
#             x1, y1, x2, y2 = map(int, box)
#             label_name = label

#             # 사각형 테두리 그리는 함수(사각형을 그릴 이미지, 사각형 좌상단 좌표, 사각형 우하단 좌표, 사각형 색, 사각형 두께)
#             cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             # 텍스트 추가하는 함수(텍스트 추가할 이미지, 텍스트 문자열, 텍스트 시작점, 텍스트 폰트, 텍스트 크기, 텍스트 색상, 텍스트 두께)
#             cv2.putText(image, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
#             # 박스 좌표, 신뢰도, 라벨이름 출력
#             print(f'박스 좌표: {box}, 신뢰도: {conf}, 라벨: {label_name}')

# Pillow를 사용하여 한글 텍스트를 출력한다.
def draw_with_pil(image, boxes, confidences, labels):
    print("\n최종 결정:")
    
    # OpenCV 이미지를 PIL 이미지로 변환
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    
    # 한글 폰트 경로 설정 (여기서는 예시로 나눔고딕 폰트를 사용)
    font_path = "font/ONE Mobile POP.ttf"  # 실제 한글 폰트 파일 경로로 변경
    font_size = 32
    font = ImageFont.truetype(font_path, font_size)

    if len(boxes) > 0:
        for box, conf, label in zip(boxes, confidences, labels):
            x1, y1, x2, y2 = map(int, box)
            label_name = label
            
            # 사각형 그리기
            draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 127), width=2)

            # 텍스트 추가
            text = f'{label_name} {conf:.2f}'
            draw.text((x1, y1 - 30), text, fill=(0, 128, 255), font=font)  # 텍스트 색상과 폰트 지정

            # 박스 좌표, 신뢰도, 라벨이름 출력
            print(f'박스 좌표: {box}, 신뢰도: {conf}, 라벨: {label_name}')

    # 다시 OpenCV 이미지로 변환
    image_with_boxes = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    
    return image_with_boxes