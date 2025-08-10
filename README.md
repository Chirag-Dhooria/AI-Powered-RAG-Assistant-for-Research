# Watsonx.ai Project Template

This repository contains a Python script to connect and interact with the **Watsonx.ai** platform using IBM's `ibm-watsonx-ai` SDK.

## 📌 Features
- Connect to Watsonx.ai using API key authentication.
- Specify and use your Watsonx.ai project ID and instance URL.
- Ready to be extended for your own AI workflows.

## 📂 Files
- `main.py` → The main script to connect to Watsonx.ai.
- `requirements.txt` → Dependencies required to run the script.

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Replace the placeholders in `main.py` with your Watsonx.ai details:
```python
url = "YOUR_WATSONX_URL"
project_id = "YOUR_PROJECT_ID"
```

You will also need your **IBM Cloud API Key**. Store it securely as an environment variable:
```bash
export IBM_CLOUD_API_KEY="your_api_key_here"   # For Linux/Mac
set IBM_CLOUD_API_KEY="your_api_key_here"     # For Windows
```

### 4️⃣ Run the Script
```bash
python main.py
```

## 🛡️ Security Notice
- **Never** commit your API key or credentials to the repository.
- Always use `.gitignore` to avoid uploading sensitive files.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
💡 *Tip:* This is just a starting template. You can expand this project by adding Watsonx.ai model training, inference, and data management code.
