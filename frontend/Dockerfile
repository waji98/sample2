# backend/Dockerfile

FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y build-essential

# Set the CXX environment variable
ENV CXX=g++

# Install gendoc
RUN pip install gendoc==1.0.1

# Use an official Python runtime as a parent image

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
