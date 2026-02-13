
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN useradd -m -u 1000 user

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app


COPY --chown=user requirements.txt requirements.txt


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV NLTK_DATA=$HOME/nltk_data
RUN python3 -m nltk.downloader -d $NLTK_DATA punkt vader_lexicon


COPY --chown=user ./app ./app


EXPOSE 7860


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
