# gce-cloud-postgresql-demo
![image](https://user-images.githubusercontent.com/77932366/184556016-d989511f-28f5-4e45-ad1b-65fa3eb5f2ed.png)

## Introduction

This repository targets junior data engineers/developers who are interested in deploying a Python script into the cloud with the use of Docker & Google Cloud Platform (GCP). 

The sample script used for this demo performs reading a .csv file, creating a table in a SQL database & uploads the data into the created table.

For this demo Docker, Google Container Registry & Google Compute Engine is used. These two services are offering an easy deployment of the containerized Python script.

Note that Google offers a Free Trial. After the Free Trial period some GCP services are free of charge, within specified monthly usage limits:(https://cloud.google.com/free/docs/free-cloud-features)

## Prerequisites

- Ubuntu (WSL) is used for development
- Python (https://www.python.org/downloads/) | (https://www.python.org/downloads/windows/)
- Docker on Ubuntu (https://docs.docker.com/engine/install/ubuntu/)
- Access to use GCP services as 'Owner' (Full Account/Free Trial)
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
```
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
### gcloud CLI & log in Docker with .json keyfile
