
FROM public.ecr.aws/lambda/python:3.8

# Install pandas
RUN pip install pandas

# Copy the lambda function
COPY lambda_function.py /var/task/

CMD ["lambda_function.lambda_handler"]
