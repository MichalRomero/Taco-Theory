from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# Main Homepage (Public homepage for non-logged-in users, Redirect for logged-in users)
@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:  # If the user is logged in
        if request.method == 'POST':  # Handle note submission
            note = request.form.get('note')

            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')

        # Redirect logged-in users to their role-based homepage
        if current_user.role == "staff":
            return render_template("staff_home.html", user=current_user)  # Staff homepage
        else:
            return render_template("customer_home.html", user=current_user)  # Customer homepage

    # If the user is not logged in, show the public homepage
    return render_template("public_home.html", user=None)  # Public homepage for non-logged-in users

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
