import os
import json
from flask import render_template, request, jsonify, g, flash, redirect, url_for, session
from app.db import get_db
from app.auth.routes import login_required
from app.ai import bp
import google.generativeai as genai

# Setup Gemini API configuration
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def get_open_shelters():
    db = get_db()
    shelters = db.execute(
        'SELECT * FROM shelters WHERE status = "Open"'
    ).fetchall()
    return [dict(row) for row in shelters]

def call_gemini_guidance(prompt_content, system_context=None):
    if not model:
        # Graceful fallback response if API key is not configured
        return (
            "**[System Notice: Gemini API Key is not set in your .env file. Showing mock disaster guidance.]**\n\n"
            "Here are the safety guidelines for your request:\n"
            "1. **Stay Informed**: Listen to radio or local news updates.\n"
            "2. **Evacuate if Instructed**: If local authorities advise evacuation, do so immediately.\n"
            "3. **Emergency Kit**: Keep water, non-perishable foods, first-aid, and flashlights handy.\n"
            "4. **Avoid Hazard Areas**: Do not walk or drive through flooded areas or near active hazards."
        )
    
    try:
        full_prompt = prompt_content
        if system_context:
            full_prompt = f"{system_context}\n\nUser Query: {prompt_content}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error contacting AI services: {str(e)}"

@bp.route('/chat', methods=('GET', 'POST'))
@login_required
def chat():
    if request.method == 'POST':
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'response': 'Message cannot be empty.'}), 400
        
        # 1. Intent Detection: Check if user is asking for shelters
        shelter_keywords = ['shelter', 'safe house', 'refuge', 'accommodation', 'housing', 'stay', 'where to go']
        contains_shelter_query = any(kw in user_message.lower() for kw in shelter_keywords)
        
        system_context = (
            "You are ResQLink's AI Emergency Response Agent. You provide clear, concise, and structured safety "
            "guidance. Prioritize human safety and list sequential actionable steps."
        )
        
        if contains_shelter_query:
            # Query the database only
            open_shelters = get_open_shelters()
            
            # Format the database shelters into the context for Gemini
            shelter_list_str = ""
            for s in open_shelters:
                capacity_left = s['capacity'] - s['current_occupancy']
                shelter_list_str += f"- Name: {s['name']}, Location: {s['location']}, Space Left: {capacity_left} spots, Coordinates: {s['latitude']}, {s['longitude']}\n"
            
            system_context += (
                "\nCRITICAL: The user is asking about emergency shelters. You MUST ONLY recommend the shelters listed below, "
                "which are fetched from our database. DO NOT fabricate, hallucinate, or assume any other shelter locations.\n"
                f"Available open shelters in database:\n{shelter_list_str if shelter_list_str else 'No open shelters currently available.'}\n"
                "If no shelters are available, instruct them to wait for official dispatch or move to high ground."
            )

        ai_response = call_gemini_guidance(user_message, system_context)
        return jsonify({'response': ai_response})

    return render_template('ai/chat.html')

@bp.route('/checklist', methods=('GET', 'POST'))
@login_required
def checklist():
    checklist_content = None
    selected_disaster = None
    
    if request.method == 'POST':
        selected_disaster = request.form.get('disaster_type')
        if selected_disaster:
            prompt = (
                f"Generate a detailed, step-by-step emergency checklist for preparation and evacuation during a {selected_disaster}. "
                "Structure it into 'Pre-Disaster Setup', 'Immediate Evacuation Actions', and 'Post-Disaster Safety'. "
                "Keep bullet points short, high-priority, and direct."
            )
            checklist_content = call_gemini_guidance(prompt)
            
    return render_template('ai/checklist.html', checklist=checklist_content, disaster=selected_disaster)
