FROM python:3.9.10 as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +


FROM python:3.9.10

COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8000

COPY . /code/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
