from flask import Flask, request, jsonify, abort
from flasgger import Swagger
from flasgger.utils import swag_from
from sqlalchemy import or_
from database import init_db, db_session
from models import Note
from config import N

init_db()
app = Flask(__name__)
swagger = Swagger(app)


@app.route("/notes", methods=["GET", "POST"])
@swag_from("swagger/notes_get.yml", methods=["GET"])
@swag_from("swagger/notes_post.yml", methods=["POST"])
def notes():
    if request.method == "GET":
        query = request.args.get("query", None)
        if query is None:
            notes_from_db = Note.query.all()
        else:
            notes_from_db = Note.query.filter(or_(Note.title.contains(query), Note.content.contains(query))).all()
        result = []
        for note in notes_from_db:
            result.append(note.serialize)
        return jsonify(result)

    elif request.method == "POST":
        request_json = request.json
        content = request_json["content"]
        title = request_json.get("title", content[:min(N, len(content))])
        new_note = Note(title=title, content=content)
        db_session.add(new_note)
        db_session.commit()
        return jsonify(new_note.serialize)


@app.route("/notes/<int:note_id>", methods=["GET", "PUT", "DELETE"])
@swag_from("swagger/specified_note_get.yml", methods=["GET"])
@swag_from("swagger/specified_note_put.yml", methods=["PUT"])
@swag_from("swagger/specified_note_delete.yml", methods=["DELETE"])
def specified_note(note_id):
    note = Note.query.filter(Note.id == note_id).first()
    if note is None:
        abort(400, "Specified note id not found.")
    else:
        if request.method == "GET":
            return jsonify(note.serialize)
        elif request.method == "PUT":
            title = request.json.get("title", None)
            content = request.json.get("content", None)
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            db_session.commit()
            return jsonify(note.serialize)
        elif request.method == "DELETE":
            db_session.delete(note)
            db_session.commit()
            return "Specified note deleted.", 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
