from flask import Flask, jsonify, request

app = Flask(__name__)


auth_database = {
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4MGMxOWQzYy03ZWQ5LTQ4ODItYWIzMy03ODlmZTQ1OTkxYzQiLCJmaXJzdF9uYW1lIjoiQWxla3NleSIsImxhc3RfbmFtZSI6Ikt1Y2hlcnlhdmVua28iLCJpYXQiOjE1MTYyMzkwMjJ9.xLp_4zECLl-0YpbcPpy-SOi9o7sO64_1G37tJ0ZWw7A": {
        "username": "frbgd",
        "first_name": "Aleksey",
        "last_name": "Kucheryavenko",
        "email": "kap17597@yandex.ru",
        "id": "80c19d3c-7ed9-4882-ab33-789fe45991c4",
    },
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2YWQzYTE0ZS0yZmZkLTRlM2EtOTAxMy1iOTgxYTIwMmIxNTkiLCJmaXJzdF9uYW1lIjoiT2xlZyIsImxhc3RfbmFtZSI6Ilphdml0YWV2IiwiaWF0IjoxNTE2MjM5MDIyfQ.5G12pR-rel7UHNz7kdNrNcQ_it63pHmKCM7_eeM1zSY": {
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
