# ---- Build Stage ----
FROM public.ecr.aws/lambda/python:3.11 as builder

# Set the working directory
WORKDIR /var/task

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /var/task/

# Install pipenv, generate requirements.txt, and install dependencies
RUN pip install pipenv && \
  pipenv install --system

# Copy the lambda handler code and the model files
COPY ./src /var/task/src

# Set the CMD to your handler
CMD [ "src.lambda_function.lambda_handler" ]
