# 🎯 ToneForge AI

**AI-powered email tone transformation** - Transform your emails between formal and casual tones instantly using T5 language model.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://tone-forge-ai.vercel.app)
[![Hugging Face](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)](https://huggingface.co/spaces/dxv39/tone-formalizer)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


---

## ✨ Features

- 🔄 **Dual Mode Transformation** - Switch between formal and casual tones
- ⚡ **Real-time Processing** - Get transformed emails in milliseconds
- 🎨 **Modern UI** - Beautiful dark theme with smooth animations
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile
- 🔒 **Privacy-First** - No data stored, all processing done on-demand
- 🚀 **Fast API** - Powered by FastAPI and T5 model

---

## 🎥 Demo

**Live Application**: [https://tone-forge-ai.vercel.app](https://tone-forge-ai.vercel.app)

### Example Transformation

**Input (Casual):**

```
hey, just wanted to check in about the project we discussed yesterday.
let me know if you have any updates or questions.
```

**Output (Formal):**

```
Subject: Project Follow-up

Hi Sarah,

I hope this message finds you well. I am writing to follow up on our
discussion regarding the project from yesterday. Please feel free to
share any updates or questions you may have at your convenience.

Thanks,
Mark
```

---

## 🏗️ Architecture

```
┌─────────────────┐         HTTPS          ┌──────────────────┐
│                 │ ──────────────────────> │                  │
│  Vercel Frontend│                         │  HuggingFace API │
│   (React/HTML)  │ <────────────────────── │   (FastAPI)      │
│                 │         JSON            │                  │
└─────────────────┘                         └──────────────────┘
       │                                              │
       │                                              │
       v                                              v
  User Interface                            T5 Model (dxv39/tone)
  - Email Input                             - Tone Transformation
  - Mode Selection                          - Text Generation
  - Result Display                          - Response Formatting
```

### Tech Stack

**Frontend:**

- HTML5 / CSS3 / JavaScript (Vanilla)
- Deployed on [Vercel](https://vercel.com)
- Fonts: Clash Display, General Sans

**Backend:**

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Transformers](https://huggingface.co/docs/transformers) - Hugging Face library
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [T5 Model](https://huggingface.co/dxv39/tone) - Fine-tuned for tone transformation
- Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for Vercel CLI, optional)
- Git

### Backend Setup (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/K37VIN/ToneForgeAI.git
   cd ToneForgeAI
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server**

   ```bash
   uvicorn app:app --reload --port 8000
   ```

4. **Test the API**
   ```bash
   curl http://localhost:8000/
   # Expected: {"status":"online","model":"T5-tone-formalizer"}
   ```

### Frontend Setup (Local)

1. **Update API URL**

   Open `index.html` and change the API URL:

   ```javascript
   const API_URL = "http://localhost:8000"; // For local testing
   ```

2. **Open in browser**

   ```bash
   # Simple way - just open the file
   open index.html

   # OR use a local server (recommended)
   python -m http.server 3000
   # Then visit: http://localhost:3000
   ```

---

## 📦 Deployment

### Deploy Backend to Hugging Face Spaces

1. **Create a new Space**
   - Go to [Hugging Face Spaces](https://huggingface.co/new-space)
   - Select "Docker" as the SDK
   - Choose a name (e.g., `tone-formalizer`)

2. **Upload files**

   ```
   app.py
   requirements.txt
   Dockerfile (optional)
   ```

3. **Your API will be live at:**
   ```
   https://[username]-[space-name].hf.space
   ```

### Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional)

   ```bash
   npm i -g vercel
   ```

2. **Deploy**

   ```bash
   vercel
   ```

   **OR** use the dashboard:
   - Go to [vercel.com](https://vercel.com)
   - Drag and drop `index.html`
   - Done! ✨

3. **Update API URL in frontend**

   ```javascript
   const API_URL = "https://[username]-[space].hf.space";
   ```

4. **Update CORS in backend**
   ```python
   allow_origins=[
       "https://your-app.vercel.app",
       "https://your-app-*.vercel.app",
   ]
   ```

---

## 🔧 Configuration

### Backend (app.py)

```python
# Model Configuration
MODEL_NAME = "dxv39/tone"  # Change to your model

# CORS Settings
allow_origins=[
    "https://your-vercel-app.vercel.app",  # Your frontend URL
    "*"  # Remove in production
]

# Generation Parameters
max_length=256      # Maximum output length
num_beams=5         # Beam search size
temperature=0.7     # Sampling temperature
```

### Frontend (index.html)

```javascript
// API Endpoint
const API_URL = "https://your-backend.hf.space";

// Modes
const modes = ["formal", "casual"]; // Available transformation modes
```

---

## 📡 API Documentation

### Base URL

```
https://dxv39-tone-formalizer.hf.space
```

### Endpoints

#### `GET /`

Health check endpoint.

**Response:**

```json
{
  "status": "online",
  "model": "T5-tone-formalizer"
}
```

#### `POST /transform-email`

Transform email tone.

**Request Body:**

```json
{
  "subject": "Project Update",
  "recipient": "Sarah",
  "sender": "John",
  "body": "hey, just checking in on the project",
  "mode": "formal"
}
```

**Response:**

```json
{
  "formatted_email": "Subject: Project Update\n\nHi Sarah,\n\nI hope this message finds you well...\n\nThanks,\nJohn",
  "latency_ms": 1247.32
}
```

**Error Response:**

```json
{
  "detail": "Mode must be either 'formal' or 'casual'"
}
```

---

## 🧪 Testing

### Backend Tests

```bash
# Test health endpoint
curl https://dxv39-tone-formalizer.hf.space/

# Test transformation
curl -X POST https://dxv39-tone-formalizer.hf.space/transform-email \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test",
    "recipient": "Jane",
    "sender": "John",
    "body": "hey whats up",
    "mode": "formal"
  }'
```

### Frontend Tests

1. Open browser DevTools (F12)
2. Go to Console tab
3. Submit a test email
4. Check for any errors

---

## 🎨 Customization

### Changing Colors

Edit CSS variables in `index.html`:

```css
:root {
  --bg: #0a0a0f; /* Background */
  --accent: #7c3aed; /* Primary accent */
  --accent-bright: #a78bfa; /* Light accent */
  --success: #10b981; /* Success color */
}
```

### Changing Fonts

Update Google Fonts import:

```html
<link
  href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap"
  rel="stylesheet"
/>
```

---

## 📊 Performance

- **Average Response Time**: ~1-2 seconds
- **Model Size**: ~220MB
- **Supported Platforms**: CPU/GPU
- **Concurrent Requests**: Limited by Hugging Face Spaces tier

---

## 🛠️ Troubleshooting

### Issue: "CORS Error"

**Solution:**

- Ensure CORS middleware is enabled in backend
- Verify your Vercel URL is in `allow_origins`
- Check browser console for exact error

### Issue: "Status shows Offline"

**Solution:**

- Check if backend is running (visit HF Space URL)
- Verify `API_URL` in frontend matches backend URL
- Check browser Network tab for failed requests

### Issue: "Request Failed"

**Solution:**

- Verify all form fields are filled
- Check mode is either "formal" or "casual"
- Ensure backend is deployed and accessible

### Issue: "Slow Response Times"

**Solution:**

- HF Spaces may be cold-starting (first request is slower)
- Consider upgrading to paid HF Spaces tier
- Check your internet connection

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Test thoroughly before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **K37VIN** - _Initial work_ - [@K37VIN](https://github.com/K37VIN)

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for hosting and Transformers library
- [Vercel](https://vercel.com/) for frontend hosting
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- Google Fonts for Clash Display and General Sans

---

## 🗺️ Roadmap

- [ ] Add more tone options (professional, friendly, assertive)
- [ ] Support for multiple languages
- [ ] Email template library
- [ ] Browser extension
- [ ] Mobile app (iOS/Android)
- [ ] API rate limiting and authentication
- [ ] User accounts and history
- [ ] Batch processing
- [ ] Export to various formats (PDF, DOCX)

---

<div align="center">

**Made with ❤️ by K37VIN**

If you found this helpful, please ⭐ star the repo!

</div>

