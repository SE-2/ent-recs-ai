# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

COPY datasets /app/

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the Flask application
CMD [ "python", "app.py" ]
