from flask import Flask,render_template,request
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai

api = os.getenv("API_KEY")
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()
