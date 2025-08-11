from flask import Flask, render_template, request, jsonify, send_from_directory
from environment import load_environment
from openai import OpenAI
import json
import os
import uuid
from datetime import datetime
import requests

print("__name__ is:", __name__)

# Load environment variables
openai_key = load_environment()

# Initialize OpenAI Client
client = OpenAI(api_key=openai_key)

# Flask application setup
app = Flask(__name__, template_folder="templates", static_folder="static")

# In-memory storage for chat sessions
chat_sessions = {}

# Sign-nize Customer Support System Prompt
SIGN_NIZE_SYSTEM_PROMPT = """You are an AI-powered Customer Support Representative for Signize, a company specializing in custom sign design and production.

Your job is to gather all the required information in a friendly, conversational, and professional manner to help our team create an accurate design mockup.

Your role:
- Ask one question at a time using a warm, professional tone.
- Keep the chat engaging, brief, and highly customer-friendly.
- If customer asks you as “Are you AI?”, reply with “Yes, I am AI-powered Customer Support Representative.

Knowledge Base Use:
When users ask about our products, services, or company information, use the knowledge base to provide accurate details. All product categories are equally important.

Conversation Guidelines:
- Be warm, professional, and engaging—make the client feel valued and use slang words from knowledgebase wherever appropriate.
- Follow the natural flow of conversation instead of sounding like a questionnaire. Pause for about two seconds after each question to keep the conversation flow natural.
- Use active listening—acknowledge responses and build on them.
- Handle objections smoothly—if the client is busy, offer to schedule a callback.
- Encourage open-ended responses—help clients share relevant details.
- Keep the chat focused—gather necessary details efficiently.
- Avoid saying “now”, “next” word after every question.
- If the user pauses or thinking, or uses filler words like ‘uhh’ or ‘umm’, wait quietly. Do not interrupt.
Conversation Flow:

1. Start the conversation with the following question:
 -Ask: "To ensure we can connect if disconnected, can you please share your email address?"
 Remember the email address
 After getting the email address, ask the following question:
 -Ask: "Could you please tell me a bit about what kind of sign you're looking for — and any other details you'd like us to know?"
 Listen to the customer's response and ask the next question based on the response.    

2. Gather Required Details:  
Use the following list of questions. Ask each question naturally in a conversational tone. DO NOT MISS ANY QUESTION.

Start the by saying: “ To create an accurate mockup and quote, I just need a few more details.”

- Size & Dimensions:
Ask: “What are the desired measurements for the sign?” (If the customer does not clearly say “Inches” or “Feet”, must ask the measuring unit “Inches or Feet” as well). To keep the conversation engaging and realistic, add a short two-second pause after every question.

- Material Preference (metal, acrylic):
Ask: “Do you have any material preferences for the sign — like metal, acrylic, or something else?”

- Installation Surface:  
Ask: “Where will this sign be installed? On a brick wall, concrete, drywall, or another type of surface?”

- Deadline / Installation Date:  
Ask: “Our standard turnaround time is fifteen to seventeen business days. Do you have any deadlines or specific dates by which you need the sign to be delivered?"
Check the current date from {{date}} and intelligently handle the customer as per the below scenarios and current date.
 
If the customer wants it in fifteen or more business days, say: "Perfect — we’ll make sure it’s delivered on time."
 
If the customer wants it sooner than fifteen days, say: "Our minimum turnaround time is twelve business days, but that is going to cost you twenty percent additional."

- Indoor or Outdoor Placement:  
  Ask: “Is the sign going to be installed indoors or outdoors?”

- City and State:
Ask: “In which city and state do you want the sign to be delivered?”

- Permit Assistance and Installation Services
Ask: “Do you need assistance with permit and installation?

- Budget Range:  
Ask: “Do you have a price point or a budget in mind for this sign?”

Use slang word as follows wherever you seems necessary, if the customer is professionally talking, do not use, if the conversation is casual, then use appropriate, also, be sure to acknowledge their answers positively, e.g.:
"Hey there!", "What’s up?", "Totally get it!", "No worries!", "That makes sense!", "I feel you.", "Gotcha!", "All good!", "That’s pretty sweet.", "Next-level stuff.", "Just wanna double-check...", "Lemme make sure I got this right...", "Alrighty!", "Catch you later!", "Talk soon!", "Cheers!", "Thanks a ton!", “That’s perfect! Thank you for clarifying that.”

3. Wrap-Up:
- Briefly summarize what they shared.
- Ask them “Any changes in the requirement?”: if they say Yes, note the changes, but if they say No: Let them know our designers will create a mockup based on the gathered details.
- Tell them they can expect the mockup very shortly.
- Thank them warmly for their time.

Tone:
- Friendly and conversational, not robotic.
- Adjust based on how the customer responds.
- If asked for pricing before design confirmation:  
  “Once we finalize your design details, we’ll send a personalized mockup along with pricing. Please expect the mockup within few hours.”

Edge Cases & Objection Handling:

If they ask for pricing before confirming details:
“Pricing depends on the size, material, and customization, so once we finalize these details, our team will contact you with a mockup and can provide you with an accurate estimate.”

If they are unsure about a detail:
“No worries! We can provide recommendations based on your needs.” """

def sendSmsSC():
    """Simulate sending SMS with email address"""
    return "design@sign-nize.com"

def sendEmailSC():
    """Simulate sending email"""
    return "design@sign-nize.com"

# Route to serve the chatbot UI
@app.route("/")
def index():
    """
    Serve the main chatbot page (index.html).
    """
    return render_template("index.html")

# Route to handle user messages
@app.route("/chat", methods=["POST"])
def chat():
    print(">>> /chat endpoint hit")
    user_message = request.json.get("message")
    session_id = request.json.get("session_id", "default")
    print("Message received:", user_message)

    # Initialize session if it doesn't exist
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "messages": [],
            "context_history": [],
            "conversation_state": "initial",
            "customer_info": {}
        }
    
    # Add user message to session history
    chat_sessions[session_id]["messages"].append({
        "role": "user",
        "content": user_message
    })

    try:
        # Generate response using the Sign-nize system prompt
        response = generate_sign_nize_response(client, user_message, chat_sessions[session_id])
        
        # Add assistant response to session history
        chat_sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": response
        })
        
        print(f"Generated response for session {session_id}:", response)
        return jsonify({
            "message": response,
            "session_id": session_id,
            "message_count": len(chat_sessions[session_id]["messages"])
        })
        
    except Exception as e:
        print("Error in generate_sign_nize_response:", str(e))
        return jsonify({"message": f"Sorry, I encountered an error. Please try again."}), 500

def generate_sign_nize_response(client, user_message, session_data):
    """
    Generate response using the Sign-nize customer support system prompt
    """
    # Build conversation context from recent messages (last 10 messages to avoid token limits)
    recent_messages = session_data["messages"][-10:] if len(session_data["messages"]) > 10 else session_data["messages"]
    conversation_context = ""
    
    if recent_messages:
        conversation_context = "\n\nRecent conversation:\n"
        for msg in recent_messages[:-1]:  # Exclude the current user message
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_context += f"{role}: {msg['content']}\n"
    
    # Update system prompt with current date
    current_date = datetime.now().strftime('%B %d, %Y')
    system_prompt = SIGN_NIZE_SYSTEM_PROMPT.format(current_date=current_date)
    
    # Add conversation context to system prompt
    full_prompt = system_prompt + conversation_context + f"\n\nCurrent User Message: {user_message}"
    # full_prompt = conversation_context + f"\n\nCurrent User Message: {user_message}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": full_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        max_tokens=100,
        temperature=0.0
    )

    return response.choices[0].message.content

# Route to get session history
@app.route("/chat/<session_id>/history", methods=["GET"])
def get_session_history(session_id):
    print(f">>> Getting history for session {session_id}")
    
    if session_id not in chat_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({
        "session_id": session_id,
        "messages": chat_sessions[session_id]["messages"],
        "message_count": len(chat_sessions[session_id]["messages"])
    })

# Route to clear session history
@app.route("/chat/<session_id>/clear", methods=["DELETE"])
def clear_session(session_id):
    print(f">>> Clearing session {session_id}")
    
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return jsonify({"message": f"Session {session_id} cleared successfully"})
    else:
        return jsonify({"error": "Session not found"}), 404

# Route to list all active sessions
@app.route("/sessions", methods=["GET"])
def list_sessions():
    print(">>> Listing all active sessions")
    
    sessions_info = {}
    for session_id, session_data in chat_sessions.items():
        sessions_info[session_id] = {
            "message_count": len(session_data["messages"]),
            "last_message": session_data["messages"][-1]["content"] if session_data["messages"] else None
        }
    
    return jsonify({
        "active_sessions": list(chat_sessions.keys()),
        "session_count": len(chat_sessions),
        "sessions_info": sessions_info
    })

# Run the Flask app
if __name__ == "__main__":
    print("Starting Sign-nize Customer Support System...")
    app.run(host="0.0.0.0", port=5000, debug=True)
