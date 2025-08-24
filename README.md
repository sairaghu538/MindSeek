# 🧠 MindSeek - AI Chat Assistant

A modern, intelligent AI chatbot powered by Google Gemini AI, built with Streamlit.

![MindSeek App](https://img.shields.io/badge/Streamlit-App-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange)

## ✨ Features

- 🤖 **Powered by Google Gemini AI** - Latest AI model with 1-year subscription
- 💬 **Intelligent Chat Interface** - Natural conversation flow with chat history
- 🎨 **Modern UI/UX** - Beautiful gradient design with responsive layout
- ⚙️ **Customizable Settings** - Adjust creativity levels and model selection
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔒 **Secure API Management** - Environment-based configuration
- 📊 **Chat Statistics** - Track your conversation history

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (1-year subscription)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MindSeek-1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the root directory:
   ```bash
   # .env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```
   
   **⚠️ Important**: Never commit your `.env` file to version control!

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 🔑 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API key" in the top right
4. Create a new API key or use an existing one
5. Copy the API key and add it to your `.env` file

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended for Beginners)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit with Gemini integration"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Add your environment variables:
     - `GOOGLE_API_KEY`: Your Gemini API key
   - Click "Deploy"

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_api_key_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Option 3: Railway

1. **Connect your GitHub repo to Railway**
2. **Set environment variables**
3. **Deploy automatically**

### Option 4: VPS/Cloud Server

1. **Set up a VPS** (DigitalOcean, AWS, etc.)
2. **Install Python and dependencies**
3. **Use systemd or PM2 for process management**
4. **Set up Nginx reverse proxy**
5. **Configure SSL with Let's Encrypt**

## 📁 Project Structure

```
MindSeek-1/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .streamlit/           # Streamlit configuration
│   └── config.toml      # Production settings
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Gemini API key | Required |
| `STREAMLIT_SERVER_PORT` | Port to run the app | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Server address | 0.0.0.0 |

### Model Settings

- **gemini-1.5-flash**: Fast, efficient responses (default)
- **gemini-1.5-pro**: More advanced, detailed responses
- **Temperature**: Controls creativity (0.0 = focused, 1.0 = creative)

## 🛠️ Customization

### Changing the Theme

Edit `.streamlit/config.toml` to customize colors and appearance.

### Adding New Features

The modular structure makes it easy to add:
- File upload capabilities
- Image generation
- Voice input/output
- Multi-language support
- Custom system prompts

## 🔒 Security Best Practices

1. **Never hardcode API keys** in your source code
2. **Use environment variables** for sensitive data
3. **Add `.env` to `.gitignore`**
4. **Regularly rotate your API keys**
5. **Monitor API usage** to stay within limits

## 📊 Monitoring & Analytics

- Track API usage in Google AI Studio
- Monitor app performance with Streamlit Cloud analytics
- Set up logging for production environments

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your `.env` file exists and contains the correct API key
   - Verify the API key is valid and not expired

2. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Deployment Issues**
   - Verify environment variables are set correctly
   - Check deployment platform logs for errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Streamlit team for the amazing framework
- Open source community for inspiration and tools

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Made with ❤️ using Google Gemini AI and Streamlit**


