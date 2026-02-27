from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db


views = Blueprint("views", __name__)


@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        note = request.form["note"]

        if len(note) < 1:
            flash("Note is blank!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category='success')
        
    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = request.get_json()
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note Deleted!", category='success')

    return jsonify({})