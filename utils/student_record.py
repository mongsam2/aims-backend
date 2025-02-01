from .upstage import get_answer_from_solar
from django.conf import settings
import asyncio
import os

async def summarization_content(student_record, extraction, api_key):

        prompt_file = os.path.join(settings.BASE_DIR, 'prompts', 'summarization.txt')  
        
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
        
        response = get_answer_from_solar(api_key, extraction, prompt_content)

        await response

        student_record.summarization.content = response
        student_record.summarization.save()

        return response

async def summarization_question(student_record, extraction, api_key):

    prompt_file = os.path.join(settings.BASE_DIR, 'prompt', 'question.txt')  
    with open(prompt_file, 'r', encoding='utf-8') as file:
        prompt_content = file.read()

    response = get_answer_from_solar(api_key, extraction, prompt_content)

    await response

    student_record.summarization.question = response
    student_record.summarization.save()

    return response