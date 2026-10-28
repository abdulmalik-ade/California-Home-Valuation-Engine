import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Set premium page configuration
st.set_page_config(
    page_title="California Home Valuation Engine",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced custom styling for a sleek, corporate-grade dashboard
st.markdown("""
    <style>
        /* Base imports & variables */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Sleek Top Banner */
        .header-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
            padding: 2.5rem 2rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
        }
        .header-banner h1 {
            font-size: 2.75rem !important;
            font-weight: 800 !important;
            margin: 0 0 0.5rem 0 !important;
            letter-spacing: -1px;
            color: #ffffff !important;
        }
        .header-banner p {
            font-size: 1.1rem;
            font-weight: 300;
            margin: 0;
            opacity: 0.95;
            color: #93c5fd;
        }

        /* Key Metrics Card */
        .valuation-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            border: 1px solid #e2e8f0;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
            margin-bottom: 1.5rem;
            transition: transform 0.2s ease;
        }
        .valuation-card:hover {
            transform: translateY(-2px);
        }
        .valuation-label {
            text-transform: uppercase;
            font-size: 0.85rem;
            font-weight: 700;
            color: #64748b;
            letter-spacing: 1.5px;
            margin-bottom: 0.75rem;
        }
        .valuation-price {
            font-size: 3.25rem;
            font-weight: 800;
            color: #1e3a8a;
            margin: 0 0 1rem 0;
            letter-spacing: -1px;
        }

        /* Metric Sub-items */
        .spec-grid {
            display: flex;
            justify-content: space-around;
            border-top: 1px solid #f1f5f9;
            padding-top: 1.25rem;
            margin-top: 1rem;
        }
        .spec-item {
            text-align: center;
        }
        .spec-val {
            font-weight: 700;
            color: #334155;
            font-size: 1.1rem;
        }
        .spec-lbl {
            font-size: 0.75rem;
            color: #94a3b8;
        }
    </style>
""", unsafe_allow_html=True)

# Load trained model gracefully
@st.cache_resource
def load_model():
    try:
        return joblib.load('california_housing_rf.joblib')
    except Exception as e:
        st.error(f"Failed to load model file. Please ensure 'california_housing_rf.joblib' is in the same directory. Error: {e}")
        return None

model = load_model()

# Main Header Banner
st.markdown("""
    <div class='header-banner'>
        <h1>🏠 California Home Valuation Engine</h1>
        <p>Instant Machine Learning Predictions with Real-Time Coordinate Mapping</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for user inputs (keeps main panel clean and spacious)
with st.sidebar:
    st.markdown("### 🛠️ Property Specifications")
    st.write("Adjust sliders to change property details:")

    med_inc = st.slider(
        "Median Income (in $10k blocks)", 
        min_value=0.5, max_value=15.0, value=3.8, step=0.1,
        help="Median income of households in the block group"
    )
    house_age = st.slider("Housing Median Age (Years)", min_value=1, max_value=52, value=28, step=1)
    rooms = st.slider("Total Rooms", min_value=10, max_value=10000, value=2500, step=50)
    bedrooms = st.slider("Total Bedrooms", min_value=5, max_value=3000, value=500, step=10)
    pop = st.slider("Block Population", min_value=10, max_value=15000, value=1400, step=50)
    households = st.slider("Households Count", min_value=5, max_value=5000, value=500, step=10)

    st.markdown("--- ")
    st.markdown("### 📍 Location Details")
    lat = st.number_input("Latitude", min_value=32.0, max_value=42.0, value=34.05, step=0.01)
    lon = st.number_input("Longitude", min_value=-124.5, max_value=-114.0, value=-118.24, step=0.01)

# Main Dashboard
if model is not None:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### 📊 Valuation Analysis")

        # Prepare feature vector for model prediction
        features = np.array([[lon, lat, house_age, rooms, bedrooms, pop, households, med_inc]])
        predicted_value = model.predict(features)[0]

        # Beautiful KPI Output Container
        st.markdown(f"""
            <div class='valuation-card'>
                <div class='valuation-label'>Estimated Market Value</div>
                <div class='valuation-price'>${predicted_value:,.2f}</div>
                <div class='spec-grid'>
                    <div class='spec-item'>
                        <div class='spec-val'>${med_inc*10:,.1f}k</div>
                        <div class='spec-lbl'>Avg Income</div>
                    </div>
                    <div class='spec-item'>
                        <div class='spec-val'>{house_age} Yrs</div>
                        <div class='spec-lbl'>Home Age</div>
                    </div>
                    <div class='spec-item'>
                        <div class='spec-val'>{rooms}</div>
                        <div class='spec-lbl'>Total Rooms</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗺️ Geographical Location Map")
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data, zoom=11)

    with col2:
        st.markdown("### ℹ️ Engine Information")
        st.success("**Active Model:** Random Forest Regressor")
        st.info("💡 **Pro Tip:** Increase the *Median Income* slider in the sidebar to see how local economic demographics dramatically influence housing prices.")

        # Performance stats container
        st.markdown("""
            <div style='background-color:#ffffff; padding:1.25rem; border-radius:12px; border:1px solid #e2e8f0; margin-top:1rem;'>
                <h4 style='margin-top:0; color:#1e3a8a;'>📉 Model Metrics</h4>
                <ul style='margin-bottom:0; padding-left:1.2rem; color:#475569;'>
                    <li><strong>R² Score:</strong> 82.28%</li>
                    <li><strong>Validation RMSE:</strong> $49,414.55</li>
                    <li><strong>Database Size:</strong> 17,000 properties</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
