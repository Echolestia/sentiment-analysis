# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install Cython before installing your packages. It can be included in the Dockerfile like so:
RUN pip install Cython
RUN pip install -r requirements.txt


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app