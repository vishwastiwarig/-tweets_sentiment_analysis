from flask import Flask, redirect
from sentiment_blueprint import second

app = Flask(__name__)

# Register the sentiment analysis blueprint
app.register_blueprint(second)

@app.route('/')
def index():
    """Redirect to the main sentiment analyzer page"""
    return redirect('/sentiment_analyzer')

if __name__ == '__main__':
    # Create static directories if they don't exist
    import os
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Starting Twitter Sentiment Analysis App...")
    print("📊 Navigate to http://localhost:5000 to use the application")
    print("⚠️  Remember to update your Twitter API credentials in sentiment_blueprint.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000)