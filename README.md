# gce-cloud-postgresql-demo
![image](https://user-images.githubusercontent.com/77932366/184716028-b883dc68-ce6f-4cc5-b2ba-2b64294a5ae2.png)

## Introduction

This repository targets junior data engineers/developers who are interested in deploying a Python script into the cloud with the use of Docker & Google Cloud Platform (GCP). 

The sample script used for this demo performs reading a .csv file, creating a table in a SQL database & uploads the data into the created table.

For this demo Docker, Google Container Registry & Google Compute Engine is used. These two services are offering an easy deployment of the containerized Python script.

Note that Google offers a Free Trial. After the Free Trial period some GCP services are free of charge, within specified monthly usage limits:(https://cloud.google.com/free/docs/free-cloud-features)

## Prerequisites

- Ubuntu (WSL) is used for development
- Docker on Ubuntu (https://docs.docker.com/engine/install/ubuntu/)
- Python (https://www.python.org/downloads/) | (https://www.python.org/downloads/windows/)
- Access to use GCP services as 'Owner' (Full Account/Free Trial)
- Cloud Postgresql database (https://cloud.google.com/sql/docs/postgres/create-instance)
- gcloud CLI (https://cloud.google.com/sdk/docs/install)
- Local directory where Python script, dataset, Dockerfile & service account key file is located

## Get started
Google offers a detailed documentation & it is recommended to read the resources provided. In this case, the following documentation can be useful for the development process:
- Connect to PostgreSQL (https://cloud.google.com/sql/docs/postgres/connect-overview) - Useful to validate if data upload working e.g. with WebUI pgAdmin
- Container Registry (https://cloud.google.com/container-registry/docs/using-with-google-cloud-platform), (https://cloud.google.com/container-registry/docs/access-control), (https://cloud.google.com/container-registry/docs/advanced-authentication#linux-macos_1)
- GCP project (https://cloud.google.com/resource-manager/docs/creating-managing-projects)
- Google service accounts (https://cloud.google.com/iam/docs/service-accounts)
- Pushing & pulling images (https://cloud.google.com/container-registry/docs/pushing-and-pulling)

### Set up GCP project & create service account + service account key
GCP (console.cloud.google.com)
1. Create project (https://cloud.google.com/resource-manager/docs/creating-managing-projects#console)
2. Create service account (https://cloud.google.com/iam/docs/creating-managing-service-accounts)
3. Generate & download .json keyfile (https://cloud.google.com/iam/docs/creating-managing-service-account-keys)

### Push first image to Container Registry & configure permissions
The first image push to a hostname, e.g. eu.gcr.io, triggers the creation of the registry. After that, permissions can be configured to push local images. 
Open Google Cloud Shell in GCP project:

![image](https://user-images.githubusercontent.com/77932366/184651692-53952991-363b-4eee-8899-575f23985061.png)

Execute the follwing commands to push first image to Container Registry:
```python
docker pull busybox
docker tag busybox gcr.io/my-project/busybox
docker push gcr.io/my-project/busybox
```
Note that a Cloud Storage bucket got created.

![image](https://user-images.githubusercontent.com/77932366/184652471-4ac36ed7-a2d7-4261-9153-54c942d8a394.png)

### Add permissions for service account to Cloud Storage bucket
In order to push an image the 'Storage Admin' & 'Storage Legacy Bucket Writer' permission need to be assigned to the service account.

![image](https://user-images.githubusercontent.com/77932366/184664814-b50e3b3d-5a51-43da-86de-0484d99c0d42.png)

![image](https://user-images.githubusercontent.com/77932366/184665496-d12398c2-c1ef-4e12-bed0-836510fa7252.png)

## Build image locally & push to Container Registry
### Build Docker image

```python
docker build -t eu.gcr.io/sns-kafka-gcp/pyapp:v001 .
```

### Activate service account in gcloud CLI & Log into Docker with .json keyfile
1. Navigate to local directory where files are stored
2. Open terminal & execute the following commands
```python
gcloud auth list
```
The output should display the currently logged in account.

3. Switch to service account & configure Docker
```python
gcloud auth activate-service-account ACCOUNT --key-file=KEY-FILE
# gcloud auth activate-service-account saccount-sns-kafka-gcp@sns-kafka-gcp.iam.gserviceaccount.com --key-file=./sns-kafka-gcp-aa1cecbe96ab.json

gcloud auth configure-docker
```
4. Authenticate with Docker

The hostname is either 'gcr.io, us.gcr.io, eu.gcr.io, or asia.gcr.io'
```python
docker login -u _json_key -p "$(cat keyfile.json)" https://HOSTNAME
# cat sns-kafka-gcp-aa1cecbe96ab.json | docker login -u _json_key --password-stdin https://eu.gcr.io
```

### Push built image to Container Registry
```python
docker push eu.gcr.io/sns-kafka-gcp/pyapp:v001
```

### Deploy image to Google Compute Engine (use service account in configuration of VM)
An easy & convenient way to run a python script in GCP is to use Google Compute Engine. Basically this approach hosts the python script on a virtual computer & executes the scipt as soons as it turns on.

To schedule the scipt e.g. to run daily there is an option to schedule the instance (https://cloud.google.com/compute/docs/instances/schedule-instance-start-stop).

![image](https://user-images.githubusercontent.com/77932366/185045337-8a1ceac1-9dfa-4cbd-900d-e0da808210e0.png)

## Dockerfile & script.py
### Dockerfile
The Dockerfile executes the following command-line instructions:
```python
FROM python:3.8-bullseye # Pull python image

RUN apt update -y # Execute apt update command, using -y to prevent the execution to be stuck
RUN apt install -y python3-pip # Install pip for python packages

RUN pip3 install pandas # For reading .csv file & create pandas dataframe
RUN pip3 install psycopg2 # For set connection to Postgresql database
RUN pip3 install sqlalchemy # For creating engine to insert data into Postgresql database table

WORKDIR /app # Directory in the container

ADD script.py /app # Copy python script to container directory
ADD data.csv /app # Copy .csv file to container directory

CMD ["python3", "./script.py"] # Specifies what command to run within the container
```

### script.py
The sample python script performs:
1. Import necessary python packages
2. Establish connection to Postgresql database
3. Create table with given schema
4. Read .csv file & convert to pandas dataframe
5. Insert data into created table
