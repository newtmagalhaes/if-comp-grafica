FROM python:3.12

WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src
COPY projeto.py .

ENTRYPOINT [ "python" ]
CMD [ "projeto.py" ]
