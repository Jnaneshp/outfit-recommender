import sqlite3
import os


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

# Store database in py folder
DB_PATH = os.path.join(os.getcwd(), "wardrobe.db")

# Make sure folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def create_database():
    """Create database and all required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("📦 Creating database tables...")
    
    # ==========================================
    # USERS TABLE
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("✅ Users table created")
    
    
    # ==========================================
    # CLOTHES TABLE (WITH WEAR TRACKING)
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS clothes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        subtype TEXT,
        color TEXT,
        season TEXT,
        occasion TEXT,
        wear_count INTEGER DEFAULT 0,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    print("✅ Clothes table created")
    
    
    # ==========================================
    # OUTFIT HISTORY TABLE (NEW - TRACK WORN OUTFITS)
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS outfit_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        top_id INTEGER,
        bottom_id INTEGER,
        shoe_id INTEGER,
        season TEXT,
        occasion TEXT,
        rating INTEGER,
        notes TEXT,
        date_worn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
    )
    ''')
    print("✅ Outfit History table created")
    
    
    # ==========================================
    # RECOMMENDATIONS TABLE
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        top_id INTEGER,
        bottom_id INTEGER,
        shoe_id INTEGER,
        season TEXT,
        occasion TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
    )
    ''')
    print("✅ Recommendations table created")
    
    
    # ==========================================
    # SHARED OUTFITS TABLE (COMMUNITY FEATURE)
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS shared_outfits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        top_id INTEGER,
        bottom_id INTEGER,
        shoe_id INTEGER,
        title TEXT,
        description TEXT,
        likes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
        FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
    )
    ''')
    print("✅ Shared Outfits table created")
    
    
    # ==========================================
    # ITEM PRICE TABLE (COST PER WEAR)
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS item_price (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        price FLOAT,
        currency TEXT DEFAULT 'USD',
        purchase_date DATE,
        FOREIGN KEY(item_id) REFERENCES clothes(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    print("✅ Item Price table created")
    
    
    # ==========================================
    # FAVORITES TABLE
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(item_id) REFERENCES clothes(id) ON DELETE CASCADE,
        UNIQUE(user_id, item_id)
    )
    ''')
    print("✅ Favorites table created")
    
    
    # ==========================================
    # USER STATS TABLE (FOR ANALYTICS)
    # ==========================================
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        total_items INTEGER DEFAULT 0,
        total_outfits_worn INTEGER DEFAULT 0,
        favorite_color TEXT,
        favorite_style TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    print("✅ User Stats table created")
    
    
    # ==========================================
    # COMMIT CHANGES
    # ==========================================
    conn.commit()
    conn.close()
    print("\n" + "="*50)
    print("✅ DATABASE CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"📍 Location: {DB_PATH}\n")


# ==========================================
# MIGRATION FUNCTION (ADD NEW TABLES & COLUMNS)
# ==========================================

def migrate_database():
    """Add new tables and columns to existing databases"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("🔄 Checking for missing tables and columns...\n")
    
    # ===== ADD MISSING TABLES =====
    
    # Check if outfit_history exists
    try:
        c.execute("SELECT 1 FROM outfit_history LIMIT 1")
        print("⏭️  outfit_history table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating outfit_history table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS outfit_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            top_id INTEGER,
            bottom_id INTEGER,
            shoe_id INTEGER,
            season TEXT,
            occasion TEXT,
            rating INTEGER,
            notes TEXT,
            date_worn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
        )
        ''')
        print("✅ outfit_history table created")
    
    # Check if shared_outfits exists
    try:
        c.execute("SELECT 1 FROM shared_outfits LIMIT 1")
        print("⏭️  shared_outfits table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating shared_outfits table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS shared_outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            top_id INTEGER,
            bottom_id INTEGER,
            shoe_id INTEGER,
            title TEXT,
            description TEXT,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
        )
        ''')
        print("✅ shared_outfits table created")
    
    # Check if recommendations table exists
    try:
        c.execute("SELECT 1 FROM recommendations LIMIT 1")
        print("⏭️  recommendations table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating recommendations table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            top_id INTEGER,
            bottom_id INTEGER,
            shoe_id INTEGER,
            season TEXT,
            occasion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(top_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(bottom_id) REFERENCES clothes(id) ON DELETE SET NULL,
            FOREIGN KEY(shoe_id) REFERENCES clothes(id) ON DELETE SET NULL
        )
        ''')
        print("✅ recommendations table created")
    
    # Check if item_price exists
    try:
        c.execute("SELECT 1 FROM item_price LIMIT 1")
        print("⏭️  item_price table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating item_price table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS item_price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            price FLOAT,
            currency TEXT DEFAULT 'USD',
            purchase_date DATE,
            FOREIGN KEY(item_id) REFERENCES clothes(id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')
        print("✅ item_price table created")
    
    # Check if favorites exists
    try:
        c.execute("SELECT 1 FROM favorites LIMIT 1")
        print("⏭️  favorites table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating favorites table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(item_id) REFERENCES clothes(id) ON DELETE CASCADE,
            UNIQUE(user_id, item_id)
        )
        ''')
        print("✅ favorites table created")
    
    # Check if user_stats exists
    try:
        c.execute("SELECT 1 FROM user_stats LIMIT 1")
        print("⏭️  user_stats table already exists")
    except sqlite3.OperationalError:
        print("✅ Creating user_stats table...")
        c.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            total_items INTEGER DEFAULT 0,
            total_outfits_worn INTEGER DEFAULT 0,
            favorite_color TEXT,
            favorite_style TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')
        print("✅ user_stats table created")
    
    
    # ===== ADD MISSING COLUMNS =====
    
    print("\n🔍 Checking for missing columns in clothes table...\n")
    
    try:
        c.execute("ALTER TABLE clothes ADD COLUMN wear_count INTEGER DEFAULT 0")
        print("✅ Added wear_count column to clothes")
    except sqlite3.OperationalError:
        print("⏭️  wear_count column already exists")
    
    try:
        c.execute("ALTER TABLE outfit_history ADD COLUMN rating INTEGER")
        print("✅ Added rating column to outfit_history")
    except sqlite3.OperationalError:
        print("⏭️  rating column already exists")
    
    try:
        c.execute("ALTER TABLE outfit_history ADD COLUMN notes TEXT")
        print("✅ Added notes column to outfit_history")
    except sqlite3.OperationalError:
        print("⏭️  notes column already exists")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ MIGRATION COMPLETE!")
    print("="*50 + "\n")


# ==========================================
# DATABASE RESET FUNCTION (FOR TESTING)
# ==========================================

def reset_database():
    """Reset database (DELETE ALL DATA - Use with caution!)"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Old database deleted")
    
    create_database()


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("🎨 SMART WARDROBE ASSISTANT - DATABASE SETUP")
    print("="*50 + "\n")
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            print("⚠️  WARNING: This will delete all data!")
            confirm = input("Type 'YES' to confirm: ")
            if confirm == "YES":
                reset_database()
            else:
                print("❌ Reset cancelled")
        elif sys.argv[1] == "migrate":
            migrate_database()
        else:
            print("❌ Unknown command")
    else:
        # Create database if it doesn't exist
        if os.path.exists(DB_PATH):
            print("ℹ️  Database already exists at: " + DB_PATH)
            print("🔄 Running automatic migration...\n")
            migrate_database()
        else:
            create_database()
    
    print("✨ Database setup complete!\n")
