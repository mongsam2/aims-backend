import os
import torch

from torchvision import models

from django.conf import settings

from PIL import Image

from torchvision import transforms
from pdf2image import convert_from_path
from .upstage import get_answer_from_solar

from students.models import Student

from datetime import datetime


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


def predict_document_type(file_path, class_labels=["검정고시합격증명서", "국민체력100", "기초생활수급자증명서", "주민등록초본", "체력평가", "생활기록부대체양식"]):
    
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


def assign_student_id_and_document_type(content):
    """
    Extraction 테이블에 값이 저장되면 Signal이 트리거됨.
    
    1. OCR에서 추출한 학생 이름을 기반으로 Student ID 할당
    2. ValidationCriteria에서 문서 유형을 찾아 DocumentType 테이블에서 검색 후 Documentation에 설정
    """
    api_key = settings.UPSTAGE_API_KEY

    prompt = '''넌 OCR로 입시 서류에서 추출한 텍스트를 읽고 지원자의 이름, 
    즉 이 서류를 제출한 사람의 이름이 누구인지 유추하는 <제출자 이름 추출기야>. 
    서류 주인의 이름(지원자 이름)을 문자열로 첫 번째에, 발행일자를 "YYYY-MM-DD" 형식 문자열로 두 번째에 반환해.
    반환 형식 예: "홍길동, 2022-01-01", "송재현, 2022-01-00".
    주의해야할 점: 1.서류 주인의 이름은 보통 한글로 된 세 글자 이름이야. 그리고 "성명: 홍길동" "지원자: 송재현" 이런 식으로 입력 텍스트에 들어있을 거야.
    2. 보통 한국 사람의 이름으로는 "송재현", "김민성", "강민지", "이종원", "윤현주", "송가은" 이런 세 글자로 되어있어.
    3. 너는 반드시 보통의 한국 사람 이름의 형식으로 반환해야 돼. "/", "", "김", "송", "차", "*" 이런 식으로 이름을 찾아서는 안돼'''
    answer = get_answer_from_solar(api_key, content, prompt)

    answer_list = list(answer.split(", "))

    extracted_names = answer_list[0].rstrip()
    date = answer_list[1].rstrip()

    student = Student.objects.filter(name__icontains=extracted_names).first()
    if student:
        return student.id, date, extracted_names
    else:
        return "20250000", date, extracted_names

def is_date_valid(date_str):
    """
    입력된 날짜가 기준 날짜보다 이전이면 False, 이후 또는 같으면 True 반환

    Args:
        date_str (str): YYYY-MM-DD 형식의 날짜 문자열

    Returns:
        bool: 유효성 검사 결과
    """
    reference_date = datetime.strptime(settings.VALID_DATE, "%Y-%m-%d")
    
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d")
        return input_date >= reference_date

    except ValueError:
        print("잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력하세요.")
        return False