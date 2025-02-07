function deleteNote(noteId) {
    // Send a POST request to delete the note with the given ID
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Ensure the server knows the request body is JSON
        },
        body: JSON.stringify({ noteId: noteId }),
    })
    .then((_res) => {
        // Redirect to the home page after the note is deleted
        window.location.href = "/";
    })
}
