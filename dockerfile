FROM python:3.9-slim

WORKDIR . /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg libsm6 libxext6 \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY Dash_testV1.py /app/
COPY DonneeAbdNettoyeeAvecDate.csv /app/

COPY requirements.txt /app/
COPY Logo_Meaux.svg /app/

WORKDIR /app
RUN pip install -r requirements.txt

# RUN python -m spacy download fr_core_news_sm

EXPOSE 8050

# HEALTHCHECK CMD curl --fail http://localhost:8050/_stcore/health
ENTRYPOINT ["python", "-m", "Dash_testV1", "--server.port=8050", "--server.address=0.0.0.0"]