import os
import sqlite3
from flask import Flask,render_template, request,url_for,flash,redirect
from werkzeug.exceptions import abort
from app import app

# Route for the homepage
@app.route('/')
def index():
    conn = get_db_connection()
    # Fetch all posts from the 'posts' table
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Route for /drac
@app.route('/drac')
def drac():
    return "Temp"

# Route for individual posts based on post ID
@app.route('/<int:post_id>')
def post(post_id):
    # Retrieve the post from the database
    post = get_post(post_id)
    # Render the 'post.html' template with the post data
    return render_template('post.html', post=post)

# Function to get the database connection
def get_db_connection():
    # Use an absolute path to avoid issues with incorrect file paths
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database.db'))
    print(f"Using database at: {db_path}")  # Debug print to verify path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Function to get a specific post based on its ID
def get_post(post_id):
    conn = get_db_connection()
    # Query the database for the specific post
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    # If post is not found, return a 404 error
    if post is None:
        abort(404)
    return post

@app.route('/create',methods=('GET','POST'))
def create():
    if request.method=='POST':
      title=request.form['title']
      content=request.form['content']
      if not title:
          flash('Title is Required!')
      else:
          conn=get_db_connection()
          conn.execute('INSERT INTO posts (title,content) VALUES (?,?)',(title,content))
          conn.commit()
          conn.close()
          return redirect(url_for('index'))
    return render_template('create.html')
             
@app.route('/<int:id>/edit',methods=('GET','POST'))
def edit(id):
    post=get_post(id)

    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn=get_db_connection()

            conn.execute('UPDATE posts SET title = ?,content = ?''WHERE id = ? ',(title,content,id))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html',post=post)

@app.route('/<int:id>/delete',methods=('POST',))
def delete(id):
    post=get_post(id)
    conn=get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))