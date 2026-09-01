#Use lght weight python image
FROM python:3.14-slim
#set working container directory
WORKDIR /app
#Installing the package manger UV
RUN pip install --no-cache-dir uv
#Copy dependecy files
#Allowing Docker to cache dependency-installation layer
COPY pyproject.toml uv.lock ./
#Install project dependncy's
RUN uv sync --frozen

#Copy source code intocontainer
COPY src ./src

#Mentioned the python application lives that is the path of code
ENV  PYTHONPATH=/app/src

#Port
EXPOSE 8000

#Start the FastAPI application
CMD ["uv","run","uvicorn","url_designer.main:app","--host","0.0.0.0","--port","8000"]