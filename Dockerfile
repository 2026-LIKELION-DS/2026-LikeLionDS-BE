# 베이스 이미지로 Python 3.12 사용
FROM python:3.12-slim

# 컨테이너 내에서 작업할 디렉토리 설정
WORKDIR /reqruitment

# 필요 파일들을 복사
COPY requirements.txt .

# 필요한 Linux 패키지 설치 및 의존성 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    libmariadb-dev && \
    apt-get clean

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --upgrade pip

# Python 라이브러리 설치
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*

# 프로젝트의 소스 코드 복사
COPY ./reqruitment /reqruitment

ENV DJANGO_SETTINGS_MODULE=reqruitment.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY_FILE=/reqruitment/secret_key.json

# 컨테이너 실행 시 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
