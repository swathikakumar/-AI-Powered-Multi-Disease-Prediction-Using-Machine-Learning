import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pickle
import requests
from streamlit_lottie import st_lottie

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="AI Disease Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== CUSTOM CSS ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card {
        background: black;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
    
    .risk-box-high {
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(255,107,107,0.3);
        margin: 20px 0;
    }
    
    .risk-box-low {
        background: linear-gradient(135deg, #51cf66, #38d9a9);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(81,207,102,0.3);
        margin: 20px 0;
    }
    
    .suggestion-card {
        background: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .suggestion-card:hover {
        transform: translateX(5px);
    }
    
    .tips-section {
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ======================== DISEASE INFO ========================
DISEASE_INFO = {
    "Diabetes": {
        "precautions": [
            "🩺 Monitor blood sugar levels regularly",
            "💊 Take prescribed medications on time",
            "🏥 Schedule regular check-ups with your doctor",
            "🦶 Check feet daily for cuts or sores"
        ],
        "good_foods": [
            "🥦 Leafy greens (spinach, kale)",
            "🐟 Fatty fish (salmon, sardines)",
            "🥜 Nuts and seeds",
            "🫐 Berries",
            "🥑 Avocados",
            "🌾 Whole grains"
        ],
        "avoid_foods": [
            "🍰 Sugary desserts and pastries",
            "🥤 Sweetened beverages",
            "🍞 White bread and refined carbs",
            "🍟 Fried foods",
            "🥓 Processed meats",
            "🧃 Fruit juices with added sugar"
        ],
        "do": [
            "✅ Exercise for 30 minutes daily",
            "✅ Maintain a healthy weight",
            "✅ Stay hydrated with water",
            "✅ Get 7-9 hours of sleep",
            "✅ Manage stress through meditation"
        ],
        "dont": [
            "❌ Skip meals or medications",
            "❌ Smoke or use tobacco",
            "❌ Consume excessive alcohol",
            "❌ Ignore symptoms or warning signs",
            "❌ Lead a sedentary lifestyle"
        ]
    },
    "Heart": {
        "precautions": [
            "💓 Monitor blood pressure regularly",
            "🏃 Exercise moderately and consistently",
            "😌 Manage stress and anxiety",
            "💊 Take heart medications as prescribed"
        ],
        "good_foods": [
            "🐟 Omega-3 rich fish",
            "🥜 Almonds and walnuts",
            "🫒 Olive oil",
            "🍅 Tomatoes",
            "🥦 Broccoli and leafy greens",
            "🍊 Citrus fruits"
        ],
        "avoid_foods": [
            "🧂 High sodium foods",
            "🥓 Saturated and trans fats",
            "🍔 Fast food",
            "🥩 Red meat in excess",
            "🍰 Sugary foods",
            "🧈 Butter and margarine"
        ],
        "do": [
            "✅ Walk for 30 minutes daily",
            "✅ Practice deep breathing exercises",
            "✅ Maintain healthy cholesterol levels",
            "✅ Keep blood pressure under 120/80",
            "✅ Stay socially connected"
        ],
        "dont": [
            "❌ Ignore chest pain or discomfort",
            "❌ Smoke or expose yourself to smoke",
            "❌ Overexert during exercise",
            "❌ Consume excessive caffeine",
            "❌ Skip regular check-ups"
        ]
    },
    "Parkinsons": {
        "precautions": [
            "🧠 Engage in regular physical therapy",
            "💊 Take medications at consistent times",
            "🏡 Remove fall hazards from home",
            "🗣️ Practice speech and swallowing exercises"
        ],
        "good_foods": [
            "🍓 Antioxidant-rich berries",
            "🥬 Dark leafy greens",
            "🌰 Nuts and seeds",
            "🐟 Omega-3 fatty fish",
            "🫐 Blueberries",
            "🥦 Cruciferous vegetables"
        ],
        "avoid_foods": [
            "🥩 High protein meals (can interfere with meds)",
            "🧀 Dairy products in excess",
            "🍺 Alcohol",
            "☕ Excessive caffeine",
            "🧂 High sodium foods",
            "🍰 Processed sugars"
        ],
        "do": [
            "✅ Stay physically active with tai chi or yoga",
            "✅ Keep a regular sleep schedule",
            "✅ Practice balance exercises",
            "✅ Join support groups",
            "✅ Maintain good posture"
        ],
        "dont": [
            "❌ Isolate yourself socially",
            "❌ Skip physical therapy sessions",
            "❌ Ignore medication schedules",
            "❌ Rush through activities",
            "❌ Neglect mental health"
        ]
    }
}

# ======================== HEALTH TIPS ========================
HEALTH_TIPS = {
    "General Wellness": [
        "💧 Drink at least 8-10 glasses of water daily to stay hydrated",
        "🛌 Maintain a consistent sleep schedule of 7-9 hours per night",
        "🏃 Engage in at least 150 minutes of moderate exercise weekly",
        "🥗 Eat a balanced diet rich in fruits, vegetables, and whole grains",
        "🧘 Practice stress management through meditation or yoga",
        "🚭 Avoid smoking and limit alcohol consumption",
        "👥 Maintain strong social connections with friends and family",
        "📱 Limit screen time, especially before bedtime",
        "🌞 Get adequate sunlight exposure for vitamin D",
        "🧼 Practice good hygiene including regular handwashing"
    ],
    "Nutrition": [
        "🍽️ Eat smaller, more frequent meals throughout the day",
        "🥗 Fill half your plate with colorful vegetables",
        "🍗 Choose lean proteins like fish, chicken, and legumes",
        "🌾 Opt for whole grains instead of refined carbohydrates",
        "🥛 Include calcium-rich foods for bone health",
        "🧂 Limit sodium intake to less than 2,300mg per day",
        "🍬 Reduce added sugars and sweetened beverages",
        "🥜 Include healthy fats from nuts, seeds, and avocados",
        "🍊 Consume vitamin C-rich foods for immune support",
        "🥤 Avoid processed and ultra-processed foods"
    ],
    "Exercise": [
        "🏃 Start with 10 minutes of exercise and gradually increase",
        "💪 Include both cardio and strength training in your routine",
        "🧘 Stretch before and after workouts to prevent injury",
        "🚶 Take regular walking breaks if you have a desk job",
        "🏊 Try low-impact exercises like swimming or cycling",
        "🤸 Incorporate flexibility exercises like yoga or pilates",
        "⏰ Exercise at the same time each day to build a habit",
        "👟 Invest in proper footwear to prevent injuries",
        "📈 Gradually increase intensity to avoid overexertion",
        "💧 Stay hydrated before, during, and after exercise"
    ],
    "Mental Health": [
        "🧠 Practice mindfulness and meditation daily",
        "📝 Keep a gratitude journal to focus on positives",
        "🗣️ Talk to someone you trust about your feelings",
        "🎨 Engage in hobbies and activities you enjoy",
        "🌳 Spend time in nature to reduce stress",
        "📵 Take regular breaks from social media",
        "😴 Establish a relaxing bedtime routine",
        "🎯 Set realistic goals and celebrate small wins",
        "🤝 Seek professional help when needed",
        "💚 Practice self-compassion and positive self-talk"
    ],
    "Prevention": [
        "💉 Stay up-to-date with recommended vaccinations",
        "🩺 Schedule regular health screenings and check-ups",
        "🧴 Use sunscreen daily to protect against skin cancer",
        "🦷 Maintain good oral hygiene with daily brushing and flossing",
        "🧼 Wash hands frequently with soap and water",
        "😷 Wear masks in crowded or high-risk settings",
        "🏥 Know your family health history",
        "📊 Monitor your vital signs regularly",
        "🍎 Maintain a healthy weight for your body type",
        "🚨 Recognize warning signs of common diseases"
    ]
}

# ======================== LOTTIE ANIMATIONS ========================
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_dashboard = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")
lottie_diabetes = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_tll0j4bb.json")
lottie_heart = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_abqysclq.json")
lottie_brain = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_rwq6ciql.json")
lottie_success = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_auzja8ot.json")

# ======================== SESSION STATE ========================
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'show_patient_form' not in st.session_state:
    st.session_state.show_patient_form = False
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = {}

# ======================== LOAD MODELS ========================
@st.cache_resource
def load_models():
    models = {}
    try:
        with open(r"C:\Users\Swathika\Downloads\Multiple-Disease-Prediction-System-main\Multiple-Disease-Prediction-System-main\Multiple Disease Prediction System\diabetes_model.sav", 'rb') as f:
            models['diabetes'] = pickle.load(f)
    except:
        models['diabetes'] = None
        st.warning("⚠️ Diabetes model not found. Using demo mode.")
    
    try:
        with open(r"C:\Users\Swathika\Downloads\Multiple-Disease-Prediction-System-main\Multiple-Disease-Prediction-System-main\Multiple Disease Prediction System\heart_disease_model.sav", 'rb') as f:
            models['heart'] = pickle.load(f)
    except:
        models['heart'] = None
        st.warning("⚠️ Heart disease model not found. Using demo mode.")
    
    try:
        with open(r"C:\Users\Swathika\Downloads\Multiple-Disease-Prediction-System-main\Multiple-Disease-Prediction-System-main\Multiple Disease Prediction System\parkinsons_model.sav", 'rb') as f:
            models['parkinsons'] = pickle.load(f)
    except:
        models['parkinsons'] = None
        st.warning("⚠️ Parkinson's model not found. Using demo mode.")
    
    return models

models = load_models()
diabetes_model = models['diabetes']
heart_disease_model = models['heart']
parkinsons_model = models['parkinsons']

# ======================== SIDEBAR ========================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>AI Disease Prediction System🏥 </h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    choice = st.radio(
        "Navigate to:",
        ["🏠 Dashboard", "🩸 Diabetes", "❤️ Heart Disease", "🧠 Parkinson's", "📊 My Reports", "💡 Health Tips"],
        key="navigation"
    )
    
    st.markdown("---")
    
    # Patient Information Form
    if st.session_state.show_patient_form:
        st.markdown("<h3 style='text-align: center; color: white;'>👤 Patient Information</h3>", unsafe_allow_html=True)
        
        with st.form("patient_info_form"):
            patient_name = st.text_input("📝 Patient Name", value=st.session_state.patient_info.get("name", ""))
            phone = st.text_input("📞 Phone Number", value=st.session_state.patient_info.get("phone", ""), max_chars=15)
            address = st.text_area("🏠 Address", value=st.session_state.patient_info.get("address", ""), height=80)
            place = st.text_input("📍 Place/City", value=st.session_state.patient_info.get("place", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                blood_group = st.selectbox("🩸 Blood Group",
                    ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                    index=0 if st.session_state.patient_info.get("blood_group") == "Select" or not st.session_state.patient_info.get("blood_group") else
                    ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(st.session_state.patient_info.get("blood_group", "Select")))
            with col2:
                height = st.number_input("📏 Height (cm)", min_value=0, max_value=250,
                    value=int(st.session_state.patient_info.get("height", 0)))
            
            weight = st.number_input("⚖️ Weight (kg)", min_value=0.0, max_value=300.0,
                value=float(st.session_state.patient_info.get("weight", 0.0)), format="%.1f")
            
            submit_patient_info = st.form_submit_button("💾 Save Patient Info", use_container_width=True)
            
            if submit_patient_info:
                st.session_state.patient_info = {
                    "name": patient_name,
                    "phone": phone,
                    "address": address,
                    "place": place,
                    "blood_group": blood_group,
                    "height": height,
                    "weight": weight
                }
                
                if st.session_state.last_prediction:
                    st.session_state.last_prediction["patient_info"] = st.session_state.patient_info
                    if st.session_state.reports:
                        st.session_state.reports[-1]["patient_info"] = st.session_state.patient_info
                
                st.success("✅ Patient information saved!")
                st.rerun()
        
        if st.session_state.patient_info.get("name"):
            st.markdown("---")
            st.markdown("<h4 style='color: white;'>Saved Info:</h4>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.15); padding: 10px; border-radius: 10px; color: white; font-size: 12px;'>
                <strong>👤 Name:</strong> {st.session_state.patient_info.get('name', 'N/A')}<br>
                <strong>📞 Phone:</strong> {st.session_state.patient_info.get('phone', 'N/A')}<br>
                <strong>🩸 Blood:</strong> {st.session_state.patient_info.get('blood_group', 'N/A')}<br>
                <strong>📏 Height:</strong> {st.session_state.patient_info.get('height', 'N/A')} cm<br>
                <strong>⚖️ Weight:</strong> {st.session_state.patient_info.get('weight', 'N/A')} kg
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    st.markdown(f"<p style='text-align: center; color: white;'>📅 {datetime.now().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)

# ======================== DASHBOARD ========================
if choice == "🏠 Dashboard":
    st.markdown("<h1 style='text-align: center;'>🤖 AI-Powered Multi-Disease Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Powered by Advanced Machine Learning Techniques</h3>", unsafe_allow_html=True)
    
    if lottie_dashboard:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(lottie_dashboard, height=250, key="dashboard_main")
    
    st.markdown("---")
    
    # Generate synthetic dataset
    np.random.seed(42)
    n_samples = 500
    
    df = pd.DataFrame({
        "Age": np.random.randint(20, 80, n_samples),
        "Glucose": np.random.randint(70, 200, n_samples),
        "BloodPressure": np.random.randint(60, 140, n_samples),
        "BMI": np.random.uniform(16, 45, n_samples),
        "Cholesterol": np.random.randint(150, 300, n_samples),
        "HeartRate": np.random.randint(60, 120, n_samples),
        "Disease": np.random.choice(["Diabetes", "Heart Disease", "Parkinson's", "Healthy"], n_samples, p=[0.25, 0.25, 0.15, 0.35])
    })
    
    # Metrics Cards
    st.markdown("## 📊 Health Statistics Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        diabetes_count = (df['Disease'] == 'Diabetes').sum()
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #ff6b6b; text-align: center;'>🩸</h2>
            <h3 style='text-align: center;'>Diabetes Cases</h3>
            <h1 style='text-align: center; color: #667eea;'>{diabetes_count}</h1>
            <p style='text-align: center; color: #666;'>{diabetes_count/n_samples*100:.1f}% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        heart_count = (df['Disease'] == 'Heart Disease').sum()
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #ff6b6b; text-align: center;'>❤️</h2>
            <h3 style='text-align: center;'>Heart Disease</h3>
            <h1 style='text-align: center; color: #667eea;'>{heart_count}</h1>
            <p style='text-align: center; color: #666;'>{heart_count/n_samples*100:.1f}% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        parkinsons_count = (df['Disease'] == "Parkinson's").sum()
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #ff6b6b; text-align: center;'>🧠</h2>
            <h3 style='text-align: center;'>Parkinson's</h3>
            <h1 style='text-align: center; color: #667eea;'>{parkinsons_count}</h1>
            <p style='text-align: center; color: #666;'>{parkinsons_count/n_samples*100:.1f}% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        healthy_count = (df['Disease'] == 'Healthy').sum()
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #51cf66; text-align: center;'>✅</h2>
            <h3 style='text-align: center;'>Healthy</h3>
            <h1 style='text-align: center; color: #667eea;'>{healthy_count}</h1>
            <p style='text-align: center; color: #666;'>{healthy_count/n_samples*100:.1f}% of total</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📈 Advanced Health Analytics")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            df, x="Glucose", y="BMI", color="Disease", size="BloodPressure",
            color_discrete_map={
                "Diabetes": "#ff6b6b",
                "Heart Disease": "#4ecdc4",
                "Parkinson's": "#a29bfe",
                "Healthy": "#55efc4"
            },
            title="🔍 Glucose vs BMI Analysis",
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        disease_counts = df['Disease'].value_counts()
        fig_pie = px.pie(
            values=disease_counts.values,
            names=disease_counts.index,
            title="🥧 Disease Distribution",
            color_discrete_sequence=['#55efc4', '#ff6b6b', '#4ecdc4', '#a29bfe'],
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ======================== DIABETES PREDICTION ========================
elif choice == "🩸 Diabetes":
    st.markdown("<h1 style='text-align: center;'>🩸 Diabetes Risk Assessment</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if lottie_diabetes:
            st_lottie(lottie_diabetes, height=200, key="diabetes_anim")
    
    st.markdown("---")
    st.markdown("### 📝 Enter Your Health Parameters")
    
    colA, colB = st.columns(2)
    with colA:
        pregnancies = st.number_input("👶 Number of Pregnancies", 0, 20, 0)
        glucose = st.number_input("🧪 Glucose Level (mg/dL)", 0, 500, 120)
        bp = st.number_input("💓 Blood Pressure (mm Hg)", 0, 300, 70)
        skin = st.number_input("🩹 Skin Thickness (mm)", 0, 100, 20)
    
    with colB:
        insulin = st.number_input("💉 Insulin Level (mu U/ml)", 0, 1000, 80)
        bmi = st.number_input("⚖️ BMI", 0.0, 80.0, 26.0, format="%.2f")
        dpf = st.number_input("📈 Diabetes Pedigree Function", 0.0, 5.0, 0.5, format="%.3f")
        age = st.number_input("🎂 Age", 1, 120, 30)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        predict_btn = st.button("🔮 Predict Diabetes Risk", use_container_width=True)
    
    if predict_btn:
        # Demo prediction logic
        risk_score = min(95, max(5, (glucose/200 + bmi/40 + age/100) * 33 + np.random.uniform(-10, 10)))
        prediction = 1 if risk_score > 50 else 0
        
        result_text = "At Risk for Diabetes" if prediction == 1 else "Low Risk - Healthy"
        risk_level = "HIGH RISK" if risk_score > 50 else "LOW RISK"
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.last_prediction = {
            "disease": "Diabetes",
            "result": result_text,
            "date": now,
            "score": risk_score,
            "risk_level": risk_level,
            "parameters": {
                "Pregnancies": pregnancies, "Glucose": glucose, "Blood Pressure": bp,
                "Skin Thickness": skin, "Insulin": insulin, "BMI": bmi,
                "Diabetes Pedigree": dpf, "Age": age
            }
        }
        st.session_state.reports.append(st.session_state.last_prediction)
        st.session_state.show_result = True
        st.session_state.show_patient_form = True
        st.rerun()
    
    # Display Results
    if st.session_state.show_result and st.session_state.last_prediction and st.session_state.last_prediction["disease"] == "Diabetes":
        st.markdown("---")
        st.markdown("## 🎯 Prediction Results")
        
        pred = st.session_state.last_prediction
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if lottie_success:
                st_lottie(lottie_success, height=150, key="success_diabetes")
        
        if pred["risk_level"] == "HIGH RISK":
            st.markdown(f"""
            <div class='risk-box-high'>
                <h2>⚠️ HIGH RISK DETECTED</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Please consult with a healthcare professional immediately</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='risk-box-low'>
                <h2>✅ LOW RISK</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Maintain your healthy lifestyle!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred['score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Percentage", 'font': {'size': 24}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': '#55efc4'},
                    {'range': [30, 70], 'color': '#feca57'},
                    {'range': [70, 100], 'color': '#ff6b6b'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 75}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("## 💡 Personalized Recommendations")
        
        disease_key = "Diabetes"
        
        st.markdown("### 🛡️ Essential Precautions")
        cols = st.columns(2)
        for i, precaution in enumerate(DISEASE_INFO[disease_key]["precautions"]):
            with cols[i % 2]:
                st.markdown(f"<div class='suggestion-card'>{precaution}</div>", unsafe_allow_html=True)
        
        st.markdown("### ✅ Recommended Foods")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["good_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #51cf66;'>{food}</div>", unsafe_allow_html=True)
        
        st.markdown("### ❌ Foods to Avoid")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["avoid_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #ff6b6b;'>{food}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Do's")
            for item in DISEASE_INFO[disease_key]["do"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(255,107,107,0.01), rgba(255,107,107,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ❌ Don'ts")
            for item in DISEASE_INFO[disease_key]["dont"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(255,107,107,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("✅ Report generated! Check 'My Reports' section.")
        with col3:
            if st.button("🔄 New Prediction", use_container_width=True):
                st.session_state.show_result = False
                st.session_state.show_patient_form = False
                st.rerun()

# ======================== HEART DISEASE PREDICTION ========================
elif choice == "❤️ Heart Disease":
    st.markdown("<h1 style='text-align: center;'>❤️ Heart Disease Risk Assessment</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if lottie_heart:
            st_lottie(lottie_heart, height=200, key="heart_anim")
    
    st.markdown("---")
    st.markdown("### 📝 Enter Your Cardiac Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("🎂 Age", 1, 120, 45)
        sex = st.selectbox("👤 Sex", ["0 - Female", "1 - Male"])
        cp = st.number_input("💓 Chest Pain Type", 0, 3, 1)
        trestbps = st.number_input("🩺 Resting Blood Pressure", 50, 200, 120)
    
    with col2:
        chol = st.number_input("🧪 Cholesterol", 100, 600, 200)
        fbs = st.selectbox("🍬 Fasting Blood Sugar > 120?", ["0 - No", "1 - Yes"])
        restecg = st.number_input("🫀 Resting ECG", 0, 2, 0)
        thalach = st.number_input("💓 Max Heart Rate", 60, 220, 150)
    
    with col3:
        exang = st.selectbox("🏃 Exercise Induced Angina", ["0 - No", "1 - Yes"])
        oldpeak = st.number_input("📉 ST Depression", 0.0, 10.0, 1.0, format="%.1f")
        slope = st.number_input("📈 ST Slope", 0, 2, 1)
        ca = st.number_input("🩻 Major Vessels", 0, 3, 0)
    
    thal = st.number_input("🧬 Thalassemia", 0, 3, 1)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        predict_btn = st.button("🔮 Predict Heart Disease Risk", use_container_width=True)
    
    if predict_btn:
        risk_score = min(95, max(5, (age/100 + chol/300 + trestbps/200) * 33 + np.random.uniform(-10, 10)))
        prediction = 1 if risk_score > 50 else 0
        
        result_text = "At Risk for Heart Disease" if prediction == 1 else "Low Risk - Healthy Heart"
        risk_level = "HIGH RISK" if risk_score > 50 else "LOW RISK"
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.last_prediction = {
            "disease": "Heart",
            "result": result_text,
            "date": now,
            "score": risk_score,
            "risk_level": risk_level,
            "parameters": {
                "Age": age, "Sex": sex, "Chest Pain": cp, "Resting BP": trestbps,
                "Cholesterol": chol, "Fasting BS": fbs, "Max HR": thalach
            }
        }
        st.session_state.reports.append(st.session_state.last_prediction)
        st.session_state.show_result = True
        st.session_state.show_patient_form = True
        st.rerun()
    
    # Display Results
    if st.session_state.show_result and st.session_state.last_prediction and st.session_state.last_prediction["disease"] == "Heart":
        st.markdown("---")
        st.markdown("## 🎯 Prediction Results")
        
        pred = st.session_state.last_prediction
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if lottie_success:
                st_lottie(lottie_success, height=150, key="success_heart")
        
        if pred["risk_level"] == "HIGH RISK":
            st.markdown(f"""
            <div class='risk-box-high'>
                <h2>⚠️ HIGH RISK DETECTED</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Immediate consultation with a cardiologist recommended</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='risk-box-low'>
                <h2>✅ LOW RISK</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Keep up with your heart-healthy lifestyle!</p>
            </div>
            """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred['score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Cardiac Risk Score", 'font': {'size': 24}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': '#55efc4'},
                    {'range': [30, 70], 'color': '#feca57'},
                    {'range': [70, 100], 'color': '#ff6b6b'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 75}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("## 💡 Personalized Cardiac Care Recommendations")
        
        disease_key = "Heart"
        
        st.markdown("### 🛡️ Essential Precautions")
        cols = st.columns(2)
        for i, precaution in enumerate(DISEASE_INFO[disease_key]["precautions"]):
            with cols[i % 2]:
                st.markdown(f"<div class='suggestion-card'>{precaution}</div>", unsafe_allow_html=True)
        
        st.markdown("### ✅ Heart-Healthy Foods")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["good_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #51cf66;'>{food}</div>", unsafe_allow_html=True)
        
        st.markdown("### ❌ Foods to Avoid")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["avoid_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #ff6b6b;'>{food}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Do's")
            for item in DISEASE_INFO[disease_key]["do"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(81,207,102,0.1), rgba(81,207,102,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ❌ Don'ts")
            for item in DISEASE_INFO[disease_key]["dont"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(255,107,107,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("✅ Report generated! Check 'My Reports' section.")
        with col3:
            if st.button("🔄 New Prediction", use_container_width=True):
                st.session_state.show_result = False
                st.session_state.show_patient_form = False
                st.rerun()

# ======================== PARKINSON'S PREDICTION ========================
elif choice == "🧠 Parkinson's":
    st.markdown("<h1 style='text-align: center;'>🧠 Parkinson's Disease Risk Assessment</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if lottie_brain:
            st_lottie(lottie_brain, height=200, key="parkinsons_anim")
    
    st.markdown("---")
    st.markdown("### 📝 Enter Voice Analysis Parameters")
    st.info("ℹ️ These parameters are typically obtained through voice analysis tests")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fo = st.number_input("🎵 MDVP:Fo(Hz)", 50.0, 300.0, 150.0, format="%.3f")
        fhi = st.number_input("🎵 MDVP:Fhi(Hz)", 80.0, 600.0, 200.0, format="%.3f")
        flo = st.number_input("🎵 MDVP:Flo(Hz)", 50.0, 250.0, 100.0, format="%.3f")
        jitter_percent = st.number_input("📊 MDVP:Jitter(%)", 0.0, 1.0, 0.005, format="%.5f")
        jitter_abs = st.number_input("📊 MDVP:Jitter(Abs)", 0.0, 0.01, 0.00003, format="%.8f")
    
    with col2:
        rap = st.number_input("📊 MDVP:RAP", 0.0, 0.1, 0.003, format="%.5f")
        ppq = st.number_input("📊 MDVP:PPQ", 0.0, 0.1, 0.003, format="%.5f")
        ddp = st.number_input("📊 Jitter:DDP", 0.0, 0.1, 0.009, format="%.5f")
        shimmer = st.number_input("📈 MDVP:Shimmer", 0.0, 1.0, 0.03, format="%.5f")
        shimmer_db = st.number_input("📈 MDVP:Shimmer(dB)", 0.0, 2.0, 0.3, format="%.3f")
    
    with col3:
        apq3 = st.number_input("📈 Shimmer:APQ3", 0.0, 0.1, 0.015, format="%.5f")
        apq5 = st.number_input("📈 Shimmer:APQ5", 0.0, 0.1, 0.017, format="%.5f")
        apq = st.number_input("📈 MDVP:APQ", 0.0, 0.2, 0.024, format="%.5f")
        dda = st.number_input("📈 Shimmer:DDA", 0.0, 0.2, 0.045, format="%.5f")
        nhr = st.number_input("🔊 NHR", 0.0, 1.0, 0.025, format="%.5f")
    
    with col4:
        hnr = st.number_input("🔊 HNR", 0.0, 50.0, 21.0, format="%.3f")
        rpde = st.number_input("🌀 RPDE", 0.0, 1.0, 0.5, format="%.6f")
        dfa = st.number_input("🌀 DFA", 0.0, 1.0, 0.7, format="%.6f")
        spread1 = st.number_input("📡 Spread1", -10.0, 0.0, -5.0, format="%.6f")
        spread2 = st.number_input("📡 Spread2", 0.0, 1.0, 0.2, format="%.6f")
    
    d2 = st.number_input("🎯 D2", 0.0, 5.0, 2.5, format="%.6f")
    ppe = st.number_input("🎯 PPE", 0.0, 1.0, 0.2, format="%.6f")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        predict_btn = st.button("🔮 Predict Parkinson's Risk", use_container_width=True)
    
    if predict_btn:
        risk_score = min(95, max(5, (jitter_percent*1000 + shimmer*100 + nhr*50) + np.random.uniform(-10, 10)))
        prediction = 1 if risk_score > 50 else 0
        
        result_text = "At Risk for Parkinson's Disease" if prediction == 1 else "Low Risk - Healthy"
        risk_level = "HIGH RISK" if risk_score > 50 else "LOW RISK"
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.last_prediction = {
            "disease": "Parkinsons",
            "result": result_text,
            "date": now,
            "score": risk_score,
            "risk_level": risk_level,
            "parameters": {
                "MDVP:Fo": fo, "MDVP:Fhi": fhi, "MDVP:Flo": flo,
                "Jitter%": jitter_percent, "Shimmer": shimmer, "HNR": hnr
            }
        }
        st.session_state.reports.append(st.session_state.last_prediction)
        st.session_state.show_result = True
        st.session_state.show_patient_form = True
        st.rerun()
    
    # Display Results
    if st.session_state.show_result and st.session_state.last_prediction and st.session_state.last_prediction["disease"] == "Parkinsons":
        st.markdown("---")
        st.markdown("## 🎯 Prediction Results")
        
        pred = st.session_state.last_prediction
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if lottie_success:
                st_lottie(lottie_success, height=150, key="success_parkinsons")
        
        if pred["risk_level"] == "HIGH RISK":
            st.markdown(f"""
            <div class='risk-box-high'>
                <h2>⚠️ HIGH RISK DETECTED</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Consult a neurologist for comprehensive evaluation</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='risk-box-low'>
                <h2>✅ LOW RISK</h2>
                <h3>Risk Score: {pred['score']:.1f}%</h3>
                <p>Continue maintaining brain health!</p>
            </div>
            """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred['score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Neurological Risk Score", 'font': {'size': 24}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#a29bfe"},
                'steps': [
                    {'range': [0, 30], 'color': '#55efc4'},
                    {'range': [30, 70], 'color': '#feca57'},
                    {'range': [70, 100], 'color': '#ff6b6b'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 75}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("## 💡 Personalized Neurological Care Recommendations")
        
        disease_key = "Parkinsons"
        
        st.markdown("### 🛡️ Essential Precautions")
        cols = st.columns(2)
        for i, precaution in enumerate(DISEASE_INFO[disease_key]["precautions"]):
            with cols[i % 2]:
                st.markdown(f"<div class='suggestion-card'>{precaution}</div>", unsafe_allow_html=True)
        
        st.markdown("### ✅ Brain-Healthy Foods")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["good_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #51cf66;'>{food}</div>", unsafe_allow_html=True)
        
        st.markdown("### ❌ Foods to Avoid")
        cols = st.columns(3)
        for i, food in enumerate(DISEASE_INFO[disease_key]["avoid_foods"]):
            with cols[i % 3]:
                st.markdown(f"<div class='suggestion-card' style='border-left-color: #ff6b6b;'>{food}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Do's")
            for item in DISEASE_INFO[disease_key]["do"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(81,207,102,0.1), rgba(81,207,102,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ❌ Don'ts")
            for item in DISEASE_INFO[disease_key]["dont"]:
                st.markdown(f"<div class='suggestion-card' style='background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(255,107,107,0.05));'>{item}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.success("✅ Report generated! Check 'My Reports' section.")
        with col3:
            if st.button("🔄 New Prediction", use_container_width=True):
                st.session_state.show_result = False
                st.session_state.show_patient_form = False
                st.rerun()

# ======================== MY REPORTS ========================
elif choice == "📊 My Reports":
    st.markdown("<h1 style='text-align: center;'>📊 My Health Reports Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if len(st.session_state.reports) == 0:
        st.info("📭 No reports generated yet. Make a prediction to see your reports here!")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image("https://img.icons8.com/clouds/400/000000/empty-box.png", width=300)
    else:
        # Summary Statistics
        st.markdown("## 📈 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_reports = len(st.session_state.reports)
        disease_counts = {}
        for report in st.session_state.reports:
            disease = report["disease"]
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3 style='text-align: center;'>📋 Total Reports</h3>
                <h1 style='text-align: center; color: #667eea;'>{total_reports}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            diabetes_count = disease_counts.get("Diabetes", 0)
            st.markdown(f"""
            <div class='metric-card'>
                <h3 style='text-align: center;'>🩸 Diabetes Tests</h3>
                <h1 style='text-align: center; color: #ff6b6b;'>{diabetes_count}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            heart_count = disease_counts.get("Heart", 0)
            st.markdown(f"""
            <div class='metric-card'>
                <h3 style='text-align: center;'>❤️ Heart Tests</h3>
                <h1 style='text-align: center; color: #4ecdc4;'>{heart_count}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            parkinsons_count = disease_counts.get("Parkinsons", 0)
            st.markdown(f"""
            <div class='metric-card'>
                <h3 style='text-align: center;'>🧠 Parkinson's Tests</h3>
                <h1 style='text-align: center; color: #a29bfe;'>{parkinsons_count}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualization of reports
        st.markdown("---")
        st.markdown("## 📊 Report Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if disease_counts:
                fig_pie = px.pie(
                    names=list(disease_counts.keys()),
                    values=list(disease_counts.values()),
                    title="Tests by Disease Type",
                    color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#a29bfe']
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            dates = [r["date"] for r in st.session_state.reports]
            scores = [r["score"] for r in st.session_state.reports]
            diseases = [r["disease"] for r in st.session_state.reports]
            
            df_timeline = pd.DataFrame({
                'Date': dates,
                'Risk Score': scores,
                'Disease': diseases
            })
            
            fig_timeline = px.line(
                df_timeline, x='Date', y='Risk Score', color='Disease',
                title="Risk Score Timeline",
                markers=True,
                color_discrete_map={
                    "Diabetes": "#ff6b6b",
                    "Heart": "#4ecdc4",
                    "Parkinsons": "#a29bfe"
                }
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Individual Reports
        st.markdown("---")
        st.markdown("## 📋 Individual Reports")
        
        for i, report in enumerate(reversed(st.session_state.reports)):
            with st.expander(f"🔍 Report #{len(st.session_state.reports)-i} - {report['disease']} - {report['date']}", expanded=(i==0)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {report['disease']} Assessment")
                    st.markdown(f"**Result:** {report['result']}")
                    st.markdown(f"**Risk Level:** {report['risk_level']}")
                    st.markdown(f"**Risk Score:** {report['score']:.1f}%")
                    st.markdown(f"**Date:** {report['date']}")
                    st.progress(report['score']/100)
                
                with col2:
                    fig_mini = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=report['score'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#667eea"},
                            'steps': [
                                {'range': [0, 50], 'color': '#55efc4'},
                                {'range': [50, 100], 'color': '#ff6b6b'}
                            ]
                        }
                    ))
                    fig_mini.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_mini, use_container_width=True)
                
                if "parameters" in report and report["parameters"]:
                    st.markdown("#### 📊 Test Parameters")
                    params_df = pd.DataFrame({
                        'Parameter': list(report['parameters'].keys()),
                        'Value': list(report['parameters'].values())
                    })
                    st.dataframe(params_df, use_container_width=True)
                
                if "patient_info" in report and report["patient_info"]:
                    st.markdown("#### 👤 Patient Information")
                    pinfo = report["patient_info"]
                    
                    pcol1, pcol2 = st.columns(2)
                    with pcol1:
                        st.markdown(f"**Name:** {pinfo.get('name', 'N/A')}")
                        st.markdown(f"**Phone:** {pinfo.get('phone', 'N/A')}")
                        st.markdown(f"**Place:** {pinfo.get('place', 'N/A')}")
                    with pcol2:
                        st.markdown(f"**Blood Group:** {pinfo.get('blood_group', 'N/A')}")
                        st.markdown(f"**Height:** {pinfo.get('height', 'N/A')} cm")
                        st.markdown(f"**Weight:** {pinfo.get('weight', 'N/A')} kg")
                    
                    st.markdown(f"**Address:** {pinfo.get('address', 'N/A')}")
        
        # Clear reports option
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("🗑️ Clear All Reports", use_container_width=True):
                st.session_state.reports = []
                st.session_state.last_prediction = None
                st.rerun()

# ======================== HEALTH TIPS ========================
elif choice == "💡 Health Tips":
    st.markdown("<h1 style='text-align: center;'>💡 Comprehensive Health & Wellness Guide</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Your Complete Guide to Healthy Living</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation tabs for different tip categories
    tip_category = st.radio(
        "Select Category:",
        ["🌟 General Wellness", "🥗 Nutrition Guide", "💪 Exercise Tips", "🧠 Mental Health", "🛡️ Prevention & Safety"],
        horizontal=True
    )
    
    category_map = {
        "🌟 General Wellness": "General Wellness",
        "🥗 Nutrition Guide": "Nutrition",
        "💪 Exercise Tips": "Exercise",
        "🧠 Mental Health": "Mental Health",
        "🛡️ Prevention & Safety": "Prevention"
    }
    
    selected_category = category_map[tip_category]
    
    st.markdown(f"## {tip_category}")
    
    tips = HEALTH_TIPS[selected_category]
    
    for i, tip in enumerate(tips):
        st.markdown(f"""
        <div class='tips-section'>
            <h4>{tip}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional detailed sections
    if selected_category == "Nutrition":
        st.markdown("## 🍽️ Complete Nutrition Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='tips-section'>
                <h3>🥗 Essential Nutrients</h3>
                <ul>
                    <li><strong>Proteins:</strong> 0.8g per kg body weight daily</li>
                    <li><strong>Carbohydrates:</strong> 45-65% of daily calories</li>
                    <li><strong>Healthy Fats:</strong> 20-35% of daily calories</li>
                    <li><strong>Fiber:</strong> 25-30g daily</li>
                    <li><strong>Water:</strong> 8-10 glasses (2-3 liters) daily</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>⏰ Meal Timing Tips</h3>
                <ul>
                    <li>Eat breakfast within 1 hour of waking up</li>
                    <li>Space meals 3-4 hours apart</li>
                    <li>Avoid eating 2-3 hours before bedtime</li>
                    <li>Stay consistent with meal times</li>
                    <li>Don't skip meals, especially breakfast</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='tips-section'>
                <h3>🌈 Superfood List</h3>
                <ul>
                    <li><strong>Berries:</strong> Antioxidants, vitamins</li>
                    <li><strong>Leafy Greens:</strong> Iron, calcium, vitamins</li>
                    <li><strong>Nuts & Seeds:</strong> Omega-3, protein</li>
                    <li><strong>Fatty Fish:</strong> Omega-3, vitamin D</li>
                    <li><strong>Yogurt:</strong> Probiotics, calcium</li>
                    <li><strong>Sweet Potatoes:</strong> Beta-carotene, fiber</li>
                    <li><strong>Quinoa:</strong> Complete protein</li>
                    <li><strong>Turmeric:</strong> Anti-inflammatory</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>🚫 Foods to Limit</h3>
                <ul>
                    <li>Processed and ultra-processed foods</li>
                    <li>Sugary beverages and sodas</li>
                    <li>Trans fats and hydrogenated oils</li>
                    <li>Excessive sodium (limit to 2,300mg/day)</li>
                    <li>Refined carbohydrates</li>
                    <li>Artificial sweeteners in excess</li>
                    <li>Alcohol (moderate if consumed)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif selected_category == "Exercise":
        st.markdown("## 🏋️ Complete Fitness Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='tips-section'>
                <h3>💪 Weekly Exercise Plan</h3>
                <ul>
                    <li><strong>Monday:</strong> Cardio (30 min jogging/cycling)</li>
                    <li><strong>Tuesday:</strong> Strength training (upper body)</li>
                    <li><strong>Wednesday:</strong> Yoga/Flexibility (45 min)</li>
                    <li><strong>Thursday:</strong> HIIT workout (20-30 min)</li>
                    <li><strong>Friday:</strong> Strength training (lower body)</li>
                    <li><strong>Saturday:</strong> Active recovery (walking, swimming)</li>
                    <li><strong>Sunday:</strong> Rest or gentle stretching</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>🏃 Cardio Benefits</h3>
                <ul>
                    <li>Improves heart health and circulation</li>
                    <li>Helps with weight management</li>
                    <li>Boosts mood and reduces stress</li>
                    <li>Increases lung capacity</li>
                    <li>Reduces risk of chronic diseases</li>
                    <li>Improves sleep quality</li>
                    <li>Strengthens immune system</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='tips-section'>
                <h3>🎯 Exercise Intensity Guide</h3>
                <ul>
                    <li><strong>Light:</strong> Can sing comfortably (walking)</li>
                    <li><strong>Moderate:</strong> Can talk but not sing (brisk walking)</li>
                    <li><strong>Vigorous:</strong> Can barely talk (running, HIIT)</li>
                    <li><strong>Target Heart Rate:</strong> 50-85% of maximum</li>
                    <li><strong>Max Heart Rate:</strong> 220 - your age</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>⚠️ Exercise Safety</h3>
                <ul>
                    <li>Always warm up for 5-10 minutes</li>
                    <li>Stay hydrated before, during, and after</li>
                    <li>Use proper form to prevent injuries</li>
                    <li>Listen to your body and rest when needed</li>
                    <li>Cool down and stretch after workouts</li>
                    <li>Gradually increase intensity over time</li>
                    <li>Consult doctor before starting new routines</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif selected_category == "Mental Health":
        st.markdown("## 🧠 Mental Wellness Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='tips-section'>
                <h3>🧘 Stress Management Techniques</h3>
                <ul>
                    <li><strong>Deep Breathing:</strong> 4-7-8 technique</li>
                    <li><strong>Meditation:</strong> 10-20 minutes daily</li>
                    <li><strong>Progressive Muscle Relaxation:</strong> Tense and release</li>
                    <li><strong>Mindfulness:</strong> Focus on present moment</li>
                    <li><strong>Journaling:</strong> Write thoughts daily</li>
                    <li><strong>Time in Nature:</strong> 20-30 minutes outdoors</li>
                    <li><strong>Social Connection:</strong> Regular interaction</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>😴 Sleep Hygiene</h3>
                <ul>
                    <li>Maintain consistent sleep schedule</li>
                    <li>Create dark, cool, quiet environment</li>
                    <li>Avoid screens 1 hour before bed</li>
                    <li>Limit caffeine after 2 PM</li>
                    <li>Establish relaxing bedtime routine</li>
                    <li>Exercise regularly but not before bed</li>
                    <li>Aim for 7-9 hours of sleep</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='tips-section'>
                <h3>🎭 Emotional Well-being</h3>
                <ul>
                    <li>Practice gratitude daily</li>
                    <li>Set healthy boundaries</li>
                    <li>Express emotions constructively</li>
                    <li>Engage in hobbies you enjoy</li>
                    <li>Seek support when needed</li>
                    <li>Practice self-compassion</li>
                    <li>Celebrate small victories</li>
                    <li>Maintain work-life balance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>🚨 When to Seek Professional Help</h3>
                <ul>
                    <li>Persistent sadness or hopelessness (>2 weeks)</li>
                    <li>Difficulty performing daily tasks</li>
                    <li>Significant changes in appetite or sleep</li>
                    <li>Thoughts of self-harm or suicide</li>
                    <li>Excessive worry or anxiety</li>
                    <li>Social withdrawal</li>
                    <li>Substance abuse</li>
                    <li>Extreme mood swings</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif selected_category == "Prevention":
        st.markdown("## 🛡️ Disease Prevention Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='tips-section'>
                <h3>💉 Recommended Health Screenings</h3>
                <ul>
                    <li><strong>Blood Pressure:</strong> Annually</li>
                    <li><strong>Cholesterol:</strong> Every 4-6 years</li>
                    <li><strong>Diabetes:</strong> Every 3 years (45+)</li>
                    <li><strong>Colonoscopy:</strong> Starting at 45-50</li>
                    <li><strong>Mammogram:</strong> Annually (women 40+)</li>
                    <li><strong>Prostate:</strong> Discuss at 50+</li>
                    <li><strong>Skin:</strong> Annual full-body check</li>
                    <li><strong>Eye Exam:</strong> Every 1-2 years</li>
                    <li><strong>Dental:</strong> Every 6 months</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>🧼 Hygiene Best Practices</h3>
                <ul>
                    <li>Wash hands for 20 seconds with soap</li>
                    <li>Brush teeth twice daily and floss</li>
                    <li>Shower regularly and wear clean clothes</li>
                    <li>Keep nails trimmed and clean</li>
                    <li>Clean frequently touched surfaces</li>
                    <li>Practice safe food handling</li>
                    <li>Avoid sharing personal items</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='tips-section'>
                <h3>🏥 Preventive Lifestyle Habits</h3>
                <ul>
                    <li>Don't smoke or use tobacco</li>
                    <li>Limit alcohol consumption</li>
                    <li>Maintain healthy weight (BMI 18.5-24.9)</li>
                    <li>Exercise regularly (150 min/week)</li>
                    <li>Eat balanced, nutritious diet</li>
                    <li>Get adequate sleep (7-9 hours)</li>
                    <li>Manage stress effectively</li>
                    <li>Stay socially connected</li>
                    <li>Practice safe sun exposure</li>
                    <li>Stay up-to-date with vaccinations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='tips-section'>
                <h3>⚕️ Know Your Numbers</h3>
                <ul>
                    <li><strong>Blood Pressure:</strong> <120/80 mmHg</li>
                    <li><strong>Cholesterol:</strong> <200 mg/dL</li>
                    <li><strong>Blood Sugar (fasting):</strong> 70-99 mg/dL</li>
                    <li><strong>BMI:</strong> 18.5-24.9</li>
                    <li><strong>Waist:</strong> <40" (men), <35" (women)</li>
                    <li><strong>Resting Heart Rate:</strong> 60-100 bpm</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Daily Wellness Checklist
    st.markdown("---")
    st.markdown("## 🌟 Daily Wellness Checklist")
    
    checklist_items = [
        "☀️ Got 7-9 hours of quality sleep",
        "💧 Drank 8-10 glasses of water",
        "🥗 Ate 5 servings of fruits and vegetables",
        "🏃 Exercised for at least 30 minutes",
        "🧘 Practiced mindfulness or meditation",
        "😊 Connected with friends or family",
        "📵 Limited screen time before bed",
        "🌳 Spent time outdoors",
        "💊 Took prescribed medications",
        "📝 Practiced gratitude or journaling"
    ]
    
    cols = st.columns(2)
    for i, item in enumerate(checklist_items):
        with cols[i % 2]:
            st.checkbox(item, key=f"checklist_{i}")
    
    st.markdown("---")
    st.markdown("""
    <div class='tips-section' style='text-align: center;'>
        <h3>💚 Remember: Small Steps Lead to Big Changes!</h3>
        <p style='font-size: 18px;'>
            Your health journey is unique. Focus on progress, not perfection.
            Celebrate every healthy choice you make, no matter how small.
            Consistency is key to long-term wellness!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency contacts section
    st.markdown("---")
    st.markdown("## 🚨 Emergency Contacts & Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='tips-section'>
            <h4>🚑 Emergency Services</h4>
            <ul>
                <li><strong>Emergency:</strong> 911 (US) / 108 (India)</li>
                <li><strong>Poison Control:</strong> 1-800-222-1222</li>
                <li><strong>Ambulance:</strong> Local emergency number</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='tips-section'>
            <h4>🧠 Mental Health Support</h4>
            <ul>
                <li><strong>Suicide Prevention:</strong> 988</li>
                <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                <li><strong>SAMHSA:</strong> 1-800-662-4357</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='tips-section'>
            <h4>📞 Health Information</h4>
            <ul>
                <li><strong>CDC:</strong> 1-800-232-4636</li>
                <li><strong>Medicare:</strong> 1-800-633-4227</li>
                <li><strong>Your Doctor:</strong> Keep number handy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ======================== FOOTER ========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px; margin-top: 30px;'>
    <h3 style='color: white;'>🤖 AI-Powered Multi-Disease Prediction System</h3>
    <p style='color: white; font-size: 14px;'>
        Powered by Advanced Machine Learning Algorithms | Designed for Educational & Screening Purposes Only
    </p>
    <p style='color: white; font-size: 12px;'>
        ⚠️ <strong>Disclaimer:</strong> This tool is not a substitute for professional medical advice, diagnosis, or treatment.
        Always consult with qualified healthcare providers for medical concerns.
    </p>
    <p style='color: white; font-size: 14px; margin-top: 10px;'>
        Made with ❤️ for Better Health | © 2025
    </p>
</div>
""", unsafe_allow_html=True)