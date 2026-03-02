import requests
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
URL = "https://jsonplaceholder.typicode.com/todos"


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)


def fill():
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    todos = r.json()

    for t in todos:
        row = Todo(
            id=int(t["id"]),
            userId=int(t["userId"]),
            title=str(t["title"]),
            completed=bool(t["completed"]),
        )
        db.session.add(row)

    db.session.commit()


def title_completed_count(userId):
    return (
        db.session.query(Todo)
        .filter(Todo.userId == int(userId), Todo.completed.is_(True))
        .count()
    )