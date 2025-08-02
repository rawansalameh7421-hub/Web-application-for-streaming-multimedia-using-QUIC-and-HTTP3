
import asyncio
from quart import Quart, send_from_directory, request, jsonify
from pathlib import Path
from hypercorn.asyncio import serve
from hypercorn.config import Config
import jwt
import datetime
import os


from DB import setup_database, add_user, find_user, check_password

SCRIPT_DIR = Path(__file__).resolve().parent
CERT_FILE = SCRIPT_DIR / "cert.crt"
KEY_FILE = SCRIPT_DIR / "key.pem"
PROJECT_DIR = SCRIPT_DIR
VIDEO_DIR = PROJECT_DIR / "video"
HLS_DIR = PROJECT_DIR / "hls_output"

# Quart app
app = Quart(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-super-secret-key-that-is-long-and-secure")

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(HLS_DIR, exist_ok=True)
setup_database() 

@app.route("/")
@app.route("/player1.html")
async def player():
    return await send_from_directory(PROJECT_DIR, "player1.html")

@app.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    user_data = find_user(username)

    
    if user_data and check_password(user_data[2], password):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, app.config["JWT_SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token})
        
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/register", methods=["POST"])
async def register():
    data = await request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    
    if add_user(username, password):
        print(f" New user '{username}' has been saved to the database with a hashed password.")
        return jsonify({"message": "Account created successfully"}), 201
    else:
        return jsonify({"message": "Username already exists"}), 409

@app.route("/hls/<path:filename>")
async def serve_hls(filename):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    try:
        
        jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return await send_from_directory(HLS_DIR, filename)
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 401


@app.after_request
async def add_alt_svc_header(response):
    response.headers["Alt-Svc"] = 'h3=":4433"; ma=86400'
    return response


async def main():
    config = Config()
    config.bind = ["0.0.0.0:4433"]
    config.certfile = CERT_FILE
    config.keyfile = KEY_FILE
    config.alpn_protocols = ["h3"]
    config.keep_alive_timeout = 60

    print(f" Full-featured server with Permanent DB and QUIC/HTTP/3 support running at https://localhost:4433")
    await serve(app, config)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
