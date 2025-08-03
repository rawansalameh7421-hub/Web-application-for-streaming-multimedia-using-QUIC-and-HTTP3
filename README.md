-----

# Secure Video Streaming Web App with JWT Authentication and HLS

This project is a secure web application that allows users to register, log in, and stream HLS (HTTP Live Streaming) video content. It uses JWT-based authentication, stores user data in a permanent SQLite database with hashed passwords, and delivers video content using HTTP/3 (QUIC) via the Quart framework and Hypercorn server.

-----

## Features

  - User registration and login with secure password hashing (bcrypt).
  - JWT token issuance and validation for secure access to protected content.
  - Video playback using HLS.js with quality selection.
  - Animated HTML UI for login, signup, and playback.
  - HTTP/3 & QUIC support via Hypercorn + TLS.

-----

## Project Structure

```
project/
├── DB.py                # Database functions (SQLite + bcrypt)
├── Server_DB.py         # Quart backend server
├── player1.html         # HTML frontend for login/register & video player
├── cert.crt             # TLS certificate (for HTTPS/QUIC)
├── key.pem              # TLS private key
├── video/               # (Optional) Raw video uploads
└── hls_output/          # HLS files served to the player (.m3u8 and .ts files)
```

-----

## Technologies Used

  - **Python**: Backend logic
  - **Quart**: Async web framework
  - **Hypercorn**: ASGI server with QUIC support
  - **JWT (PyJWT)**: Authentication tokens
  - **bcrypt**: Secure password hashing
  - **SQLite**: Lightweight local database
  - **HTML5 + JavaScript**: User interface
  - **HLS.js**: Video streaming player
  - **TLS/HTTPS**: Encrypted traffic using `cert.pem` and `key.pem`

-----

## Installation & Running

### 1\. Prerequisites

  - Python 3.9+
  - pip (Python package installer)
  - TLS certificate and key (`cert.crt` and `key.pem`)
  - HLS-encoded videos in the `hls_output/` directory

### 2\. Install Dependencies

```bash
pip install quart hypercorn pyjwt bcrypt
```

### 3\. Run the Server

```bash
python Server_DB.py
```

The server will run on:
`https://localhost:4433` (with HTTP/3 support)

> **Note:** Make sure you have `cert.crt` and `key.pem` in the same folder for HTTPS/QUIC to work.

### 4\. Open the App

Navigate to the following URL in your browser:

```
https://localhost:4433/player1.html
```

> You may need to accept the browser's security warning if you are using a self-signed certificate.

-----

## Authentication Workflow

  - **Register**: `POST /register` → Stores the user with a hashed password in the database.
  - **Login**: `POST /login` → Returns a JWT token upon successful authentication.
  - **Access HLS Videos**: `GET /hls/*.m3u8` or `*.ts` → Requires a valid `Authorization: Bearer <token>` header in the request.

-----

## Video Playback

The `player1.html` file provides a responsive interface with animated login/signup forms and a built-in HLS video player. Upon successful login, the app dynamically switches to playback mode, offering quality selection (Auto / High / Low).

-----

## Notes

  - You can add your HLS streams to the `hls_output/` directory. They can be referenced in the player using paths like:
    ```
    /hls/master1.m3u8
    /hls/master2.m3u8
    /hls/master3.m3u8
    ```
  - JWT tokens are configured to be valid for 1 hour by default.
  - This project uses **HTTP/3 over TLS**. Therefore, traditional testing on `http://localhost:5000` will not work. You must access the server over HTTPS.
