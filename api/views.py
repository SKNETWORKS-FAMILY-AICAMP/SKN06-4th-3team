from django.contrib.auth.decorators import login_required  # 로그인 확인 추가
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_GET
from .llm import Chatting, add_message_to_history

@login_required  # 로그인한 사용자만 접근 가능하게 설정
@require_GET
def chat_message(request, message):
    """
    대화를 수행하는 API 엔드포인트.
    path parameter로 사용자의 메시지를 받아서 AI의 응답을 반환한다.
    각 사용자별로 대화 기록을 저장하도록 수정한다.
    """
    chat = Chatting()
    
    user_id = str(request.user.id)  # 사용자 ID 기반으로 저장
    history_key = f"chatting_history_{user_id}"  # 사용자별 history 키 생성

    # session에서 해당 사용자의 대화내역(history) 불러오기. (없으면 빈 배열 반환.)
    history = request.session.get(history_key, [])

    # llm에게 메시지 전송
    response = chat.send_message(message, history)

    # history에 message, response 저장 (max_length가 넘으면 오래된 순으로 삭제)
    add_message_to_history(history, ("human", message))
    add_message_to_history(history, ("ai", response))

    # session에 변경된 대화내역 업데이트
    request.session[history_key] = history

    return JsonResponse({'response': response})

@login_required
@require_GET
def chat_history(request):
    """
    사용자의 대화 기록을 불러오는 API
    """
    user_id = str(request.user.id)
    history_key = f"chatting_history_{user_id}"
    history = request.session.get(history_key, [])
    
    return JsonResponse({'history': history})
