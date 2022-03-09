import http
import os

from flask import Flask, jsonify, request

app = Flask(__name__)


auth_database = {
    os.getenv('Kucheryavenko'): {
        "username": "frbgd",
        "first_name": "Aleksey",
        "last_name": "Kucheryavenko",
        "email": "kap17597@yandex.ru",
        "id": "80c19d3c-7ed9-4882-ab33-789fe45991c4",
    },
    os.getenv('Zavitaev'): {
        "username": "TheZavitaev",
        "first_name": "Oleg",
        "last_name": "Zavitaev",
        "email": "o.zavitaev@yandex.ru",
        "id": "6ad3a14e-2ffd-4e3a-9013-b981a202b159",
    },
}


@app.route("/api/v1/me")
def get_me():
    token = request.headers.get("authorization")
    if not token:
        return jsonify("unauthorized"), http.HTTPStatus.UNAUTHORIZED

    user_data = auth_database.get(token)
    if not user_data:
        return jsonify("unauthorized"), http.HTTPStatus.UNAUTHORIZED

    return jsonify(user_data), http.HTTPStatus.CREATED


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5555,
    )
