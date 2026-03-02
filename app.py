# app.py
from io import BytesIO

from flask import Flask, jsonify, Response
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import usuario

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

usuario.db.init_app(app)


def init_db_once():
    # Borrar y crear la base de datos
    usuario.db.drop_all()
    usuario.db.create_all()

    # Completar la base de datos
    usuario.fill()
    print("Base de datos generada")


def completed_counts_all_users():
    # jsonplaceholder usa userId 1..10
    return {uid: usuario.title_completed_count(uid) for uid in range(1, 11)}


@app.get("/user/<int:id>/titles")
def user_titles(id: int):
    count = usuario.title_completed_count(id)
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2>Reporte</h2>
        <p>El usuario <b>{id}</b> completó <b>{count}</b> títulos.</p>
      </body>
    </html>
    """


@app.get("/user/titles")
def users_titles_json():
    data = completed_counts_all_users()
    payload = [{"userId": uid, "completed_titles": cnt} for uid, cnt in data.items()]
    return jsonify(payload)


@app.get("/user/graph")
def users_graph():
    data = completed_counts_all_users()
    user_ids = list(data.keys())
    counts = list(data.values())

    fig = plt.figure()
    plt.bar(user_ids, counts)
    plt.title("Títulos completados por usuario")
    plt.xlabel("userId")
    plt.ylabel("Cantidad completados")
    plt.xticks(user_ids)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return Response(buf.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    # Inicializar DB una sola vez al iniciar el server
    with app.app_context():
        init_db_once()

    app.run(debug=True)