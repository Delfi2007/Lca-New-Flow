# 🌍 LCA (Life Cycle Assessment) Application

A comprehensive web application for conducting Life Cycle Assessments with AI-powered data analysis and gap-filling.

## 🚀 Features

### ✅ Authentication System
- **Email/Password Authentication**: Traditional login/signup
- **Google OAuth 2.0**: Social login integration
- **Facial Recognition**: Biometric authentication using Face++ API
- **Two-Factor Authentication (2FA)**: Enhanced security with OTP

### 📊 Dataset Selection (Page 1)
- **OpenLCA Integration**: Connect to local OpenLCA IPC Server
- **Ecoinvent Database**: Access to comprehensive LCA datasets
- **Indian LCI Database**: Region-specific data
- **Built-in Datasets**: Pre-loaded common materials and processes
- **Custom Upload**: Upload your own CSV/Excel datasets

### 🤖 AI-Powered Product Input (Page 2)
- **Natural Language Processing**: Describe products in plain English
- **Structured Form Input**: Detailed material composition forms
- **Intelligent Gap-Filling**: Auto-complete missing data using:
  - Groq AI (llama-3.3-70b-versatile)
  - OpenLCA database queries
  - Industry-standard defaults
- **Smart Hints**: Context-aware suggestions for better data quality
- **Material Recycling Slider**: Track recycled content percentage (0-100%)

## 📋 Prerequisites

- **Python 3.8+**
- **OpenLCA 2.5.0** (optional, for OpenLCA datasets)
- **Groq API Key** (for AI features)
- **Face++ API Key** (for facial recognition)
- **Google OAuth Credentials** (for Google login)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Delfi2007/Lca-New-Flow.git
cd Lca-New-Flow
```

### 2. Install Dependencies
```bash
cd authentication
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

**Get API Keys:**
- **Groq API**: https://console.groq.com/keys
- **Face++ API**: Already configured in `face_api.py`
- **Google OAuth**: https://console.cloud.google.com/

### 4. Set Up OpenLCA (Optional)

1. Download and install [OpenLCA 2.5.0](https://www.openlca.org/download/)
2. Open OpenLCA and create/open a database (e.g., ELCD 3.2)
3. Start the IPC Server:
   - **Tools** → **Developer Tools** → **IPC Server**
   - Port: `8080`

## 🎯 Running the Application

### Windows (PowerShell)
```powershell
# Set environment variable
$env:GROQ_API_KEY="your_api_key_here"

# Run the app
cd authentication
python app.py
```

Or use the provided script (after editing with your API key):
```powershell
.\run_app.ps1
```

### Linux/Mac
```bash
# Set environment variable
export GROQ_API_KEY="your_api_key_here"

# Run the app
cd authentication
python app.py
```

### Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. **Authentication**
- Create an account using email/password, Google, or facial recognition
- Login using any of the configured methods

### 2. **Dataset Selection**
- Choose your data source:
  - **OpenLCA**: Requires local IPC Server running
  - **Ecoinvent**: Pre-loaded dataset
  - **Indian LCI**: Region-specific data
  - **Built-in**: Default materials database
- Click **Continue** to proceed

### 3. **Product Input**
Choose your input method:

**Option A: Natural Language Input**
```
Example: "500g aluminum can with 30% recycled content for beverage packaging, manufacturing stage"
```
- Click **Analyze with AI**
- AI extracts structured data automatically
- Review and confirm extracted information

**Option B: Structured Form**
- Fill in product details:
  - Product name
  - Material type (dropdown)
  - Weight (with unit)
  - Recycled content (0-100% slider)
  - Lifecycle stage
  - Processing details
- Click **Analyze Product**

### 4. **Gap-Filling**
- If data is missing, click **Fill Missing Data**
- AI and OpenLCA automatically fill gaps with industry standards
- Review and adjust filled values

### 5. **Confirmation & Results**
- Review final product data
- Proceed to LCA calculation
- View environmental impact results

## 🛠️ API Endpoints

### Authentication
- `POST /signup` - Email/password registration
- `POST /login` - Email/password login
- `POST /face-login` - Facial recognition login
- `POST /face-signup` - Facial recognition registration
- `GET /auth/google` - Google OAuth login
- `GET /auth/google/callback` - OAuth callback

### Dataset Management
- `GET /dataset` - Dataset selection page
- `GET /api/check-openlca` - Check OpenLCA availability
- `GET /api/datasets?source=<source>` - Get datasets by source
- `POST /api/upload-dataset` - Upload custom dataset

### Product Input (Page 2)
- `GET /input-data` - Product input page
- `POST /api/analyze-nlp` - NLP text analysis
- `POST /api/analyze-structured` - Structured form analysis
- `POST /api/gap-fill` - Fill missing data
- `POST /api/openlca-data` - Query OpenLCA database

## 📁 Project Structure

```
Lca-New-Flow/
├── authentication/
│   ├── app.py                    # Main Flask application
│   ├── face_api.py              # Face++ API integration
│   ├── database.py              # Database models and queries
│   ├── otp_service.py           # 2FA OTP service
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   ├── templates/
│   │   ├── auth.html           # Authentication page
│   │   ├── dataset.html        # Dataset selection (Page 1)
│   │   └── input.html          # Product input (Page 2)
│   ├── static/
│   │   ├── css/
│   │   │   ├── auth.css
│   │   │   ├── dataset.css
│   │   │   └── input.css
│   │   └── js/
│   │       ├── auth.js
│   │       ├── dataset.js
│   │       └── input.js
│   ├── instance/               # SQLite database
│   ├── flask_session/          # Session storage
│   └── user_faces/             # Facial recognition tokens
├── .gitignore
└── README.md
```

## 🔐 Security Notes

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use `.env` file (excluded from git)
- **Production**: Change `SECRET_KEY` and disable debug mode
- **HTTPS**: Use HTTPS in production for OAuth callbacks
- **Face Tokens**: Stored securely, not in database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- **Delfi2007** - [GitHub](https://github.com/Delfi2007)

## 🙏 Acknowledgments

- **OpenLCA** - Open source LCA software
- **Groq** - Fast AI inference API
- **Face++** - Facial recognition technology
- **Flask** - Python web framework

## 📞 Support

For issues and questions:
- Create an issue on [GitHub](https://github.com/Delfi2007/Lca-New-Flow/issues)
- Check the documentation in the `authentication/` folder

## 🔄 Updates

### Version 2.0 (Current)
- ✅ AI-powered NLP product input
- ✅ Intelligent gap-filling with Groq API
- ✅ OpenLCA integration for dataset queries
- ✅ Material recycling content tracking
- ✅ Smart hints and industry averages

### Coming Soon (Page 3 & 4)
- 📋 Confirmation page with data review
- 📊 LCA calculation engine
- 📈 Results dashboard with visualizations
- 📄 Report generation (PDF/Excel)
- 🔄 Comparison tools for multiple products

---

Made with ❤️ for sustainable engineering
