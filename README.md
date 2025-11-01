# 👗 Smart Wardrobe Assistant

An **AI-powered outfit recommendation system** built with **Flask + TensorFlow**, designed to intelligently classify clothing items and suggest perfect outfit combinations based on season, occasion, and wear frequency. Features a sophisticated wardrobe management system with wear tracking to balance your wardrobe usage.

## 🌟 Features

### 🎯 Core Features

- ✅ **User Authentication** - Secure login/register with SQLite database
- ✅ **AI Clothing Classification** - TensorFlow models classify items (tops/bottoms/shoes)
- ✅ **Smart Wardrobe Management** - Upload, organize, and manage your clothes
- ✅ **Intelligent Recommendations** - AI-powered outfit suggestions by season & occasion
- ✅ **Manual Tag Editing** - Fix/update season and occasion for any item

### 🚀 Advanced Features

- ✅ **Wear Count Tracking** - Track how many times each item is worn
- ✅ **Balanced Recommendations** - System prioritizes less-worn items automatically
- ✅ **Outfit History** - Complete history of all worn outfits
- ✅ **Wardrobe Statistics** - Visual dashboard with most/least worn items
- ✅ **Color-Coded Wear Badges** - Easy identification of item usage patterns
- ✅ **Responsive UI** - Beautiful, modern interface for desktop and mobile
- ✅ **One-Click Outfit Marking** - Mark outfits as worn to update statistics

---

## ⚙️ Tech Stack

| Component              | Technology              |
| ---------------------- | ----------------------- |
| **Backend**            | Flask 2.0+              |
| **ML Framework**       | TensorFlow / Keras      |
| **Database**           | SQLite3                 |
| **Image Processing**   | OpenCV, PIL, NumPy      |
| **Frontend**           | HTML5, CSS3, JavaScript |
| **Data Visualization** | Matplotlib, NumPy       |

---

## 📋 Requirements

Python 3.10+
pip (Python package manager)
Virtual Environment (recommended)

---

## 🧩 Installation & Setup

### **Step 1: Clone the Repository**

git clone https://github.com/Jnaneshp/outfit-recommender.git
cd Smart-Wardrobe-Assistant

### **Step 2: Create Virtual Environment** (use python 10.13)

Windows
python -m venv venv
venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate

### **Step 3: Install Dependencies**

pip install -r requirements.txt

### **Step 4: Set Up Database**

cd py
python db_setup.py

This will create and initialize all required database tables.

### **Step 5: Ensure Model Files Exist**

Place your trained TensorFlow models in the `models/` folder:
models/
├── model_top/ # Top classification model
├── model_bottom/ # Bottom classification model
├── model_sub/ # Subtype classification model
└── model_shoes/ # Shoes classification model

### **Step 6: Run the Flask App**

python app.py

Visit: [**http://127.0.0.1:5000/**](http://127.0.0.1:5000/)

---

## 📁 Project Structure

Smart-Wardrobe-Assistant/
│
├── venv/ # Virtual environment (in .gitignore)
│
├── requirements.txt # Project dependencies
├── .gitignore # Git ignore rules
├── README.md # This file
├── LICENSE # MIT License
│
├── models/ # Pre-trained ML models
│ ├── model_sub/
│ ├── model_top/
│ ├── model_bottom/
│ └── model_shoes/
│
├── data/ # Training data and samples
│
├── pictures/ # Demo images
│ ├── tutorial.png
│ ├── screenshot.png
│ └── demo/
│
├── py/ # Main Flask application
│ ├── app.py # Flask entry point (main app)
│ ├── recognition_module.py # ML prediction logic
│ ├── db_setup.py # Database initialization
│ ├── wardrobe.db # SQLite database (generated)
│ │
│ ├── templates/ # HTML templates
│ │ ├── index.html # Home page
│ │ ├── login.html # Login page
│ │ ├── register.html # Registration page
│ │ ├── recommend.html # Outfit recommendations
│ │ ├── wardrobe.html # Wardrobe management
│ │ └── outfit_history.html # Wear history (future)
│ │
│ ├── static/ # Static files
│ │ ├── style.css # Main stylesheet
│ │ ├── uploads/ # User uploaded images
│ │ │ └── [user_id]/ # User-specific uploads
│ │ └── temp/ # Temporary files
│ │
│ └── pycache/ # Python cache (in .gitignore)
│
└── documentation/ # Additional docs
├── SETUP.md # Detailed setup guide
├── FEATURES.md # Feature documentation
└── API.md # API endpoints reference

---

## 🚀 Quick Start Guide

### 1. **Register & Login**

Visit http://127.0.0.1:5000/
Create account → Login

### 2. **Upload Clothes**

Go to Home page
Upload clothing images
System automatically classifies them

### 3. **View Wardrobe**

Go to "My Wardrobe"
See all items with season/occasion tags
See wear count for each item
Edit tags or delete items

### 4. **Get Outfit Recommendations**

Go to "Recommendations"
Select Season (Spring/Summer/Fall/Winter)
Select Occasion (Casual/Formal/Party/etc)
Click "Generate Perfect Outfit"
System shows 3 items with lowest wear counts

### 5. **Mark Outfit as Worn**

Click "✅ Wear This Outfit!"
Wear counts increase for all 3 items
Get new recommendation automatically

---

## 🔧 Key Features Explained

### **Smart Wear Balancing Algorithm**

System prioritizes less-worn items
ORDER BY wear_count ASC

Instead of random recommendations, the app suggests the items you wear least frequently, ensuring balanced wardrobe usage.

### **Manual Season/Occasion Editing**

- Click "✏️ Edit" on any wardrobe item
- Change season or occasion tags
- System learns from corrections
- Improves future recommendations

### **Wear Count Tracking**

- Each item displays: "👕 Worn X times"
- Color-coded badges:
  - 🔵 **Blue** = Never worn (0 times)
  - 🟢 **Green** = Well-balanced (1-5 times)
  - 🟠 **Orange** = Frequently worn (5+ times)

### **Outfit History**

- Complete record of all worn outfits
- Track what you wore when
- Statistics dashboard showing patterns

---

## 📊 Database Schema

### **Tables Created**

- `users` - User accounts
- `clothes` - Wardrobe items with wear_count
- `outfit_history` - Track worn outfits
- `recommendations` - Saved recommendations
- `shared_outfits` - Community feature (future)
- `item_price` - Cost per wear (future)
- `favorites` - Favorite items (future)
- `user_stats` - User analytics

---

## 🎯 API Endpoints

| Endpoint            | Method | Purpose              |
| ------------------- | ------ | -------------------- |
| `/`                 | GET    | Home page            |
| `/login`            | POST   | User login           |
| `/register`         | POST   | User registration    |
| `/logout`           | GET    | User logout          |
| `/upload`           | POST   | Upload clothing item |
| `/recommend`        | GET    | Recommendation page  |
| `/generate_outfit`  | POST   | Generate outfit      |
| `/mark_outfit_worn` | POST   | Mark outfit as worn  |
| `/wardrobe`         | GET    | Wardrobe view        |
| `/update_item`      | POST   | Edit item tags       |
| `/delete_item`      | POST   | Delete item          |
| `/wardrobe_stats`   | GET    | Get statistics       |

---

## 🤖 ML Model Integration

### **Recognition Module** (`recognition_module.py`)

Classifies clothing using pre-trained models
subtype, info, details = single_classification(image_path)

Returns:

- subtype: 'top' / 'bottom' / 'foot'
- info: Human-readable description
- details: [color, pattern, season, occasion, ...]

---

## 📱 Responsive Design

- ✅ Works on Desktop (1920px+)
- ✅ Works on Tablet (768px-1024px)
- ✅ Works on Mobile (375px-768px)
- ✅ Beautiful modern UI with gradients
- ✅ Smooth animations and transitions

---

## 🔐 Security Features

- ✅ Password-based authentication
- ✅ Session management
- ✅ User data isolation
- ✅ SQL injection prevention
- ✅ Secure file handling

⚠️ **Note**: For production, implement:

- Password hashing (bcrypt)
- JWT tokens
- HTTPS
- CORS protection

---

## 🚨 Troubleshooting

### **Error: "no such table: outfit_history"**

cd py
python db_setup.py migrate

text

### **Error: Models not found**

Ensure `.h5` or `.keras` files are in `models/` folder

### **Port already in use**

Change port in app.py:
app.run(debug=True, port=5001)

text

### **Virtual environment not activating**

Windows (PowerShell issue):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate:
venv\Scripts\Activate.ps1

text

---

## 🎨 Customization

### **Change App Colors**

Edit `static/style.css`:
--primary-color: #667eea;
--secondary-color: #764ba2;

text

### **Add New Occasions**

Edit `templates/recommend.html`:

<option value="Your Occasion">🎯 Your Occasion</option> ```
Modify Wear Badge Thresholds
Edit templates/wardrobe.html:

text
{% if item.get('wear_count', 0) > 5%}high{% endif %}
