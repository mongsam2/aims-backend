INSERT INTO student_record_evaluation_category(id, category_name)
VALUES 
(1, "2024 학생부 평가 기준"),
(2, "2025 학생부 평가 기준");

INSERT INTO student_record_evaluation_question(title, description, category_id)
VALUES 
("학업 역량", "전체적인 교과 관련 성취수준 및 학업 발전 정도", 1),
("진로 역량", "지원 전공에 필요한 과목을 선택하여 이수한 정도", 1),
("창의적 문제 해결 역량", "문제 해결을 위한 창의적·적극적 노력과 경험", 1),
("공동체 역량", "나눔, 배려, 타인을 존중하는 태도와 경험", 1);
