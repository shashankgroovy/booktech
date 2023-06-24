FROM python:3.10-buster

# Switch directory
WORKDIR /app

# Install the requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY . .

# There is no CMD or ENTRYPOINT since booktech can be invoked from outside.
# And it's a wrap!
