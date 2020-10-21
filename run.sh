#!/bin/bash
#. venv/bin/activate
gunicorn -b 0.0.0.0:5000 "pdfocr:create_app()" --access-logfile - --error-logfile - --timeout 300 -w 2 --threads=2
 
