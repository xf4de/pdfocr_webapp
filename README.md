# pdfocr_webapp
simple webapp to extract text from pdf scans

```
docker build -t pdfocr:1 .
docker run --rm -p 127.0.0.1:5000:5000 -d --name pdfocr pdfocr:1
```
