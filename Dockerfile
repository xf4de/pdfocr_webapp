FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
COPY . /pdfocr
WORKDIR /pdfocr
RUN apt update && apt install -y curl iputils-ping poppler-utils tesseract-ocr tesseract-ocr-ita tesseract-ocr-eng && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
EXPOSE 5000
STOPSIGNAL SIGKILL
ENTRYPOINT [ "./run.sh" ]
