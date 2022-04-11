#FROM python:3.9.2
#
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /Nav_App
#
#COPY . /Nav_App
#
#COPY ./requirements.txt /Nav_App/requirements.txt
#
#RUN pip install -r requirements.txt
#
#COPY . /Nav_App
#
#RUN mkdir ../static; exit 0
#
#RUN mkdir ../media; exit 0
#
#COPY ./static/ ../static
#
#RUN rm -rf ./static
FROM python:3.9.10 as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Now multistage builds
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
