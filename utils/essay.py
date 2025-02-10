import os

from django.conf import settings
from rest_framework.exceptions import APIException

from .upstage import get_answer_from_solar

import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
import numpy as np


prompt_paths = [
    os.path.join(settings.BASE_DIR, 'prompts', 'essay_prompt.txt'),
    os.path.join(settings.BASE_DIR, 'prompts', 'essay_prompt2.txt')
]


def evaluate(api_key, content, criteria):
    '''
    input:
    - content: OCR 추출 텍스트
    - criteria: EssayCriteria 인스턴스
    output:
    - summary_extract: 요약 추출 결과
    - penalty: 글자 수에 따른 패널티
    '''
    # prompt 불러오기
    try:
        with open(prompt_paths[0], 'r', encoding='utf-8') as f1, \
             open(prompt_paths[1], 'r', encoding='utf-8') as f2:
                prompt = f1.read()
                prompt2 = f2.read()
    except FileNotFoundError:
        raise APIException(f"Prompt file not found at path: {prompt_paths}")

    rule = "".join(criteria.criteria_items.values_list("content", flat=True))
    summary_extract = get_answer_from_solar(api_key, content, f"{prompt}\n{rule}\n{prompt2}")
    
    # 글자 수 계산
    char_cnt = len(content)
    
    # 글자 수 평가 기준 불러오기
    penalty = None
    for rule in criteria.ranges.values():
        if rule["min_value"] <= char_cnt and char_cnt < rule["max_value"]:
            penalty = rule["penalty"]
            break

    return summary_extract, penalty

def process_ocr_task_for_essay(api_key, content, confidence):
    threshold = 0.8
    # OCR 인식률 저하 시 경고 메시지 저장
    if confidence <= threshold:
        warning = f'경고: OCR 신뢰도가 낮습니다 ({confidence:.2f}). 텍스트가 부정확할 수 있습니다.\n'
        return warning + content
    else:
        prompt_path = os.path.join(settings.BASE_DIR, 'prompts', 'refine_prompt.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
        refined_content = get_answer_from_solar(api_key, content, prompt)
        return refined_content

def preprocess_pdf(pdf_path, output_path, manuscript_box=(54, 1050, 3430, 4810), dpi=300):
    
    pdf_doc = fitz.open(pdf_path)
    preprocessed_images = []

    for page in pdf_doc:
        pixmap = page.get_pixmap(dpi=dpi)
        img = Image.open(BytesIO(pixmap.tobytes("png")))

        # rotate 및 crop 수행
        rotated_img = rotate(np.array(img), get_angle(np.array(img)))
        cropped_img = Image.fromarray(rotated_img).crop(manuscript_box)

        img_bytes = BytesIO()
        cropped_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        img_doc = fitz.open("pdf", fitz.open(stream=img_bytes.read(), filetype="png").convert_to_pdf())
        preprocessed_images.append(img_doc)

    output_pdf = fitz.open()
    for img_pdf in preprocessed_images:
        output_pdf.insert_pdf(img_pdf)

    output_pdf.save(output_path)
    output_pdf.close()