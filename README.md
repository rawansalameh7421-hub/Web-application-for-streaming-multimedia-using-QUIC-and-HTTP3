# Web-application-for-streaming-multimedia-using-QUIC-and-HTTP3
---

```markdown
#  Secure Video Streaming Web App with JWT Authentication and HLS

This project is a secure web application that allows users to register, log in, and stream HLS (HTTP Live Streaming) video content. It uses JWT-based authentication, stores user data in a permanent SQLite database with hashed passwords, and delivers video content using HTTP/3 (QUIC) via the Quart framework and Hypercorn server.

---

##  Features

- User registration and login with secure password hashing (bcrypt)
- JWT token issuance and validation for secure access to protected content
- Video playback using HLS.js with quality selection
- animated HTML UI for login, signup, and playback
- HTTP/3 & QUIC support via Hypercorn + TLS

---

##  Project Structure

```

project/
├── DB.py              # Database functions (SQLite + bcrypt)
├── Server\_DB.py       # Quart backend server
├── player1.html       # HTML frontend for login/register & video player
├── cert.crt           # TLS certificate (for HTTPS/QUIC)
├── key.pem            # TLS private key
├── video/             # (Optional) Raw video uploads
└── hls\_output/        # HLS files served to the player (.m3u8 and .ts files)

````

---

##  Technologies Used

- **Python**: Backend logic
- **Quart**: Async web framework
- **Hypercorn**: ASGI server with QUIC support
- **JWT (PyJWT)**: Authentication tokens
- **bcrypt**: Secure password hashing
- **SQLite**: Lightweight local database
- **HTML5 + JavaScript**: User interface
- **HLS.js**: Video streaming player
- **TLS/HTTPS**: Encrypted traffic using cert.pem and key.pem

---

##  Installation & Running

### 1. Prerequisites

- Python 3.9+
- pip (Python package installer)
- TLS certificate and key (`cert.crt` and `key.pem`)
- HLS-encoded videos in `hls_output/` directory

### 2. Install Dependencies

```bash
pip install quart hypercorn pyjwt bcrypt
````

### 3. Run the Server

```bash
python Server_DB.py
```

Server will run on:
`https://localhost:4433` (with HTTP/3)

> Make sure you have `cert.crt` and `key.pem` in the same folder for HTTPS/QUIC.

### 4. Open the App

Navigate to:

```
https://localhost:4433/player1.html
```

>  Accept the certificate warning if using a self-signed cert.

---

##  Authentication Workflow

* **Register**: `POST /register` → stores user with hashed password
* **Login**: `POST /login` → returns JWT token
* **Access HLS videos**: `GET /hls/*.m3u8` or `*.ts` → requires valid `Authorization: Bearer <token>` header

---

##  Video Playback

The `player1.html` file provides a responsive interface with animated login/signup forms and a built-in HLS video player. Upon successful login, the app dynamically switches to playback mode with quality selection (Auto / High / Low).

---

##  Notes

* You can add your HLS streams to the `hls_output/` directory and reference them via:

  ```
  /hls/master1.m3u8
  /hls/master2.m3u8
  /hls/master3.m3u8
  ```
* Tokens are valid for 1 hour by default.
* This project uses **HTTP/3 over TLS**, so traditional `localhost:5000` HTTP testing won't work unless run over HTTPS.

```
