from pathlib import Path
import speech_recognition as sr
import pandas as pd
import traceback

import streamlit as st
from streamlit_ace import st_ace
from PIL import Image
import streamlit as st
from streamlit_extras.let_it_rain import rain
from tempfile import NamedTemporaryFile
from streamlit_option_menu import option_menu
from streamlit_extras.mandatory_date_range import date_range_picker
import os
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from streamlit_lottie import st_lottie
import requests 



global s
k=0
os.getenv("AIzaSyDwX2irhbT4LU8K8jhvFPHAaKp91qA3LLI")
genai.configure(api_key="AIzaSyDwX2irhbT4LU8K8jhvFPHAaKp91qA3LLI")

st.set_page_config(layout="wide")
def example():
    rain(
        emoji="*",
        font_size=40,
        falling_speed=7,
        animation_length="infinite",
    )

def get_gemini_response(question):
        model = genai.GenerativeModel('gemini-pro')  # Initialize Gemini model
        response = model.generate_content(question)  # Generate content
        return response.text
def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json() 

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

EXAMPLE_NO = 1
def streamlit_menu(example=1):
    if example == 1:
        with st.sidebar:
            selected = option_menu(
                menu_title="Authentication",
                options=["Dashborad","AI-Enhanced Password","Safe Chat","Fake Profile Detector","Mail Spam Detector"], 
                icons=["geo-alt-fill","bi bi-code-slash","bi bi-camera-video-fill","robot"],  # optional
                menu_icon="cast",  
                default_index=0,
            )
        return selected

selected = streamlit_menu(example=EXAMPLE_NO)



if selected=="AI-Enhanced Password":
    import streamlit as st
    import pandas as pd
    from password_strength import PasswordPolicy
    
    genai.configure(api_key="AIzaSyDwX2irhbT4LU8K8jhvFPHAaKp91qA3LLI")
    
    # Function to generate a password using Generative AI
    def generate_password(length, complexity):
        prompt = f"Generate a {length}-character password with {complexity} complexity for Gmail."
        # model = genai.GenerativeModel('gemini-pro')
        # response = model.generate_content(prompt)

        # Extract the first candidate's text as the password
        # password = response.candidates[0]
        password= "fehg"
        return password

    # Function to load breached passwords dataset
    @st.cache_data
    def load_breached_passwords():
        try:
            breached_data = pd.read_csv('breached_passwords.csv')  # CSV file with 'password' column
            return set(breached_data['password'])
        except FileNotFoundError:
            
            return {"123456", "password", "qwerty", "abc123", "admin", "welcome"}

    # Load breached passwords
    breached_passwords = load_breached_passwords()

    # Define password policy
    policy = PasswordPolicy.from_names(
        length=8,  # Minimum length of 8 characters
        uppercase=1,  # At least one uppercase letter
        numbers=1,  # At least one digit
        special=1,  # At least one special character
        nonletters=0,  # Any character
    )

    # Function to evaluate password strength
    def check_password_strength(password):
        if not password:
           st.write("Please enter a password.")

        suggestions = []
        score = 0

        # Evaluate against password policy
        issues = policy.test(password)
        if issues:
            for issue in issues:
                suggestions.append(str(issue))
        else:
            score += 1

        # Check for common patterns
        common_patterns = ['123', 'password', 'qwerty', 'abc']
        if any(pattern in password.lower() for pattern in common_patterns):
            suggestions.append("Avoid common patterns like '123', 'password', or 'qwerty'.")
        else:
            score += 1

        # Check against breached passwords
        if password in breached_passwords:
            suggestions.append("This password has been found in known data breaches.")
        else:
            score += 1

        # Evaluate password length
        if len(password) > 12:
            score += 1
        else:
            suggestions.append("Consider using a longer password (more than 12 characters).")

        # Calculate final score percentage
        score_percentage = (score / 4) * 100
        return score_percentage, suggestions

    link="https://lottie.host/d3dda3c7-711b-41e0-98bc-43f7f8dde483/krjC94tvvI.json"
    l=load_lottieurl(link)
    col1, col2 = st.columns([1.3,9])  # Create two columns
    with col1:
        st.lottie(l, height=100, width=100)
    with col2:
        st.header(f":rainbow[AI-Enhanced Password Utility ]😎🧑‍🏫", divider='rainbow')
    # Buttons to toggle functionality
    col1, col2 = st.columns(2)

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None

    # Button Selection
    with col1:
        if st.button("Generate Password"):
            st.session_state.selected_option = "generate"

    with col2:
        if st.button("Check Password Strength"):
            st.session_state.selected_option = "check"

    # Display functionality based on selected option
    if st.session_state.selected_option == "generate":
        st.subheader("Password Generation")
        length = st.slider("Password Length", min_value=8, max_value=32, value=12)
        complexity = st.selectbox("Password Complexity", ["Low", "Medium", "High"])
        #add checkbok
        spcialchar="do not include special charecter"
        if st.checkbox("Include Special Characters"):
            spcialchar = "incleded  specal charecter "
        if st.button("Generate Secure Password", key="generate_button"):
            password = get_gemini_response("Generate a secure password of size "+ str(length) + " with " + complexity + " complexity. also conlude  "+spcialchar+" special characters")
            st.success(f"Generated Password: {password}")

    elif st.session_state.selected_option == "check":
        st.subheader("Password Strength Evaluation")
        st.markdown(
            """
            <div style="background-color:#f9f9f9;padding:10px;border-radius:5px;box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                <h4 style="color:#333;">Tips for Creating a Strong Password:</h4>
                <ul style="color:#555;">
                    <li>Use at least <b>8 characters</b>, but aim for more than <b>12 characters</b>.</li>
                    <li>Include a mix of <b>uppercase</b>, <b>lowercase</b>, <b>numbers</b>, and <b>special characters</b>.</li>
                    <li>Avoid common patterns like <b>"123"</b>, <b>"password"</b>, or <b>"qwerty"</b>.</li>
                    <li>Ensure your password is <b>unique</b> and not reused across different accounts.</li>
                    <li>Check that your password hasn’t been part of a <b>known data breach</b>.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Input field for password
        password = st.text_input("Enter your password:", type="password")

        if password:
            score, feedback = check_password_strength(password)
            st.metric("Password Strength Score", f"{score}%")
            st.subheader("Recommendations:")
            if feedback:
                for tip in feedback:
                    st.write(f"- {tip}")
            else:
                st.success("Your password is strong and secure!")
                st.balloons()
        else:
            st.info("Please enter a password to evaluate.")
    else:
        st.info("Please select an action: Generate Password or Check Password Strength.")

if selected=="Dashborad":
    import random
    import pandas as pd
    import numpy as np
    import streamlit as st
    import matplotlib.pyplot as plt
    import streamlit_shadcn_ui as ui

    # Dummy Data for the graph
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    threats = [random.randint(100, 1000) for _ in days]
    attacks = [random.randint(10, 500) for _ in days]
    types_of_threats = ['Malware', 'Phishing', 'Ransomware', 'Spyware']
    threat_distribution = [random.randint(100, 500) for _ in types_of_threats]

    # Dashboard layout
    st.title("Cyber Security Dashboard 🛡")
    st.subheader("Monitor your cyber security status and trends")

    # Health Metrics Section (Heart Rate, Steps, Blood Pressure, Sleep Condition, Overall Health)
    st.markdown("### Cyber Security Metrics:")

    # Use metric cards as per the reference given
    with st.container(border=True):
        a, b, c = st.columns(3)
        with a:
            ui.metric_card(title="Malware Detected", content=f"{random.randint(1, 10)} files", description="Warning!", key="card1")
        with b:
            ui.metric_card(title="Phishing Attempts", content=f"{random.randint(1, 5)} attempts", description="Alert!", key="card2")
        with c:
            ui.metric_card(title="Unpatched Vulnerabilities", content=f"{random.randint(0, 3)} issues", description="Critical", key="card3")

    # Cybersecurity Attack Trends Section (Graphs)
    st.markdown("### Cyber Security Attack Trends:")

    # Create columns for bar chart and line chart
    # with st.container(border=True):

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="card">
                    <div class="metric-label">Threats Over the Week</div>
                    <div class="metric-value">Bar Chart</div>
                    <div class="metric-delta">Trending Threats</div>
                </div>
            """, unsafe_allow_html=True)
            df_threats = pd.DataFrame({'Day': days, 'Threats': threats})
            st.bar_chart(df_threats.set_index('Day'))
        with st.container(border=True):
            with col2:
                st.markdown("""
                    <div class="card">
                        <div class="metric-label">Attacks Over the Week</div>
                        <div class="metric-value">Line Chart</div>
                        <div class="metric-delta">Trending Attacks</div>
                    </div>
                """, unsafe_allow_html=True)
                df_attacks = pd.DataFrame({'Day': days, 'Attacks': attacks})
                st.line_chart(df_attacks.set_index('Day'))

    # Pie Chart for Threat Distribution and Scatter Plot
    st.markdown("### Cybersecurity Threat Distribution and Attacks:")

    # Create two columns for side-by-side layout


    # Pie Chart in the first column
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="card">
                    <div class="metric-label">Threat Distribution</div>
                    <div class="metric-value">Pie Chart</div>
                    <div class="metric-delta">Types of Threats</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Create the pie chart
            fig, ax = plt.subplots(figsize=(6, 6))  # Create a figure and axis object
            ax.pie(threat_distribution, labels=types_of_threats, autopct='%1.1f%%', startangle=90, colors=['#ff6666','#ffcc99','#99ff99','#66b3ff'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)  # Pass the figure object to st.pyplot()

        # Scatter Plot in the second column
        with col2:
            st.markdown("""
                <div class="card">
                    <div class="metric-label">Threats vs Attacks</div>
                    <div class="metric-value">Scatter Plot</div>
                    <div class="metric-delta">Compare Threats and Attacks</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Scatter plot of Threats vs Attacks
            df = pd.DataFrame({'Threats': threats, 'Attacks': attacks})
            st.scatter_chart(df)

    # Display some insights
    st.markdown("### Actionable Insights for Cybersecurity:")
    with st.container(border=True):
        st.write("""
        - *Enable two-factor authentication (2FA)* for all your accounts.
        - *Keep your software updated* to avoid vulnerabilities.
        - *Monitor network traffic* for suspicious activities.
        - *Be cautious with email links* to avoid phishing attempts.
        - *Use strong and unique passwords* for each account.
        """)

    # Footer/Closing Section
    st.markdown("---")
    st.markdown("Stay safe online! 🌐 Keep your data secure.")
if selected=="Safe Chat":               

    import streamlit as st
    from streamlit_lottie import st_lottie
    import requests
    #import genai

    # Function to load Lottie animation
    def load_lottieurl(url: str):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Function to get responses from Gemini
      # Return the response text

    # Streamlit App
    

    # Sidebar
    st.sidebar.title("Safe Chat Bot")
    st.sidebar.info(
        """
        *Purpose*: Educate and guide users to chat safely online.  
        *Features*:  
        - Real-time warnings for risky language.  
        - Tips for safe online practices.
        """
    )

    # Main page
    
    

    link="https://lottie.host/364beff7-b5bc-459e-ac28-d26cfa0dfece/FLsJPwNGdK.json"
    l=load_lottieurl(link)
    col1, col2 = st.columns([1.4,9])  # Create two columns
    with col1:
        st.lottie(l, height=100, width=100)
    with col2:
        st.header(f":rainbow[Safe Chat ]😎🧑‍🏫", divider='rainbow')
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you chat safely online?"}]

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])
        else:
            st.chat_message("user").write(msg["content"])

    # User input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # Generate AI response
        response = get_gemini_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)



if selected=="Fake Profile Detector":
    lottie_social_media = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tno6cg2w.json")

    # Hardcoded credentials for demonstration purposes
    USERNAME = "welcome_solar_system"        
    PASSWORD = "JaiShreeRam" 
    # Enhanced Scoring Function
    def calculate_fake_profile_score(followers, following, posts, biography):
        score = 0

        # Follower-to-Following Ratio
        if following == 0:
            ratio = float("inf")
        else:
            ratio = followers / following

        # Adjust thresholds based on followers
        if followers < 1000:
            if ratio < 0.5 or ratio > 5:  # Small accounts are expected to have balanced ratios
                score += 2
        elif followers >= 1000:
            if ratio < 0.1 or ratio > 100:  # Larger accounts have higher follower-following ratios
                score += 2

        # Posts Logic
        if posts == 0:
            score += 2  # No activity
        elif posts > 1000 and followers < 10000:  # Non-celebrity accounts with excessive posts
            score += 2

        # Bio Completeness
        if not biography.strip():
            score += 1  # Missing or empty bio is a mild flag

        # High Follower Suspicious Check
        if followers > 10000 and posts == 0:
            score += 2  # High follower count but no posts is unusual

        # Determine risk level
        if score <= 2:
            risk_level = "Low"
        elif score <= 4:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return score, risk_level

    # Streamlit UI


    # Title with social media animation
    col1, col2 = st.columns([1, 5])
    with col1:
        if lottie_social_media:
            st_lottie(lottie_social_media, height=100, key="social_media")
        else:
            st.write("🔗 [View Social Media Animation](https://lottiefiles.com/)")
    with col2:
        
        st.header(f":rainbow[ Fake Profile Detector ]🕵‍♂🕵‍♂", divider='rainbow')
    st.header(
        """
        *Detect fake Instagram profiles!*  
        Analyze profile details like followers, following, and bio completeness to identify suspicious accounts. 
        """
    )

    
    profile_name = st.text_input("Enter the Instagram Profile Name to Analyze")
    
    if profile_name:
        try:
            # Instantiate Instaloader and login
            loader = Instaloader()
            with st.spinner("🔑 Logging in..."):
                loader.login(USERNAME, PASSWORD)

            # Load profile data
            with st.spinner(f"📄 Fetching data for {profile_name}..."):
                profile = Profile.from_username(loader.context, profile_name)

            # Fetch profile details
            followers = profile.followers
            following = profile.followees
            biography = profile.biography or ""
            profile_pic_url = profile.profile_pic_url
            posts = profile.mediacount

            # Analyze profile for fake indicators
            score, risk_level = calculate_fake_profile_score(followers, following, posts, biography)

            # Display results
            st.success(f"Profile data for {profile_name} fetched successfully!")
            # st.image(profile_pic_url, caption=f"{profile_name}'s Profile Picture", use_column_width=True)
            col1, col2 = st.columns(2)

    # Add content to the first column
            with col1:
                st.subheader("📊 Profile Details")
                st.write(f"*Full Name:* {profile.full_name}")
                st.write(f"*Biography:* {biography or 'Not Provided'}")
                st.write(f"*Number of Followers:* {followers}")
                st.write(f"*Number of Following:* {following}")
                st.write(f"*Number of Posts:* {posts}")


                st.subheader("🔍 Fake Profile Analysis")
                st.write(f"*Risk Level:* {risk_level}")
                st.write(f"*Score:* {score} (Lower is better)")
            # Add content to the second column
            with col2:
                st.subheader("📊 Profile Metrics")
                stats = {
                    "Followers": followers,
                    "Following": following,
                    "Posts": posts,
                }
                fig = px.pie(values=list(stats.values()), names=list(stats.keys()), title="Profile Metrics",
                    color_discrete_sequence=["orange", "lightgreen", "lightyellow"])
                fig.update_layout(
            width=800,  # Adjust width as needed
            height=400,  # Adjust height as needed
            margin=dict(l=50, r=50, t=50, b=50),  # Remove margins
            paper_bgcolor='rgba(240, 240, 240, 0.8)',  # Light grey background
            plot_bgcolor='rgba(240, 240, 240, 0.8)'  # Light grey plot background
        )
                st.plotly_chart(fig)
            


            # Display a statistical chart



            # Recommendations
            st.subheader("🛡 Recommendations")
            if risk_level == "Low":
                st.success("This profile appears genuine. Always stay cautious.")
            elif risk_level == "Medium":
                st.warning("This profile shows some signs of being fake. Be careful while engaging.")
                s=get_gemini_response("this profile is little bit fake and you have tell some reamse and tell how can i impove it")
                st.write(s)
            else:
                st.error("This profile is highly suspicious! Avoid engaging with it.")
                s=get_gemini_response("this profile is fake and you have tell some reamse and tell how can i impove it")
                st.write(s)

        except Exception as e:
            st.error(f"Error fetching profile: {e}")

    else:
        st.info("Enter an Instagram profile name to analyze.")    

if selected=="Mail Spam Detector":
    import pickle
    import requests

    def load_lottie_url(url: str):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

    spam_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_8rqgch4p.json")  # Replace with a better spam animation URL
    ham_animation = load_lottie_url("https://assets7.lottiefiles.com/private_files/lf30_5ttqpi5v.json")  # Replace with a better legit (HAM) animation URL

    # Loading the trained model
    model = pickle.load(open('model.pkl', 'rb'))

    # Page configuration
    

    # App title
    link="https://lottie.host/d3dda3c7-711b-41e0-98bc-43f7f8dde483/krjC94tvvI.json"
    l=load_lottieurl(link)
    col1, col2 = st.columns([1.3,9])  # Create two columns
    with col1:
        st.lottie(l, height=100, width=100)
    with col2:
        st.header(f":rainbow[ Spam Message Detector ]📩📩", divider='rainbow')

    # Add description
    st.header("""
    Welcome to the *Spam Message Detector*!  
    Enter a message, and we'll help you determine if it's *Spam* or *Legitimate (HAM)*.  
    """)

    # Input field for message
    message = st.text_input('📩 Enter your message here 😊:')

    # Button for prediction
    submit = st.button('🔍 Predict')

    # Display animations and results
    if submit:
        if message.strip() == "":
            st.warning("⚠ Please enter a valid message to proceed.")
        else:
            prediction = model.predict([message])
            
            if prediction[0] == 'spam':
                st.markdown("### 🛑 This message is *Spam*.")

                s=get_gemini_response("this message is spam and you have tell some reamse  why it is spam the message is "+message)
                st.write(s)
                
            else:
                st.markdown("### ✅ This message is *Legitimate (HAM)*.")
                s=get_gemini_response("this message is not a span and you have tell some reamse  why it is not spam the message is "+message)
                st.write(s)
            st.balloons()
    

    # Footer
    st.markdown("---")
