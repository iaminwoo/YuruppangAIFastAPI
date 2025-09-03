# 베이스 이미지: Python 3.12 Slim
FROM python:3.12-slim

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 전체 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
