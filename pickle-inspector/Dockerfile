# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Create a non-root user and set the working directory
RUN useradd -m user
USER user
WORKDIR /home/user

# Copy the Python inspection script
COPY inspect.py .

# Define the entrypoint to run the script
ENTRYPOINT ["python", "inspect.py", "pickles/suspect.pkl"]
