FROM python:3.11-alpine

WORKDIR /usr/qa_cloud_camp

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD pytest -s -v tests/*


