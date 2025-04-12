
# Firebase Admin SDK 연동 예시
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Firebase 초기화
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # 서비스 계정 키 경로
firebase_admin.initialize_app(cred)

# Firestore DB 접근
db = firestore.client()

# 사용자 등록 (보호자 + 자녀 정보)
def register_user(parent_email, password, child_name, child_age):
    try:
        # Firebase Auth 사용자 생성
        user = auth.create_user(
            email=parent_email,
            password=password
        )
        
        # Firestore에 사용자 정보 저장
        db.collection("parents").document(user.uid).set({
            "email": parent_email,
            "child_name": child_name,
            "child_age": child_age,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return f"{child_name}의 보호자 계정이 등록되었습니다."
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 감정 기록 저장
def save_emotion(child_id, emotion, reason=None):
    db.collection("emotions").add({
        "child_id": child_id,
        "emotion": emotion,
        "reason": reason,
        "date": firestore.SERVER_TIMESTAMP
    })

# 퀴즈 기록 저장
def save_quiz_result(child_id, question_id, selected_option, is_correct):
    db.collection("quiz_results").add({
        "child_id": child_id,
        "question_id": question_id,
        "selected_option": selected_option,
        "is_correct": is_correct,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
