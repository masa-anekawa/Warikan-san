# ---- Build Stage ----
FROM public.ecr.aws/lambda/python:3.11 as builder

# Set the working directory
WORKDIR /var/task

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /var/task/

# Install pipenv, generate requirements.txt, and install dependencies
RUN pip install pipenv && \
  pipenv install --system --extra-pip-args '--target ./package'

# ---- Final Stage ----
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory
WORKDIR /var/task

# Copy python dependencies from the builder stage
COPY --from=builder /var/task/package /var/task/package

# Set PYTHONPATH to the directory containing the dependencies
ENV PYTHONPATH=/var/task/package

# Copy the lambda handler code and the model files
COPY ./src /var/task/src
COPY ./models /var/task/models

# Set the CMD to your handler
CMD [ "src.lambda_handler.lambda_handler" ]
