import os

from django.conf import settings
from rest_framework.exceptions import APIException

from .upstage import get_answer_from_solar


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