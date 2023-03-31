FROM python
LABEL maintainer="NymV"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV TOKEN =
ENV API_KEY =
CMD ["python3","chat.py"]