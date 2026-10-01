# MULTI-STAGE Docker

# gcc g++ && rm -rf /var/lib/apt/lists/*

# Stage 1: create virtual machine, virtual env, activate it and install the project
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir . pytest

# Stage 2: create tester stage from the builder, inheriting everything inside, then test the data validation pipeline (test will run on custom df, not on real data)
FROM builder AS tester

COPY tests ./tests
RUN PYTHONPATH=/build/src python -m pytest tests/ -q --tb=short
# here the code would break if the tests fail, so the build would fail too

# Stage 3: crete clean runtime image, keep only the runtime environment and application code, discard build tools and test code to reduce image size
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

# Docker default runs processes as root, which is a security risk. Create a non-root appuser to run the application.
RUN useradd --create-home --uid 1000 appuser

# Recreate environment as in the tester stage
COPY --from=tester /opt/venv /opt/venv

# Copy the application code and model file from the builder stage to the runtime stage, setting ownership to appuser
# Notice that we want the appuser to read-only models and source code, while potentially modifying data and logs
COPY src ./src
COPY models ./models

# Data are automatically created by the application, logs are made by running it, no need to copy files from machine
RUN mkdir -p /app/data /app/logs \
    && chown -R appuser:appuser /app/data /app/logs

# Set env variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1

# Set the user to appuser for security reasons
USER appuser

# Start ML Pipeline
CMD ["python", "src/ML_pipeline.py"]

# In case of webservers, uncomment to expose the port and run the server (could be here for docu and in compose for actual port mapping)
# EXPOSE 8080
# CMD ["uvicorn", "app.main:app", " -- host", "e.e.e.e", " -- port", "8860"]