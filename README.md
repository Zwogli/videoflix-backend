# Videoflix-backend

## Table of contents
- [Introduction](#Introduction)
- [Technologies](#Technologies)
- [Utilisation](#Utilisation)
- [1. Decision making](#1-Decision-making)
- [2. Main function](#2-Main-function)
- [3. Deployment](#3-Deployment)

## Introduction

Videoflix is a backend for a Netflix clone that offers full registration, validation and verification. Users can watch global videos and upload their own videos to their account. Python and Django were used for the implementation.

## Technologies

-   **Python**: Main programming language.
-   **Django**: Web framework for developing the backend.
-   **Django REST Framework**: For creating RESTful APIs.
-   **PostgreSQL**: Relational database for data storage.
-   **Redis**: In-memory data structure store for caching.
-   **FFmpeg**: Tool for video conversion.

## Utilisation

The API offers various endpoints for interacting with the backend. Here are some examples:

-   Registration: POST /api/register/
-   Login: POST /api/login/
-   Retrieve videos: GET /api/global-videos/
-   Upload video: POST /api/local-videos/

## 1. Decision making

In the first phase, I conceptualised the project and considered how I could divide up the various tasks. The decision to implement authentication first was based on my previous experience with login processes.

## 2. Main function

The main functions of the project include

-   Video model: Model for storing videos.
-   Video conversion: Conversion of videos into different formats.
-   Backend processing: Background processing of uploads and conversions.
-   Thumbnail creation: Automatic generation of thumbnails when uploading.
-   Deletion of files: Cleaning up all files of a video.

## 3. Deployment

The backend was deployed on a Google Cloud VM with Ubuntu. Here are some steps I followed:

1. **Server configuration**: Installation and configuration of NGINX to deploy the API.
2. **Database**: Setup of PostgreSQL and migration of the database.
3. **Redis**: Configuration of Redis for caching and background processing.
4. **Gunicorn**: Installation of Gunicorn as WSGI HTTP server to run the Django application.
5. **Supervisor**: Installation of Supervisor to monitor and manage the Gunicorn process to ensure that the application is always available.
6. **Security**: Setting up environment variables and access control.
