FROM python:3.10.13

# Set the working directory in the container. /app is independent of workspace folder name
WORKDIR /app 

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Download the 'punkt' tokenizer data
RUN python -c "import nltk; nltk.download('punkt')"

# Run the Python application
CMD ["python", "main.py"]