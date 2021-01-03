FROM python:3.8.1-slim-buster

# Install Python dependencies
RUN pip install rq-dashboard

ENTRYPOINT ["/bin/bash", "-c", "rq-dashboard -H redis"]