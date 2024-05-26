# - CHANGE TO MULTI-STAGE BUILD
#This Dockerfile is uses a multi-stage build to create a 
#lightweight image with the application code and dependencies. 
#The first stage installs the dependencies and the 
#second stage copies the application code. 
#This approach is recommended for production 
#environments as it reduces the image size and improves security
#by not including unnecessary files.



# pull official base image
FROM python:3.11.2-slim

# Patch security updates & bug fixes 
RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Remove root-level-access by creating a regular user
RUN useradd --create-home united
USER united
WORKDIR  /Users/frederico/stripe_checkout_single_subscription/checkout-single-subscription

# Create and activate a virtual environment within image
# https://realpython.com/docker-continuous-integration/#isolate-your-docker-image
ENV VIRTUALENV=/Users/frederico/stripe_checkout_single_subscription/checkout-single-subscription/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

# Copy requirements file & change onwership to regular user
COPY --chown=united requirements.txt ./

# Copy server.py & change ownership to regular user
COPY --chown=united server.py ./

# Copy the app code & change ownership to regular user
COPY --chown=united app ./app

COPY --chown=united config.py ./

# Upgrade pip and setuptools
# Install dependencies
# --no-chache-dir: Avoids caching the downloaded packages
RUN python -m pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# NOTE: Dependencies were installed before installing the
# app code in the Docker Image. They will stay in a chached layer
# Any changes to source code will not require re-installing dependencies

CMD ["python", "server.py", \
    "--host", "0.0.0.0", "--port", "8080"]