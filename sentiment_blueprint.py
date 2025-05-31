from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
import os
import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web deployment

# Register this file as a blueprint
second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@second.route("/sentiment_analyzer")
def sentiment_analyzer():
    """Main page for sentiment analysis"""
    return render_template("sentiment_analyzer.html")

class SentimentAnalysis:
    """Main class containing sentiment analysis logic"""
    
    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, keyword, tweets):
        """
        Download tweets and perform sentiment analysis
        
        Args:
            keyword (str): Search keyword for tweets
            tweets (str): Number of tweets to analyze
            
        Returns:
            tuple: Analysis results including polarity, sentiment labels, and percentages
        """
        
        # Twitter API credentials - Replace with your actual credentials
        # Get these from https://developer.twitter.com/
        consumerKey = 'YOUR_CONSUMER_KEY_HERE'
        consumerSecret = 'YOUR_CONSUMER_SECRET_HERE'
        accessToken = 'YOUR_ACCESS_TOKEN_HERE'
        accessTokenSecret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'
        
        # Check if credentials are still placeholders
        if consumerKey == 'YOUR_CONSUMER_KEY_HERE':
            raise Exception("Please update your Twitter API credentials in sentiment_blueprint.py")
        
        try:
            # Authenticate with Twitter API
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Verify credentials
            api.verify_credentials()
            print("✅ Twitter API authentication successful")
            
        except Exception as e:
            raise Exception(f"Twitter API authentication failed: {str(e)}")
        
        tweets = int(tweets)
        
        try:
            # Search for tweets using the updated API method
            self.tweets = tweepy.Cursor(
                api.search_tweets, 
                q=keyword, 
                lang="en",
                result_type="recent",
                tweet_mode="extended"  # Get full text
            ).items(tweets)
            
            print(f"🔍 Searching for {tweets} tweets with keyword: '{keyword}'")
            
        except Exception as e:
            raise Exception(f"Error searching tweets: {str(e)}")
        
        # Create/open CSV file for storing results
        try:
            csvFile = open('result.csv', 'w', newline='', encoding='utf-8')
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(['Tweet Text', 'Polarity', 'Sentiment'])  # Header
        except Exception as e:
            raise Exception(f"Error creating CSV file: {str(e)}")
        
        # Initialize sentiment counters
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        processed_tweets = 0
        
        try:
            # Process each tweet
            for tweet in self.tweets:
                # Get tweet text (handle both standard and extended tweets)
                tweet_text = getattr(tweet, 'full_text', tweet.text)
                
                # Clean the tweet text
                cleaned_tweet = self.cleanTweet(tweet_text)
                self.tweetText.append(cleaned_tweet)
                
                # Perform sentiment analysis using TextBlob
                analysis = TextBlob(tweet_text)
                tweet_polarity = analysis.sentiment.polarity
                polarity += tweet_polarity
                
                # Categorize sentiment based on polarity score
                if tweet_polarity == 0:
                    neutral += 1
                    sentiment_label = "Neutral"
                elif 0 < tweet_polarity <= 0.3:
                    wpositive += 1
                    sentiment_label = "Weakly Positive"
                elif 0.3 < tweet_polarity <= 0.6:
                    positive += 1
                    sentiment_label = "Positive"
                elif 0.6 < tweet_polarity <= 1:
                    spositive += 1
                    sentiment_label = "Strongly Positive"
                elif -0.3 < tweet_polarity <= 0:
                    wnegative += 1
                    sentiment_label = "Weakly Negative"
                elif -0.6 < tweet_polarity <= -0.3:
                    negative += 1
                    sentiment_label = "Negative"
                elif -1 < tweet_polarity <= -0.6:
                    snegative += 1
                    sentiment_label = "Strongly Negative"
                else:
                    neutral += 1
                    sentiment_label = "Neutral"
                
                # Write to CSV
                csvWriter.writerow([cleaned_tweet, tweet_polarity, sentiment_label])
                processed_tweets += 1
                
                # Progress indicator for large datasets
                if processed_tweets % 10 == 0:
                    print(f"📊 Processed {processed_tweets} tweets...")
            
            csvFile.close()
            print(f"✅ Successfully processed {processed_tweets} tweets")
            
        except Exception as e:
            csvFile.close()
            raise Exception(f"Error processing tweets: {str(e)}")
        
        # Ensure we have tweets to analyze
        if processed_tweets == 0:
            raise Exception("No tweets found for the given keyword. Try a different keyword or check your API limits.")
        
        # Calculate percentages
        positive = self.percentage(positive, processed_tweets)
        wpositive = self.percentage(wpositive, processed_tweets)
        spositive = self.percentage(spositive, processed_tweets)
        negative = self.percentage(negative, processed_tweets)
        wnegative = self.percentage(wnegative, processed_tweets)
        snegative = self.percentage(snegative, processed_tweets)
        neutral = self.percentage(neutral, processed_tweets)
        
        # Calculate overall polarity
        overall_polarity = polarity / processed_tweets if processed_tweets > 0 else 0
        
        # Determine overall sentiment label
        if overall_polarity == 0:
            htmlpolarity = "Neutral"
        elif 0 < overall_polarity <= 0.3:
            htmlpolarity = "Weakly Positive"
        elif 0.3 < overall_polarity <= 0.6:
            htmlpolarity = "Positive"
        elif 0.6 < overall_polarity <= 1:
            htmlpolarity = "Strongly Positive"
        elif -0.3 < overall_polarity <= 0:
            htmlpolarity = "Weakly Negative"
        elif -0.6 < overall_polarity <= -0.3:
            htmlpolarity = "Negative"
        elif -1 < overall_polarity <= -0.6:
            htmlpolarity = "Strongly Negative"
        else:
            htmlpolarity = "Neutral"
        
        # Generate pie chart visualization
        self.plotPieChart(positive, wpositive, spositive, negative,
                         wnegative, snegative, neutral, keyword, processed_tweets)
        
        print(f"📈 Overall sentiment: {htmlpolarity} (Polarity: {overall_polarity:.3f})")
        
        return (overall_polarity, htmlpolarity, positive, wpositive, spositive, 
                negative, wnegative, snegative, neutral, keyword, processed_tweets)

    def cleanTweet(self, tweet):
        """
        Clean tweet text by removing URLs, mentions, and special characters
        
        Args:
            tweet (str): Raw tweet text
            
        Returns:
            str: Cleaned tweet text
        """
        # Remove URLs, mentions (@username), and special characters
        cleaned = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|#", " ", tweet)
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned

    def percentage(self, part, whole):
        """
        Calculate percentage with 2 decimal places
        
        Args:
            part (int): Part value
            whole (int): Whole value
            
        Returns:
            str: Formatted percentage
        """
        if whole == 0:
            return "0.00"
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets):
        """
        Generate and save pie chart visualization
        
        Args:
            positive, wpositive, spositive, negative, wnegative, snegative, neutral: Sentiment percentages
            keyword (str): Search keyword
            tweets (int): Number of tweets analyzed
        """
        try:
            # Create figure with better size and DPI
            plt.figure(figsize=(12, 8))
            
            # Prepare data for pie chart
            labels = [
                f'Positive [{positive}%]',
                f'Weakly Positive [{wpositive}%]',
                f'Strongly Positive [{spositive}%]',
                f'Neutral [{neutral}%]',
                f'Negative [{negative}%]',
                f'Weakly Negative [{wnegative}%]',
                f'Strongly Negative [{snegative}%]'
            ]
            
            sizes = [float(positive), float(wpositive), float(spositive), 
                    float(neutral), float(negative), float(wnegative), float(snegative)]
            
            colors = ['#32CD32', '#9ACD32', '#228B22', '#FFD700', '#FF6347', '#FF4500', '#DC143C']
            
            # Filter out zero values for cleaner chart
            non_zero_data = [(size, label, color) for size, label, color in zip(sizes, labels, colors) if size > 0]
            
            if non_zero_data:
                sizes, labels, colors = zip(*non_zero_data)
                
                # Create pie chart
                wedges, texts = plt.pie(sizes, colors=colors, startangle=90, 
                                      autopct='%1.1f%%', shadow=True)
                
                # Add title and legend
                plt.title(f'Sentiment Analysis for "{keyword}"\n({tweets} tweets analyzed)', 
                         fontsize=16, fontweight='bold', pad=20)
                plt.legend(wedges, labels, title="Sentiment Categories", 
                         loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                plt.axis('equal')
                
            else:
                # Handle case where all values are zero
                plt.text(0.5, 0.5, 'No sentiment data available', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=plt.gca().transAxes, fontsize=16)
                plt.title(f'Sentiment Analysis for "{keyword}" - No Data', fontsize=16)
            
            # Ensure directory exists
            os.makedirs('static/images', exist_ok=True)
            
            # Save the plot
            plot_path = 'static/images/plot1.png'
            if os.path.isfile(plot_path):
                os.remove(plot_path)
            
            plt.tight_layout()
            plt.savefig(plot_path, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()  # Close to free memory
            
            print("📊 Pie chart saved successfully")
            
        except Exception as e:
            print(f"⚠️ Error creating pie chart: {str(e)}")

@second.route('/sentiment_logic', methods=['POST'])
def sentiment_logic():
    """Handle sentiment analysis form submission"""
    try:
        # Get form data
        keyword = request.form.get('keyword', '').strip()
        tweets = request.form.get('tweets', '').strip()
        
        # Validate input
        if not keyword:
            return render_template('sentiment_analyzer.html', 
                                 error="Please enter a keyword to search for.")
        
        if not tweets:
            return render_template('sentiment_analyzer.html', 
                                 error="Please enter the number of tweets to analyze.")
        
        try:
            tweet_count = int(tweets)
            if tweet_count <= 0:
                raise ValueError("Number must be positive")
            if tweet_count > 1000:
                return render_template('sentiment_analyzer.html', 
                                     error="Please enter a number less than 1000 to avoid API limits.")
        except ValueError:
            return render_template('sentiment_analyzer.html', 
                                 error="Please enter a valid positive number for tweets.")
        
        # Perform sentiment analysis
        print(f"🚀 Starting analysis for keyword: '{keyword}' with {tweets} tweets")
        
        sa = SentimentAnalysis()
        
        (polarity, htmlpolarity, positive, wpositive, spositive, 
         negative, wnegative, snegative, neutral, keyword1, tweet1) = sa.DownloadData(keyword, tweets)
        
        # Return results
        return render_template('sentiment_analyzer.html', 
                             polarity=polarity, 
                             htmlpolarity=htmlpolarity, 
                             positive=positive,
                             wpositive=wpositive, 
                             spositive=spositive, 
                             negative=negative, 
                             wnegative=wnegative,
                             snegative=snegative, 
                             neutral=neutral, 
                             keyword=keyword1, 
                             tweets=tweet1,
                             analysis_complete=True)
    
    except Exception as e:
        error_message = str(e)
        print(f"❌ Error in sentiment analysis: {error_message}")
        return render_template('sentiment_analyzer.html', error=error_message)

@second.route('/visualize')
def visualize():
    """Display the pie chart visualization"""
    # Check if chart exists
    chart_path = 'static/images/plot1.png'
    if not os.path.exists(chart_path):
        return render_template('sentiment_analyzer.html', 
                             error="No visualization available. Please run an analysis first.")
    
    return render_template('piechart.html')