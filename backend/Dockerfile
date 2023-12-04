# backend/Dockerfile

FROM python:3.10-slim-buster

# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y build-essential

# Set the CXX environment variable
ENV CXX=g++

# Install gendoc
RUN pip install gendoc==1.0.1


# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV FLASK_APP app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

