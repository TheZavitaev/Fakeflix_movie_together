from flask import Flask, request, jsonify

app = Flask(__name__)


auth_database = {
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFsZXgiLCJpYXQiOjE1MTYyMzkwMjJ9.eYLYdLSJI8N1wFc5f3U0BMKuTJv8mcwfmA8is1f7ctc": {
        "username": "frbgd",
        "first_name": "Aleksey",
        "last_name": "Kucheryavenko",
        "email": "kap17597@yandex.ru",
        "id": "80c19d3c-7ed9-4882-ab33-789fe45991c4",
    },
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik9sZWciLCJpYXQiOjE1MTYyMzkwMjJ9.v3C2__WNGbbu17Ca6rVukPjcU0yGTeexz7QBNX42Pfc": {
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
        return jsonify("unauthorized"), 401

    user_data = auth_database.get(token)
    if not user_data:
        return jsonify("unauthorized"), 401

    return jsonify(user_data), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5555,
    )
