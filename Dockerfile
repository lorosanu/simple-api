FROM python:3.10-slim

# requires the wheel
COPY dist/*.whl .

RUN python -m pip install -U pip && pip install *.whl && rm -f *.whl

EXPOSE 8080

CMD [ "simple_api" ]