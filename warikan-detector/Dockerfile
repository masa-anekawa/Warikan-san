FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies and the app itself
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the content of the local src directory to the working directory
COPY ./src/ /app/src/

# Specify the command to run on container start
CMD [ "pipenv", "run", "python", "src/model_process.py" ]
