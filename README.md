# Videoflix-backend

## Table of contents

-   [Introduction](#Introduction)
-   [Technologies](#Technologies)
-   [Utilisation](#Utilisation)
-   [Configuration](#Configuration)
-   [Testing](#Testing)
-   [1. Decision making](#1-Decision-making)
-   [2. Main function](#2-Main-function)
-   [3. Deployment](#3-Deployment)

## Introduction

Videoflix is a backend for a Netflix clone that offers full registration, validation and verification. Users can watch global videos and upload their own videos to their account. Python and Django were used for the implementation.

## Technologies

<details>

<summary>List of technologies:</summary>
<br>

-   **Python**: Main programming language.
-   **Django**: Web framework for developing the backend.
-   **Django REST Framework**: For creating RESTful APIs.
-   **PostgreSQL**: Relational database for data storage.
-   **Redis**: In-memory data structure store for caching.
-   **FFmpeg**: Tool for video conversion.

</details>

## Utilisation

<details>

<summary>The API offers various endpoints for interacting with the backend. Here are some examples:</summary>
<br>

-   Registration: POST /api/register/
-   Login: POST /api/login/
-   Retrieve videos: GET /api/global-videos/
-   Upload video: POST /api/local-videos/

</details>

## Configuration

Sensitive information such as passwords and API keys are stored in a separate configuration file (`videoflix/config.py`), which is listed in the `.gitignore` file to prevent it from being committed to version control. For enhanced security, it is recommended to use environment variables or a dedicated secrets management service.

### Example of Environment Variables

Instead of hardcoding sensitive information, you can set environment variables like this:

In your `videoflix/config.py`:
```bash
SECRET_KEY = 'your_SECRET_KEY'

DATABASE_USER = 'your_DATABASE_USER'
DATABASE_PASSWORD = 'your_DATABASE_PASSWORD'

EMAIL_HOST = 'your_EMAIL_HOST'
EMAIL_HOST_USER = 'your_EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'your_EMAIL_HOST_PASSWORD'
```

## Testing

To ensure the reliability and stability of the application, tests have been written using **pytest**. These tests cover various functionalities of the API, including user registration, video uploads, and data retrieval. To run the tests, use the following command:

```bash
pytest
```

## 1. Decision making

In the first phase, I conceptualised the project and considered how I could divide up the various tasks. The decision to implement authentication first was based on my previous experience with login processes.

## 2. Main function

The main functions of the project include:
<br>

-   Video model: Model for storing videos.
-   Video conversion: Conversion of videos into different formats.
-   Backend processing: Background processing of uploads and conversions.
-   Thumbnail creation: Automatic generation of thumbnails when uploading.
-   Deletion of files: Cleaning up all files of a video.

## 3. Deployment

<details>
<summary>The backend was deployed on a Google Cloud VM with Ubuntu. Here are some steps I followed:</summary>
<br>

-   **Server configuration**: Installation and configuration of NGINX to deploy the API.
-   **Database**: Setup of PostgreSQL and migration of the database.
-   **Redis**: Configuration of Redis for caching and background processing.
-   **Gunicorn**: Installation of Gunicorn as WSGI HTTP server to run the Django application.
-   **Supervisor**: Installation of Supervisor to monitor and manage the Gunicorn process to ensure that the application is always available.
-   **Security**: Setting up environment variables and access control.

</details>
