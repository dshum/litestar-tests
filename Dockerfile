# build stage
FROM python:3.12-bookworm AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /app/
COPY src/ /app/src

# install dependencies and project into the local packages directory
WORKDIR /app
RUN mkdir __pypackages__ && pdm sync --prod --no-editable


# run stage
FROM python:3.12-bookworm

# retrieve packages from build stage
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.12/lib /app/pkgs

# retrieve executables
COPY --from=builder /app/__pypackages__/3.12/bin/* /bin/

WORKDIR /app/src

# set command/entrypoint, adapt to fit your needs
# CMD ["python", "-m", "project"]