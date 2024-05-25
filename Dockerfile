FROM python:latest
WORKDIR /code
ARG TG
ENV DB="localhost:8010"
ENV TG $TG
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "SalarySplitterMain.py"]