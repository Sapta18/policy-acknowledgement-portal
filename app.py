from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import ai_service
import re

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "mysecretkey"
jwt = JWTManager(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)
CORS(app)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "1234":
        token = create_access_token(identity=username)
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401


limiter = Limiter(get_remote_address, app=app, default_limits=["30 per minute"])


def sanitize_input(user_input):
    import re

    # Remove HTML
    clean_input = re.sub(r"<.*?>", "", user_input)

    # Block prompt injection
    if "ignore previous" in clean_input.lower():
        return None

    # Block SQL injection
    if "'" in clean_input or "--" in clean_input:
        return None

    return clean_input

@jwt_required()
@app.route("/chat", methods=["POST"])
@limiter.limit("30 per minute")   
def chat():
    data = request.json
    user_input = data.get("message")
    if not user_input or user_input.strip() == "":
        return jsonify({"error": "Empty input"}), 400
    if "ignore" in user_input.lower():
        return jsonify({"error": "Invalid input"}), 400

    
    clean_input = sanitize_input(user_input)

    if not clean_input:
        return jsonify({"error": "Invalid or unsafe input"}), 400
    
    try:
        ai_reply = ai_service.get_ai_response(user_input)
        return jsonify({"response": ai_reply})
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


if __name__ == "__main__":
    app.run(debug=True)
    
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response