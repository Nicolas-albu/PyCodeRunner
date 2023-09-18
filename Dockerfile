FROM python

ENV PYTHON_VERSION 3.10.10

WORKDIR /PyCodeRunner

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /PyCodeRunner/pycoderunner

COPY /pycoderunner .

EXPOSE 8000

WORKDIR /PyCodeRunner

CMD ["uvicorn", "pycoderunner.main:app", "--host", "0.0.0.0", "--port", "80"]