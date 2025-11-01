from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os, random, sqlite3
from recognition_module import single_classification  # your ML model


app = Flask(__name__)
app.secret_key = "your_secret_key_here_change_in_production"


# ==========================================
# Upload folder
# ==========================================
BASE_UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Database Configuration
# ==========================================
DB_PATH = os.path.join(os.path.dirname(__file__), "wardrobe.db")


def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# Smart Recommendation Function (Balanced by Wear Count)
# ==========================================

def get_smart_recommendations_balanced(user_id, season, occasion):
    """
    Get outfit recommendations filtered by season and occasion
    Prioritizes items that have been worn LESS frequently
    This balances wardrobe usage without changing ML models
    """
    conn = get_db_connection()
    
    # Query for matching tops - ORDER BY wear_count (lowest first)
    tops = conn.execute('''
        SELECT * FROM clothes 
        WHERE user_id = ? 
        AND subtype = 'top' 
        AND season = ? 
        AND occasion = ?
        ORDER BY wear_count ASC
    ''', (user_id, season, occasion)).fetchall()
    
    # Query for matching bottoms - ORDER BY wear_count (lowest first)
    bottoms = conn.execute('''
        SELECT * FROM clothes 
        WHERE user_id = ? 
        AND subtype = 'bottom' 
        AND season = ? 
        AND occasion = ?
        ORDER BY wear_count ASC
    ''', (user_id, season, occasion)).fetchall()
    
    # Query for matching shoes - ORDER BY wear_count (lowest first)
    shoes = conn.execute('''
        SELECT * FROM clothes 
        WHERE user_id = ? 
        AND subtype = 'foot' 
        AND season = ? 
        AND occasion = ?
        ORDER BY wear_count ASC
    ''', (user_id, season, occasion)).fetchall()
    
    conn.close()
    
    # Check if we have items for all categories
    if not tops or not bottoms or not shoes:
        missing = []
        if not tops: missing.append('tops')
        if not bottoms: missing.append('bottoms')
        if not shoes: missing.append('shoes')
        
        return {
            'success': False,
            'message': f'Not enough {season} {occasion} items ({", ".join(missing)}). Please upload more clothes!'
        }
    
    # Pick items with lowest wear_count (they're already sorted)
    selected_top = tops[0]
    selected_bottom = bottoms[0]
    selected_shoe = shoes[0]
    
    return {
        'success': True,
        'outfit': {
            'top': dict(selected_top),
            'bottom': dict(selected_bottom),
            'shoe': dict(selected_shoe)
        }
    }


# ==========================================
# Routes
# ==========================================

@app.route("/")
def index():
    """Home page"""
    return render_template("index.html", user=session.get("user_id"))


# ==========================================
# Login/Register
# ==========================================

@app.route("/login", methods=["GET","POST"])
def login():
    """User login"""
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password)).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    """User registration"""
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)", (username,email,password))
            conn.commit()
            user_id = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
        except:
            conn.close()
            return render_template("register.html", error="Username or email already exists")
        conn.close()
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for("index"))


# ==========================================
# Upload route
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():
    """Upload and classify clothing item"""
    user_id = session.get("user_id", "guest")
    user_folder = os.path.join(BASE_UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    file = request.files["file"]
    filepath = os.path.join(user_folder, file.filename)
    file.save(filepath)

    # Use ML model to classify clothing
    subtype, info_str, details = single_classification(filepath)

    # Save to database with wear_count=0 by default
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO clothes (user_id, file_path, subtype, color, season, occasion, wear_count) 
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (user_id, filepath, subtype, details[2], details[3], details[4]))
    conn.commit()
    conn.close()

    return jsonify({
        "file_url": f"/static/uploads/{user_id}/{file.filename}",
        "subtype": subtype,
        "season": details[3],
        "occasion": details[4],
        "info": info_str
    })


# ==========================================
# Recommendation Page
# ==========================================

@app.route("/recommend")
def recommend():
    """Render the recommendation page with season/occasion filters"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("recommend.html", user=session.get("user_id"))


# ==========================================
# Generate Outfit API (With Wear Balancing)
# ==========================================

@app.route("/generate_outfit", methods=["POST"])
def generate_outfit():
    """
    Generate outfit based on season and occasion preferences
    Prioritizes less-worn items
    """
    if "user_id" not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session["user_id"]
    season = request.form.get('season', 'Summer')
    occasion = request.form.get('occasion', 'Casual')
    
    # Get balanced recommendations (prioritizes less-worn items)
    result = get_smart_recommendations_balanced(user_id, season, occasion)
    
    if result['success']:
        outfit = result['outfit']
        top_filename = os.path.basename(outfit['top']['file_path'])
        bottom_filename = os.path.basename(outfit['bottom']['file_path'])
        shoe_filename = os.path.basename(outfit['shoe']['file_path'])
        
        return jsonify({
            'top_image': f'static/uploads/{user_id}/{top_filename}',
            'bottom_image': f'static/uploads/{user_id}/{bottom_filename}',
            'shoe_image': f'static/uploads/{user_id}/{shoe_filename}',
            'season': season,
            'occasion': occasion,
            'top_id': outfit['top']['id'],
            'bottom_id': outfit['bottom']['id'],
            'shoe_id': outfit['shoe']['id'],
            'top_wear_count': outfit['top']['wear_count'],
            'bottom_wear_count': outfit['bottom']['wear_count'],
            'shoe_wear_count': outfit['shoe']['wear_count']
        })
    else:
        return jsonify({'error': result['message']}), 404


# ==========================================
# Mark Outfit as Worn (Wear Tracking)
# ==========================================

@app.route("/mark_outfit_worn", methods=["POST"])
def mark_outfit_worn():
    """
    Mark an outfit as worn and increment wear counts for all items
    """
    if "user_id" not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = session["user_id"]
    data = request.get_json()
    
    top_id = data.get('top_id')
    bottom_id = data.get('bottom_id')
    shoe_id = data.get('shoe_id')
    
    conn = get_db_connection()
    
    try:
        # Increment wear count for each item
        for item_id in [top_id, bottom_id, shoe_id]:
            if item_id:
                conn.execute("""
                    UPDATE clothes 
                    SET wear_count = wear_count + 1 
                    WHERE id = ? AND user_id = ?
                """, (item_id, user_id))
        
        # Also record in outfit_history table
        conn.execute("""
            INSERT INTO outfit_history (user_id, top_id, bottom_id, shoe_id)
            VALUES (?, ?, ?, ?)
        """, (user_id, top_id, bottom_id, shoe_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Outfit marked as worn!'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})


# ==========================================
# Wardrobe page (With wear counts)
# ==========================================

@app.route("/wardrobe")
def wardrobe():
    """Display user's wardrobe with wear counts"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    clothes = conn.execute("SELECT * FROM clothes WHERE user_id=?", (user_id,)).fetchall()
    conn.close()

    # Organize clothes by subtype with all metadata
    wardrobe = {"top": [], "bottom": [], "foot": []}
    for c in clothes:
        wardrobe[c["subtype"]].append({
            "id": c["id"],
            "file_name": os.path.basename(c["file_path"]),
            "url": f"/static/uploads/{user_id}/{os.path.basename(c['file_path'])}",
            "subtype": c["subtype"],
            "season": c["season"],
            "occasion": c["occasion"],
            "wear_count": c["wear_count"]
        })

    return render_template("wardrobe.html", wardrobe=wardrobe, user=user_id)


# ==========================================
# Update Item (Manual Season/Occasion Editing)
# ==========================================

@app.route("/update_item", methods=["POST"])
def update_item():
    """Update season and occasion for an existing wardrobe item"""
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"})
    
    user_id = session["user_id"]
    data = request.get_json()
    file_name = data.get("file_name")
    new_season = data.get("season")
    new_occasion = data.get("occasion")
    
    # Construct full file path
    file_path = os.path.join(BASE_UPLOAD_FOLDER, str(user_id), file_name)
    
    # Update database
    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE clothes 
            SET season = ?, occasion = ? 
            WHERE user_id = ? AND file_path = ?
        """, (new_season, new_occasion, user_id, file_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Item updated successfully"})
    except Exception as e:
        conn.close()
        return jsonify({"success": False, "error": str(e)})


# ==========================================
# Delete wardrobe item
# ==========================================

@app.route("/delete_item", methods=["POST"])
def delete_item():
    """Delete a wardrobe item"""
    if "user_id" not in session:
        return jsonify({"success": False, "error": "Not logged in"})

    user_id = session["user_id"]
    data = request.get_json()
    file_name = data.get("file")
    file_path = os.path.join(BASE_UPLOAD_FOLDER, str(user_id), file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        # Remove from DB
        conn = get_db_connection()
        conn.execute("DELETE FROM clothes WHERE user_id=? AND file_path=?", (user_id, file_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "File not found"})


# ==========================================
# Wardrobe Statistics
# ==========================================

@app.route("/wardrobe_stats")
def wardrobe_stats():
    """Get statistics about wardrobe usage"""
    if "user_id" not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = session["user_id"]
    conn = get_db_connection()
    
    stats = conn.execute("""
        SELECT 
            COUNT(*) as total_items,
            SUM(wear_count) as total_wears,
            AVG(wear_count) as avg_wears,
            MIN(wear_count) as min_wears,
            MAX(wear_count) as max_wears
        FROM clothes
        WHERE user_id = ?
    """, (user_id,)).fetchone()
    
    # Get most worn items
    most_worn = conn.execute("""
        SELECT id, file_path, subtype, wear_count 
        FROM clothes 
        WHERE user_id = ? 
        ORDER BY wear_count DESC 
        LIMIT 3
    """, (user_id,)).fetchall()
    
    # Get least worn items
    least_worn = conn.execute("""
        SELECT id, file_path, subtype, wear_count 
        FROM clothes 
        WHERE user_id = ? 
        ORDER BY wear_count ASC 
        LIMIT 3
    """, (user_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'total_items': stats['total_items'] or 0,
        'total_wears': stats['total_wears'] or 0,
        'avg_wears': round(stats['avg_wears'], 2) if stats['avg_wears'] else 0,
        'most_worn': [{'id': m['id'], 'path': m['file_path'], 'type': m['subtype'], 'count': m['wear_count']} for m in most_worn],
        'least_worn': [{'id': l['id'], 'path': l['file_path'], 'type': l['subtype'], 'count': l['wear_count']} for l in least_worn]
    })


# ==========================================
# Outfit History
# ==========================================

@app.route("/outfit_history")
def outfit_history():
    """Display outfit wear history"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    conn = get_db_connection()
    
    history = conn.execute("""
        SELECT oh.*, 
               c1.file_path as top_path,
               c2.file_path as bottom_path,
               c3.file_path as shoe_path
        FROM outfit_history oh
        LEFT JOIN clothes c1 ON oh.top_id = c1.id
        LEFT JOIN clothes c2 ON oh.bottom_id = c2.id
        LEFT JOIN clothes c3 ON oh.shoe_id = c3.id
        WHERE oh.user_id = ?
        ORDER BY oh.date_worn DESC
        LIMIT 20
    """, (user_id,)).fetchall()
    
    conn.close()
    
    return render_template("outfit_history.html", history=history, user=user_id)


# ==========================================
# Run Application
# ==========================================

if __name__=="__main__":
    app.run(debug=True, port=5000)
