# 🐦 Twitter Sentiment Analysis Web App

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Twitter API](https://img.shields.io/badge/Twitter-API%20v1.1-blue.svg)](https://developer.twitter.com/)

A modern, responsive web application that analyzes the sentiment of tweets for any given keyword using Natural Language Processing. Built with Flask, Twitter API, and TextBlob for real-time sentiment analysis with beautiful visualizations.

## ✨ Features

- 🔍 **Real-time Tweet Analysis** - Fetch and analyze live tweets from Twitter
- 📊 **Comprehensive Sentiment Scoring** - 7-level sentiment classification system
- 📈 **Interactive Visualizations** - Beautiful pie charts with detailed breakdowns
- 💾 **Data Export** - Save analyzed tweets to CSV format
- 📱 **Responsive Design** - Mobile-friendly Bootstrap interface
- ⚡ **Fast Processing** - Efficient analysis with progress tracking
- 🛡️ **Error Handling** - Robust error management and user feedback
- 🎨 **Modern UI** - Professional gradient design with intuitive navigation



### Sentiment Categories

| Category | Score Range | Description | Color |
|----------|-------------|-------------|-------|
| 🟢 Strongly Positive | 0.6 to 1.0 | Very enthusiastic, excited tweets | Dark Green |
| 🟢 Positive | 0.3 to 0.6 | Generally positive sentiment | Green |
| 🟡 Weakly Positive | 0.0 to 0.3 | Slightly positive tone | Light Green |
| ⚪ Neutral | 0.0 | No emotional sentiment | Gold |
| 🟡 Weakly Negative | 0.0 to -0.3 | Slightly negative tone | Light Salmon |
| 🔴 Negative | -0.3 to -0.6 | Generally negative sentiment | Red |
| 🔴 Strongly Negative | -0.6 to -1.0 | Very negative, angry tweets | Dark Red |

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Twitter Developer Account
- Git (optional)


## 🔧 Configuration

### Twitter API Setup

1. **Create Twitter Developer Account**
   - Visit [Twitter Developer Portal](https://developer.twitter.com/)
   - Apply for a developer account
   - Wait for approval (typically 1-2 days)

2. **Create New App**
   - Go to Developer Portal Dashboard
   - Click "Create Project" or "Create App"
   - Fill in application details:
     - **App Name**: "Sentiment Analysis Tool"
     - **Description**: "Educational sentiment analysis application"
     - **Use Case**: Select appropriate category

3. **Generate API Keys**
   - Navigate to your app's "Keys and Tokens" section
   - Generate the following credentials:
     - API Key (Consumer Key)
     - API Secret (Consumer Secret)
     - Access Token
     - Access Token Secret

4. **Configure Application**
   
   Open `sentiment_blueprint.py` and replace the placeholder values:
   
   ```python
   # Replace these with your actual Twitter API credentials
   consumerKey = 'your_api_key_here'
   consumerSecret = 'your_api_secret_here'
   accessToken = 'your_access_token_here'
   accessTokenSecret = 'your_access_token_secret_here'
   ```

   ⚠️ **Security Note**: Never commit API keys to version control. Consider using environment variables for production.

### Environment Variables (Optional but Recommended)

Create a `.env` file in the project root:

```bash
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

Then modify `sentiment_blueprint.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

consumerKey = os.getenv('TWITTER_API_KEY')
consumerSecret = os.getenv('TWITTER_API_SECRET')
accessToken = os.getenv('TWITTER_ACCESS_TOKEN')
accessTokenSecret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
```

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the Web Interface

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Enter Analysis Parameters**:
   - **Keyword**: Enter any topic you want to analyze (e.g., "climate change", "iPhone 15", "cryptocurrency")
   - **Number of Tweets**: Specify how many tweets to analyze (recommended: 50-200)

3. **Run Analysis**: Click "Analyze Sentiment" button

4. **View Results**:
   - Overall sentiment score and classification
   - Detailed percentage breakdown by category
   - Click "View Visualization" to see the pie chart

5. **Export Data**: Analyzed tweets are automatically saved to `result.csv`

### Example Queries

| Keyword | Description | Expected Results |
|---------|-------------|------------------|
| "Python programming" | Programming language | Generally positive |
| "Monday morning" | Day of the week | Mixed/negative |
| "Coffee" | Beverage | Positive |
| "Traffic jam" | Transportation issue | Negative |
| "Vacation" | Travel/leisure | Positive |

## 📁 Project Structure

```
twitter-sentiment-analysis/
│
├── app.py                      # Main Flask application
├── sentiment_blueprint.py      # Core sentiment analysis logic
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
│
├── templates/                # HTML templates
│   ├── base.html            # Base template with common elements
│   ├── sentiment_analyzer.html # Main analysis page
│   └── piechart.html        # Visualization page
│
├── static/                   # Static files
│   ├── images/              # Generated charts and images
│   │   └── plot1.png       # Latest pie chart (auto-generated)
│   ├── css/                 # Custom stylesheets (optional)
│   └── js/                  # Custom JavaScript (optional)
│
│
└── data/                     # Data files
    ├── result.csv           # Latest analysis results (auto-generated)
    └── analysis-history/    # Historical analysis data (optional)
```

## 📚 API Reference

### Core Classes

#### `SentimentAnalysis`

Main class containing sentiment analysis logic.

**Methods:**

- `DownloadData(keyword, tweets)` - Fetches and analyzes tweets
- `cleanTweet(tweet)` - Cleans tweet text
- `percentage(part, whole)` - Calculates percentages
- `plotPieChart(...)` - Generates visualization

#### Flask Routes

- `GET /` - Redirects to main page
- `GET /sentiment_analyzer` - Main analysis page
- `POST /sentiment_logic` - Processes analysis request
- `GET /visualize` - Displays pie chart

### Configuration Parameters

| Parameter | Type | Description | Default | Range |
|-----------|------|-------------|---------|-------|
| keyword | string | Search term for tweets | None | Any valid search term |
| tweets | integer | Number of tweets to analyze | None | 1-1000 (recommended: 50-200) |
| lang | string | Tweet language | "en" | ISO language codes |
| result_type | string | Type of tweets to fetch | "recent" | recent, popular, mixed |

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Errors

**Error**: `Twitter API authentication failed`

**Solutions**:
- Verify API credentials are correct
- Check for extra spaces in keys
- Ensure Twitter app has necessary permissions
- Verify API keys are not expired

#### 2. No Tweets Found

**Error**: `No tweets found for the given keyword`

**Solutions**:
- Try more common keywords
- Reduce the number of tweets requested
- Check if keyword is too specific
- Verify Twitter API rate limits

#### 3. Import Errors

**Error**: `ModuleNotFoundError: No module named 'tweepy'`

**Solutions**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
# Or install specific package:
pip install tweepy==4.14.0
```

#### 4. Chart Display Issues

**Error**: Chart not showing in visualization

**Solutions**:
- Ensure `static/images/` directory exists
- Check matplotlib backend configuration
- Verify sufficient disk space
- Try running analysis again

#### 5. Rate Limit Exceeded

**Error**: `Rate limit exceeded`

**Solutions**:
- Wait 15 minutes before retrying
- Reduce number of tweets
- Consider upgrading Twitter API plan
- Implement request queuing

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In app.py
app.run(debug=True)
```

### Logging

Add logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Testing

### Manual Testing

1. **Test with known keywords**:
   ```
   Positive: "vacation", "coffee", "success"
   Negative: "traffic", "monday", "taxes"
   Neutral: "weather", "news", "information"
   ```

2. **Test different tweet counts**:
   - Small dataset: 10-20 tweets
   - Medium dataset: 50-100 tweets
   - Large dataset: 200-500 tweets

3. **Test edge cases**:
   - Very specific keywords
   - Keywords with special characters
   - Non-English keywords (if supported)

### Unit Tests (Future Enhancement)

```bash
# Run tests (when implemented)
python -m pytest tests/
```

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

#### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

#### Environment Variables for Production

```bash
export FLASK_ENV=production
export TWITTER_API_KEY=your_key
export TWITTER_API_SECRET=your_secret
# ... other variables
```

### Deployment Platforms

- **Heroku**: Easy deployment with git integration
- **AWS EC2**: Full control over server environment
- **DigitalOcean**: Simple droplet deployment
- **Google Cloud Platform**: Scalable cloud hosting



### Development Guidelines

- Follow PEP 8 Python style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write clear commit messages
- Update documentation for new features


## 📈 Roadmap

### Version 2.0 (Planned)

- [ ] User authentication and profiles
- [ ] Historical analysis tracking
- [ ] Comparison between keywords
- [ ] Advanced filtering options
- [ ] Real-time streaming analysis
- [ ] API endpoints for developers
- [ ] Mobile app integration

### Version 2.1 (Future)

- [ ] Machine learning model training
- [ ] Multi-language support
- [ ] Advanced visualizations (word clouds, trends)
- [ ] Integration with other social platforms
- [ ] Automated report generation
- [ ] Email notifications for sentiment changes

## 🙏 Acknowledgments

- **TextBlob** - For providing excellent sentiment analysis capabilities
- **Twitter API** - For access to real-time tweet data
- **Flask** - For the lightweight and flexible web framework
- **Bootstrap** - For the responsive UI components
- **Matplotlib** - For beautiful data visualizations
- **GeeksforGeeks** - For the original tutorial inspiration



---

**Built with ❤️ by [Your Name](https://github.com/vishwastiwarig)**

