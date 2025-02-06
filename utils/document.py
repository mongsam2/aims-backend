import os
import torch

from torchvision import models

from django.conf import settings

from PIL import Image

from torchvision import transforms
from pdf2image import convert_from_path

import re


MODEL_DIR = os.path.join(settings.BASE_DIR, "parameters")


def load_model(model_name="student_model.pth"):

    model_path = os.path.join(MODEL_DIR, model_name)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 가중치 파일이 존재하지 않습니다: {model_path}")

    model = models.mobilenet_v3_small(weights=None)
    model.classifier[3] = torch.nn.Linear(1024, 6)

    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    print(f"model load completed: {model_path}")

    return model


def predict_document_type(file_path, class_labels=["검정고시합격증명서", "국민체력100인증서", "기초생활수급자증명서", "주민등록초본", "체력평가", "생활기록부대체양식"]):
    
    model = load_model()
    model.eval()

    image = preprocess_image(file_path)
    
    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()

    predicted_label = class_labels[predicted_class]
    confidence = probabilities[0][predicted_class].item()
    
    return predicted_label, confidence


def pdf_to_image(pdf_path, output_folder="/tmp", dpi=300):
    """
    PDF 파일을 이미지로 변환하여 첫 번째 페이지를 반환
    
    Args:
        pdf_path (str): 변환할 PDF 파일 경로
        output_folder (str): 변환된 이미지 저장 경로 (기본값: /tmp)
        dpi (int): 변환 시 해상도 설정 (기본값: 300)
    
    Returns:
        image_path (str): 변환된 첫 번째 페이지 이미지 경로
    """
    os.makedirs(output_folder, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=dpi, output_folder=output_folder, fmt="png", first_page=1, last_page=1)
    if not images:
        raise ValueError("PDF 변환 실패!")

    saved_images = [f for f in os.listdir(output_folder) if f.endswith(".png")]
    saved_images.sort()

    if not saved_images:
        raise ValueError("변환된 이미지 파일이 존재하지 않습니다!")

    image_path = os.path.join(output_folder, saved_images[0])

    return image_path


def preprocess_image(file_path):
    """
    파일 경로를 입력받아 이미지 전처리를 수행하는 함수.
    PDF 파일이 입력되면 먼저 이미지로 변환 후 처리함.

    Args:
        file_path (str): 이미지 또는 PDF 파일 경로

    Returns:
        torch.Tensor: 전처리된 이미지 텐서
    """
    
    if file_path.lower().endswith(".pdf"):
        file_path = pdf_to_image(file_path)

    image = Image.open(file_path).convert("RGB")

    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = transform(image).unsqueeze(0)

    os.remove(file_path)
    print(f"🗑️ 변환된 이미지 삭제 완료: {file_path}")

    return image

def extract_student_number(content):
    """
    입력된 문자열에서 '수험번호' 패턴 이후의 8자리 숫자를 찾아 반환하는 함수.
    """
    
    patterns = [
        r"(수\s?험\s?번\s?호\s?)?(\d{8})",
        r"(\d{8})"
    ]

    nums = []

    for pattern in patterns:
        matches = re.findall(pattern, content)
        nums.extend(matches)
    nums = list(set(nums))
    if nums:
        return nums[0]
    else:
        return "20250000"