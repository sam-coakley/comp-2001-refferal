from flask import Flask, request, jsonify
from flasgger import Swagger
import pyodbc
from datetime import datetime

app = Flask(__name__)
swagger = Swagger(app)

server = 'dist-6-505.uopnet.plymouth.ac.uk' 
database = 'COMP2001_SCoakley' 
username = 'SCoakley' 
password = 'MotL560*' 
driver = '{ODBC Driver 18 for SQL Server}'
conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No;'
)

def get_connection():
    return pyodbc.connect(conn_str)

@app.route("/comments", methods=["GET"])
def get_comments():
    """
    Get all comments
    ---
    responses:
      200:
        description: A list of comments
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CommentID, TrailID, UserEmail, Content, CreatedAt FROM CW2.Comments WHERE IsArchived = 0")
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route("/comments", methods=["POST"])
def add_comment():
    """
    Add a new comment
    ---
    parameters:
      - in: body
        name: comment
        schema:
          type: object
          required: [TrailID, Content, UserEmail]
          properties:
            TrailID:
              type: integer
            Content:
              type: string
            UserEmail:
              type: string
    responses:
      201:
        description: Comment added
    """
    data = request.get_json()
    trail_id = data.get("TrailID")
    content = data.get("Content")
    user_email = data.get("UserEmail")

    if not all([trail_id, content, user_email]):
        return jsonify({"error": "TrailID, Content, and UserEmail are required"}), 400

    created_at = datetime.utcnow()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CW2.Comments (TrailID, UserEmail, Content, CreatedAt, IsArchived) VALUES (?, ?, ?, ?, 0)",
        (trail_id, user_email, content, created_at)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment added"}), 201

@app.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    """
    Update a comment (only creator can edit)
    ---
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
      - in: body
        name: update
        schema:
          type: object
          required: [Content, UserEmail]
          properties:
            Content:
              type: string
            UserEmail:
              type: string
    responses:
      200:
        description: Comment updated
      403:
        description: Forbidden
      404:
        description: Not found
    """
    data = request.get_json()
    new_content = data.get("Content")
    user_email = data.get("UserEmail")

    if not new_content or not user_email:
        return jsonify({"error": "Content and UserEmail are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT UserEmail FROM CW2.Comments WHERE CommentID = ? AND IsArchived = 0", (comment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Comment not found"}), 404

    if row[0].lower() != user_email.lower():
        conn.close()
        return jsonify({"error": "Only the creator can edit this comment"}), 403

    cursor.execute("UPDATE CW2.Comments SET Content = ? WHERE CommentID = ?", (new_content, comment_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment updated"})

@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """
    Archive a comment (admin only)
    ---
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
      - in: body
        name: user
        schema:
          type: object
          required: [Role]
          properties:
            Role:
              type: string
    responses:
      200:
        description: Comment archived
      403:
        description: Forbidden
    """
    data = request.get_json()
    role = data.get("Role", "").lower()

    if role != "admin":
        return jsonify({"error": "Only admins can archive comments"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE CW2.Comments SET IsArchived = 1 WHERE CommentID = ?", (comment_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment archived"})

if __name__ == "__main__":
    app.run(debug=True)