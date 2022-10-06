FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/
#COPY ./requirements/ /app/requirements

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then  pip install -r requirements/requirements-code-quality.txt && poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

RUN pip install avionix
RUN pip install kubernetes
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
RUN chmod +x get_helm.sh
RUN ./get_helm.sh

COPY ./app /app/app
COPY ./odoo_operator /app/odoo_operator
COPY odoo_operator/mychart /app/mychart
COPY ./run_server.py /app/run_server.py

COPY ./gunicorn_conf.py /app/gunicorn_conf.py

COPY ./start_script.sh /app/start_script.sh

ENV PYTHONPATH=/app

RUN chmod 755 ./start_script.sh
CMD ["./start_script.sh"]


