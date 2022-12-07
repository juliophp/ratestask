FROM  postgres:12
COPY rates.sql /docker-entrypoint-initdb.d/
ADD rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
ENV POSTGRES_PASSWORD=ratestask


FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["base.py"]
