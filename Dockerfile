FROM python:3.11-slim

# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# requirements.txt만 복사
COPY psc/requirements.txt ./requirements.txt

# 소스 코드만 복사
COPY psc /app/psc

EXPOSE 8000

CMD ["uvicorn", "psc.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
