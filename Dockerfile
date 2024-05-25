FROM python:latest
WORKDIR /code
ENV DB="localhost:27017"
ENV TG="none"
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "SalarySplitterMain.py"]