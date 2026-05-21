import os
import requests
import streamlit as st
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Streamlit Page Configuration
st.set_page_config(
    page_title="PhoneDoctor AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling & Theme Override
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Fonts and Background */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background: radial-gradient(circle at 10% 20%, #0d131f 0%, #07090d 90%);
        color: #e2e8f0;
    }

    /* Style the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Center header inside Sidebar */
    .sidebar-header {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }

    /* Custom Header Dashboard */
    .header-container {
        display: flex;
        align-items: center;
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }
    
    .header-logo {
        font-size: 38px;
        margin-right: 20px;
        background: rgba(16, 185, 129, 0.12);
        border: 2px solid #10b981;
        border-radius: 50%;
        width: 65px;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.35);
        animation: pulse-glow 2.5s infinite alternate;
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
        100% { box-shadow: 0 0 25px rgba(16, 185, 129, 0.7); }
    }
    
    .header-text h1 {
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 34px;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2;
    }
    
    .header-text p {
        color: #94a3b8;
        margin: 5px 0 0 0 !important;
        font-size: 14px;
        font-weight: 300;
    }

    /* Connection Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 5px;
    }
    .status-online {
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .status-offline {
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        display: inline-block;
    }
    .status-online .status-dot { background-color: #10b981; box-shadow: 0 0 8px #10b981; }
    .status-offline .status-dot { background-color: #ef4444; box-shadow: 0 0 8px #ef4444; }

    /* Custom Chat Container (Glassmorphic) */
    .chat-bubble {
        border-radius: 18px;
        padding: 14px 20px;
        margin: 8px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        font-size: 15.5px;
        line-height: 1.6;
        animation: bubble-fade 0.35s ease-out;
        max-width: 85%;
    }
    
    @keyframes bubble-fade {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-bubble-bot {
        background: rgba(22, 30, 49, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.15);
        color: #f1f5f9;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }

    .chat-avatar {
        font-size: 20px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        font-size: 13px;
        color: #94a3b8;
    }

    /* Typing Indicator Pulse Animation */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 15px 25px;
        background: rgba(22, 30, 49, 0.6);
        border: 1px solid rgba(16, 185, 129, 0.12);
        border-radius: 18px;
        border-bottom-left-radius: 4px;
        margin-top: 8px;
        width: fit-content;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse-dot 1.4s infinite ease-in-out both;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes pulse-dot {
        0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* Word Pill tags in sidebar */
    .word-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin: 3px;
        color: #cbd5e1;
    }

    /* Proximity Care Cards styling */
    .clinic-card {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s, border-color 0.2s;
    }
    
    .clinic-card:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .clinic-name {
        color: #ffffff;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 4px;
        line-height: 1.3;
    }
    
    .clinic-type {
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .type-hospital { background: rgba(239, 68, 68, 0.12); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    .type-clinic { background: rgba(59, 130, 246, 0.12); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.2); }
    .type-doctors { background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
    .type-facility { background: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
    
    .clinic-address {
        color: #94a3b8;
        font-size: 13.5px;
        line-height: 1.45;
        margin-bottom: 15px;
    }
    
    .map-btn {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981 !important;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 12.5px;
        font-weight: 500;
        text-decoration: none !important;
        transition: background 0.2s;
    }
    
    .map-btn:hover {
        background: rgba(16, 185, 129, 0.22);
        color: #10b981 !important;
        text-decoration: none !important;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# --- Helper Functions ---

def get_gemini_api_key():
    """Gets the Gemini API key, prioritizing Streamlit Secrets for cloud deployment, falling back to local environment variables."""
    try:
        # Check Streamlit secrets first (for Streamlit Community Cloud)
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # Fallback to local environment variables
    return os.getenv("GEMINI_API_KEY")


def get_coordinates(location_name):
    """Converts a location name (e.g. city) to lat/lon using OSM Nominatim API."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location_name, "format": "json", "limit": 1}
        headers = {"User-Agent": "PhoneDoctorAI/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=6.0)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()[0]
            return float(data["lat"]), float(data["lon"]), data.get("display_name", location_name)
    except Exception:
        pass
    return None


def get_nearby_medical_facilities(lat, lon, radius=15000):
    """Queries OSM Overpass API for hospitals, clinics, and doctors within a specific radius (default 15km)."""
    print(f"📡 Querying nearby medical facilities for Lat: {lat}, Lon: {lon}, Radius: {radius}m...")
    try:
        url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json][timeout:15];
        (
          node["amenity"="hospital"](around:{radius},{lat},{lon});
          node["amenity"="clinic"](around:{radius},{lat},{lon});
          node["amenity"="doctors"](around:{radius},{lat},{lon});
          way["amenity"="hospital"](around:{radius},{lat},{lon});
          way["amenity"="clinic"](around:{radius},{lat},{lon});
          relation["amenity"="hospital"](around:{radius},{lat},{lon});
          relation["amenity"="clinic"](around:{radius},{lat},{lon});
        );
        out body center;
        """
        response = requests.post(url, data={"data": query}, timeout=15.0)
        print("Overpass Response Code:", response.status_code)
        if response.status_code == 200:
            elements = response.json().get("elements", [])
            print(f"Found {len(elements)} raw OSM elements.")
            facilities = []
            for el in elements:
                tags = el.get("tags", {})
                name = tags.get("name", tags.get("operator", "Medical Facility"))
                amenity = el.get("tags", {}).get("amenity", "Facility").lower()
                
                # Resolve coordinates
                facility_lat = el.get("lat") or el.get("center", {}).get("lat")
                facility_lon = el.get("lon") or el.get("center", {}).get("lon")
                
                # Construct address details
                street = tags.get("addr:street", "")
                housenumber = tags.get("addr:housenumber", "")
                suburb = tags.get("addr:suburb", tags.get("addr:neighbourhood", ""))
                city = tags.get("addr:city", "")
                
                address = ", ".join(filter(None, [housenumber, street, suburb, city]))
                if not address:
                    address = "Proximity search address details not provided"
                    
                facilities.append({
                    "name": name,
                    "type": amenity,
                    "address": address,
                    "lat": facility_lat,
                    "lon": facility_lon
                })
            print(f"Processed {len(facilities)} facilities.")
            return facilities
        else:
            print("Overpass Response Content Error:", response.text)
    except Exception as e:
        print("Overpass Query Exception occurred:", str(e))
    return []


def get_direct_gemini_response(api_key, prompt, image_bytes=None, image_mime=None):
    """Calls Gemini API directly using identical logic, filtering, and prompts as main.py."""
    if not api_key:
        return "System Configuration Error: Gemini API Key is missing. Please add GEMINI_API_KEY in your .env file."

    # Healthcare filter (only check if we don't have an image report, because an uploaded report is inherently health-related)
    if not image_bytes:
        healthcare_words = ["health", "pain", "fever", "medicine", "disease", "injury", "symptom", "cough", "doctor"]
        if not any(word in prompt.lower() for word in healthcare_words):
            return (
                "💡 **I can only help with healthcare-related topics.**\n\n"
                "To receive symptom advice or medical information, please make sure your query contains at least one health-related term.\n\n"
                "**Supported keywords include:** *pain, fever, symptom, medicine, injury, cough, doctor, disease, health*.\n\n"
                "*Example: Instead of 'How to treat a burn?', try: 'What is the treatment for **pain** or **injury** from a burn?'*"
            )

    # Gemini API payload (multimodal compatible)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    parts = []
    
    # If image report is uploaded, convert to inline base64 data
    if image_bytes:
        import base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        parts.append({
            "inlineData": {
                "mimeType": image_mime,
                "data": base64_image
            }
        })
        
    # Append clinical prompt
    parts.append({
        "text": f"You are a healthcare assistant. Analyze the materials and query: {prompt or 'Transcribe this medical report/prescription, extract symptoms or medications, explain their purposes, and detail important precautions and warnings.'}"
    })
    
    payload = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30.0)
        if not response.ok:
            return "Server error: Unable to process request directly with Gemini API."
        
        data = response.json()
        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            reply = "I couldn't understand the response from the AI."
        return reply
    except Exception as e:
        return f"Direct Connection Error: {str(e)}"


def process_message(prompt, image_bytes=None, image_mime=None):
    """Saves user query, simulates typing, queries the model, and updates chat history."""
    display_prompt = prompt
    if image_bytes:
        display_prompt = f"📁 *[Attached Medical Image/Report]*\n\n{prompt or 'Analyzing uploaded medical image/report...'}"

    # 1. Store user query in session state
    st.session_state.messages.append({"role": "user", "content": display_prompt})
    
    # 2. Render typing indicator dynamically
    typing_indicator = st.empty()
    typing_indicator.markdown("""
    <div class="chat-avatar">🩺 PhoneDoctor AI</div>
    <div class="typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Request Gemini API Response
    api_key = get_gemini_api_key()
    reply = get_direct_gemini_response(api_key, prompt, image_bytes, image_mime)
    
    # 4. Remove typing indicator
    typing_indicator.empty()
    
    # 5. Store bot reply in session state
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()


# --- Application Layout & Sidebar ---

# Sidebar Title/Logo
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style='color:#10b981; margin:0; font-weight:700;'>🏥 PhoneDoctor</h2>
        <span style='color:#94a3b8; font-size:12px;'>AI Assistant Workspace</span>
    </div>
    """, unsafe_allow_html=True)

    # API Link Status Section
    st.markdown("### 🔌 Link Status", unsafe_allow_html=True)
    
    gemini_api_key = get_gemini_api_key()
    
    if gemini_api_key:
        st.markdown("""
        <div class="status-badge status-online">
            <span class="status-dot"></span>Gemini Link: Connected
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-badge status-offline">
            <span class="status-dot"></span>Gemini Link: Disconnected
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 Add `GEMINI_API_KEY` to your Streamlit secrets or local `.env` file to connect.")

    # Clear Chat History Button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI PhoneDoctor assistant. How can I help with your health-related symptoms or medical queries today?"}
        ]
        st.rerun()

    # Healthcare Filter Word Showcase
    st.markdown("---")
    st.markdown("### 📋 Supported Medical Triggers")
    st.markdown("To get advice, your query must contain at least one medical-related keyword:")
    triggers = ["health", "pain", "fever", "medicine", "disease", "injury", "symptom", "cough", "doctor"]
    pills_html = "".join([f"<span class='word-pill'>{t}</span>" for t in triggers])
    st.markdown(pills_html, unsafe_allow_html=True)


# --- Main Workspace Tabs ---

# Premium Top Header
st.markdown("""
<div class="header-container">
    <div class="header-logo">🩺</div>
    <div class="header-text">
        <h1>PhoneDoctor AI</h1>
        <p>Interactive medical symptom analyst powered by Gemini 2.5 Flash</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Aesthetic Safety Warning Disclaimer
st.warning(
    "⚠️ **Medical Disclaimer:** PhoneDoctor AI is an automated informational tool for educational purposes only. It does not provide professional medical diagnoses, advice, or treatment. If you are experiencing a medical emergency, please call your local emergency services immediately.",
    icon="🚨"
)

# Workspace Tab Navigation
tab_chat, tab_locator = st.tabs(["💬 Doctor Chat", "🏥 Locate Care"])

# --- Tab 1: Doctor Chat & Vision Analyzer ---
with tab_chat:
    # Initialize Session State Messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI PhoneDoctor assistant. How can I help with your health-related symptoms or medical queries today?"}
        ]

    # Render Chat History
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-avatar" style="justify-content: flex-end;">You 👤</div>
            <div class="chat-bubble chat-bubble-user">{content}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-avatar">🩺 PhoneDoctor AI</div>
            <div class="chat-bubble chat-bubble-bot">{content}</div>
            """, unsafe_allow_html=True)

    # Render Diagnostic Starter Cards if chat is brand new
    if len(st.session_state.messages) == 1:
        st.markdown("""
        <div style="margin: 25px 0 10px 0;">
            <h4 style="color: #10b981; font-weight: 600; margin-bottom: 5px;">⚡ Quick Diagnostic Starters</h4>
            <p style="color: #94a3b8; font-size: 14px; margin: 0 0 15px 0;">Select one of the common checkers below to immediately begin your symptom assessment:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤒 Persistent Fever Check", use_container_width=True, help="Analyze high body temperature and dry cough symptoms."):
                process_message("I have a persistent high fever and dry cough. What symptoms should I monitor?")
            if st.button("🤕 Severe Migraine Checker", use_container_width=True, help="Analyze throbbing headaches and relief recommendations."):
                process_message("I am experiencing a severe throbbing headache and light sensitivity. What are the common causes and medicine recommendations?")
        with col2:
            if st.button("🏃‍♂️ Joint Pain & Muscle Injury", use_container_width=True, help="Analyze joint pain, swelling, and first aid tips."):
                process_message("What is the best way to manage severe joint pain and swelling after an ankle injury?")
            if st.button("🩺 General Wellness & Fatigue Check", use_container_width=True, help="Analyze persistent fatigue and vitamin triggers."):
                process_message("I want to check general health symptoms of persistent fatigue and ask what vitamins or checks are recommended.")

    # Image Report Vision Uploader Usecase
    st.markdown("---")
    with st.expander("📷 Upload Prescription, Lab Report, or Symptom Image", expanded=False):
        st.markdown("<p style='color:#94a3b8; font-size: 13.5px;'>Upload an image of your prescription, diagnostic report, or symptom. The medical AI will read, translate, and transcribe it for you.</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Select medical image/report (PNG, JPG, JPEG)...",
            type=["png", "jpg", "jpeg"],
            key="medical_image_uploader"
        )
        if uploaded_file:
            st.image(uploaded_file, caption="Selected Medical Document", width=250)

    # Chat Input Container
    user_query = st.chat_input("Describe your symptom, pain, or query about the uploaded report here...")

    if user_query or (uploaded_file and st.button("🔬 Analyze Uploaded Image", use_container_width=True)):
        img_bytes = None
        img_mime = None
        if uploaded_file:
            img_bytes = uploaded_file.getvalue()
            img_mime = uploaded_file.type
            
        process_message(user_query, img_bytes, img_mime)


# --- Tab 2: Nearby Hospital & Clinic Finder ---
with tab_locator:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h3 style="color:#10b981; font-weight:700; margin:0 0 5px 0;">📍 Nearby Hospital & Clinic Proximity Locator</h3>
        <p style="color:#94a3b8; font-size:14.5px;">Find hospitals, local health clinics, or independent doctors within a <b>15km radius (15,000 meters)</b> of your location.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize GPS session states
    if "gps_coords" not in st.session_state:
        st.session_state.gps_coords = None
    if "gps_requested" not in st.session_state:
        st.session_state.gps_requested = False

    # Layout for selection methods
    st.markdown("<h4 style='color:#e2e8f0; font-weight:600;'>🔍 Choose Geolocation Method:</h4>", unsafe_allow_html=True)
    col_gps, col_sep, col_manual = st.columns([1.2, 0.1, 1.2])

    with col_gps:
        st.markdown("<div style='margin-bottom:10px;'>🛰️ <b>Option A: Auto-Detect Browser GPS</b></div>", unsafe_allow_html=True)
        if st.button("📍 Detect My Location", use_container_width=True, type="primary"):
            st.session_state.gps_requested = True
            st.session_state.gps_coords = None
            st.rerun()

        # If location detection is requested
        if st.session_state.gps_requested:
            st.markdown("<p style='color:#3b82f6; font-size:13.5px;'>🔄 Contacting browser GPS sensor...</p>", unsafe_allow_html=True)
            from streamlit_js_eval import get_geolocation
            loc = get_geolocation()
            
            if loc and "coords" in loc:
                lat = loc["coords"]["latitude"]
                lon = loc["coords"]["longitude"]
                st.session_state.gps_coords = {"lat": lat, "lon": lon}
                st.session_state.gps_requested = False
                st.success(f"📍 GPS coordinates locked successfully!")
                st.rerun()
            elif loc is None:
                st.info("🌐 Please click 'Allow' in the browser location popup to scan local clinics.")
                if st.button("❌ Cancel Request", key="cancel_gps_req"):
                    st.session_state.gps_requested = False
                    st.rerun()

        # If GPS coordinates are active
        if st.session_state.gps_coords:
            lat = st.session_state.gps_coords["lat"]
            lon = st.session_state.gps_coords["lon"]
            st.success(f"Locked GPS: **{lat:.5f}, {lon:.5f}**")
            if st.button("🗑️ Clear GPS Coordinates", use_container_width=True):
                st.session_state.gps_coords = None
                st.rerun()

    with col_manual:
        st.markdown("<div style='margin-bottom:10px;'>✍️ <b>Option B: Manual Region Search</b></div>", unsafe_allow_html=True)
        search_loc = st.text_input(
            "Enter City, State, or Neighborhood:", 
            placeholder="e.g. New Delhi, London, Manhattan",
            help="Type location if device GPS is off or browser permission is denied."
        )

    # Decide active searching coords
    active_lat = None
    active_lon = None
    location_label = ""
    search_triggered = False

    st.markdown("---")

    # Dynamic action buttons
    if st.session_state.gps_coords:
        search_btn_text = "🔍 Scan Nearby Care around GPS (15 km)"
        active_lat = st.session_state.gps_coords["lat"]
        active_lon = st.session_state.gps_coords["lon"]
        location_label = "your current GPS location"
        search_triggered = st.button(search_btn_text, use_container_width=True, type="primary")
    else:
        search_btn_text = "🔍 Scan Nearby Care around Manual Entry (15 km)"
        search_triggered = st.button(search_btn_text, use_container_width=True)
        if search_triggered and not search_loc:
            st.error("❌ Please enter a manual location search term or click 'Detect My Location'!")
            search_triggered = False

    # Execute locator queries
    if search_triggered:
        if not active_lat and search_loc:
            with st.spinner("📍 Geocoding manual address..."):
                coords = get_coordinates(search_loc)
                if coords:
                    active_lat, active_lon, display_name = coords
                    st.success(f"📍 Found Area: **{display_name}** ({active_lat:.4f}, {active_lon:.4f})")
                    location_label = display_name
                else:
                    st.error("❌ Could not locate the specified manual location. Please check the spelling.")

        if active_lat and active_lon:
            with st.spinner(f"📡 Querying global medical centers within 15 km of {location_label}..."):
                facilities = get_nearby_medical_facilities(active_lat, active_lon, radius=15000)
                
                if facilities:
                    st.markdown(f"<h4 style='color:#10b981; margin:20px 0 10px 0;'>🏥 Medical Centers Found ({len(facilities)}):</h4>", unsafe_allow_html=True)
                    
                    # Display medical facilities in custom styled cards
                    for fac in facilities:
                        name = fac["name"]
                        type_label = fac["type"]
                        address = fac["address"]
                        fac_lat = fac["lat"]
                        fac_lon = fac["lon"]
                        
                        # Set custom badge class based on facility type
                        badge_class = "type-facility"
                        if "hospital" in type_label:
                            badge_class = "type-hospital"
                        elif "clinic" in type_label:
                            badge_class = "type-clinic"
                        elif "doctor" in type_label:
                            badge_class = "type-doctors"
                        
                        map_url = f"https://www.google.com/maps/search/?api=1&query={fac_lat},{fac_lon}"
                        
                        st.markdown(f"""
                        <div class="clinic-card">
                            <div class="clinic-name">🏨 {name}</div>
                            <div class="clinic-type {badge_class}">{type_label}</div>
                            <div class="clinic-address">📍 {address}</div>
                            <a href="{map_url}" target="_blank" class="map-btn">🗺️ Navigate on Google Maps</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ No hospitals, clinics, or doctors found within 15km of {location_label}.")

