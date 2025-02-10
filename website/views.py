from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# Main Homepage (Public homepage for non-logged-in users, Redirect for logged-in users)
@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated and request.method == 'POST':  # If logged in and submitted a note
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)  # Single homepage

@views.route('/delete-note', methods=['POST'])
@login_required  # Ensure the user is logged in before deleting a note
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:  # Ensure user owns the note
            db.session.delete(note)
            db.session.commit()

    return jsonify({})  # Always return a response
