from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
CONTACTS_FILE = 'contacts.json'

# Helper Functions
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

@app.route('/')
def index():
    query = request.args.get('q', '').lower()
    contacts = load_contacts()
    if query:
        contacts = [c for c in contacts if query in c['name'].lower() or query in c['phone'] or query in c['email'].lower()]
    return render_template('index.html', contacts=contacts, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        new_contact = {
            'name': request.form['name'],
            'phone': request.form['phone'],
            'email': request.form['email']
        }
        contacts = load_contacts()
        contacts.append(new_contact)
        save_contacts(contacts)
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_contact(index):
    contacts = load_contacts()
    if request.method == 'POST':
        contacts[index] = {
            'name': request.form['name'],
            'phone': request.form['phone'],
            'email': request.form['email']
        }
        save_contacts(contacts)
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contacts[index], index=index)

@app.route('/delete/<int:index>')
def delete_contact(index):
    contacts = load_contacts()
    contacts.pop(index)
    save_contacts(contacts)
    return redirect(url_for('index'))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

