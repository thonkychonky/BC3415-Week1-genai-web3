from flask import Flask,render_template,request
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai
from textblob import TextBlob

api = os.getenv("API_KEY")

genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

def analyze_sentiment(sentence):
    analysis = TextBlob(sentence)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

@app.route("/ai_agent_reply", methods=["GET","POST"])
def ai_agent_reply():
     # Get the user's question from the form
    q = request.form.get("q")
    
    # Generate a response using Gemini
    response = model.generate_content(q)

    # Extract the generated text from the response
    r = response.text
    
    # Render the response in the ai_agent_reply.html template
    return render_template("ai_agent_reply.html", r=r)

@app.route("/prediction", methods=["GET","POST"])
def prediction():
    return(render_template("index.html"))

@app.route("/sg_joke", methods=["GET","POST"])
def sg_joke():
    joke = None  # Initialize joke as None
    
    if request.method == "POST":
        # When the form is submitted, set the joke
        joke = "The only thing faster than Singapore's MRT during peak hours is the way we 'chope' seats with a tissue packet."
    
    return render_template("index.html", joke=joke)

@app.route("/sentiment_analysis", methods=["GET", "POST"])
def sentiment_analysis():
    sentiment = None
    if request.method == "POST":
        sentence = request.form.get("sentence")  # Get the sentence from the form
        if sentence:  # Check if the sentence is not None or empty
            try:
                sentiment = analyze_sentiment(sentence)  # Analyze the sentiment
            except Exception as e:
                print(f"Error during sentiment analysis: {e}")
                sentiment = "An error occurred during analysis."
        else:
            sentiment = "Please enter a sentence."  # Provide feedback for empty input

    # Render the template with the sentiment result
    return render_template("sentiment_analysis.html", sentiment=sentiment)

@app.route("/paynow", methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))


if __name__ == "__main__":
    app.run()
