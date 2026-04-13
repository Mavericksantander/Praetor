FROM python:3.11-slim as base
ARG WHEEL_DIR=/wheels
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Expect wheels precargados (air-gapped)
COPY wheels/ ${WHEEL_DIR}/
COPY requirements.offline.txt /tmp/requirements.offline.txt
RUN python -m venv ${VIRTUAL_ENV} \
    && pip install --no-index --find-links=${WHEEL_DIR} -r /tmp/requirements.offline.txt

FROM python:3.11-slim
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
WORKDIR /app
COPY . /app

EXPOSE 8000
ENTRYPOINT ["uvicorn", "praetor_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
