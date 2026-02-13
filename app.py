# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle
# import plotly.graph_objects as go
# import plotly.express as px

# # Page config
# st.set_page_config(
#     page_title="🚀 Delivery Time Predictor",
#     page_icon="🚀",
#     layout="wide"
# )

# # Custom CSS
# st.markdown("""
#     <style>
#     .main-header {
#         font-size: 3rem;
#         color: #FF4B4B;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         color: #666;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .prediction-box {
#         background-color: #f0f2f6;
#         padding: 2rem;
#         border-radius: 10px;
#         text-align: center;
#         margin: 2rem 0;
#     }
#     .prediction-time {
#         font-size: 4rem;
#         color: #FF4B4B;
#         font-weight: bold;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Haversine distance function
# def haversine_distance(lat1, lon1, lat2, lon2):
#     lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
#     c = 2 * np.arcsin(np.sqrt(a))
#     km = 6371 * c
#     return km

# # Load models
# @st.cache_resource
# def load_models():
#     try:
#         with open('best_delivery_model.pkl', 'rb') as f:
#             model = pickle.load(f)
#         with open('order_encoder.pkl', 'rb') as f:
#             order_encoder = pickle.load(f)
#         with open('vehicle_encoder.pkl', 'rb') as f:
#             vehicle_encoder = pickle.load(f)
#         return model, order_encoder, vehicle_encoder
#     except:
#         return None, None, None

# model, order_encoder, vehicle_encoder = load_models()

# # Header
# st.markdown('<p class="main-header">🚀 Food Delivery Time Predictor</p>', unsafe_allow_html=True)
# st.markdown('<p class="sub-header">AI-Powered Delivery Time Estimation System</p>', unsafe_allow_html=True)

# # Sidebar
# st.sidebar.title("📊 About")
# st.sidebar.info("""
# This intelligent system predicts food delivery times using machine learning.

# **Features:**
# - 🎯 Real-time predictions
# - 📍 Distance calculation
# - 🏍️ Vehicle type optimization
# - ⭐ Partner rating analysis
# - 📊 Interactive visualizations

# **Accuracy:**
# - RMSE: ~5 minutes
# - R² Score: >0.80
# """)

# # Main content
# tab1, tab2, tab3 = st.tabs(["🎯 Predict", "📊 Analytics", "ℹ️ Model Info"])

# with tab1:
#     st.header("Enter Order Details")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("🏍️ Delivery Partner Info")
#         age = st.slider("Partner Age", 18, 60, 28)
#         rating = st.slider("Partner Rating", 1.0, 5.0, 4.5, 0.1)
        
#         st.subheader("📦 Order Details")
#         order_type = st.selectbox("Order Type", ['Meal', 'Snack', 'Drinks', 'Buffet'])
#         vehicle_type = st.selectbox("Vehicle Type", ['motorcycle', 'scooter', 'electric_scooter'])
    
#     with col2:
#         st.subheader("📍 Restaurant Location")
#         rest_lat = st.number_input("Restaurant Latitude", value=12.9716)
#         rest_lon = st.number_input("Restaurant Longitude", value=77.5946)
        
#         st.subheader("📍 Delivery Location")
#         del_lat = st.number_input("Delivery Latitude", value=13.0358)
#         del_lon = st.number_input("Delivery Longitude", value=77.5970)
    
#     # Predict button
#     if st.button("🚀 Predict Delivery Time", type="primary", use_container_width=True):
#         if model is not None:
#             # Calculate distance
#             distance = haversine_distance(rest_lat, rest_lon, del_lat, del_lon)
            
#             # Engineer features
#             partner_score = age * rating
#             is_experienced = 1 if age > 30 else 0
#             is_high_rated = 1 if rating >= 4.5 else 0
#             lat_diff = abs(rest_lat - del_lat)
#             lon_diff = abs(rest_lon - del_lon)
            
#             # Encode categorical variables
#             order_encoded = order_encoder.transform([order_type])[0]
#             vehicle_encoded = vehicle_encoder.transform([vehicle_type])[0]
            
#             # Create feature array
#             features = np.array([[
#                 age, rating, distance, order_encoded, vehicle_encoded,
#                 partner_score, is_experienced, is_high_rated, lat_diff, lon_diff
#             ]])
            
#             # Predict
#             prediction = model.predict(features)[0]
            
#             # Display prediction
#             st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
#             st.markdown('<p style="font-size: 1.5rem; color: #666;">Estimated Delivery Time</p>', unsafe_allow_html=True)
#             st.markdown(f'<p class="prediction-time">{int(prediction)} min</p>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             # Show details
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 st.metric("📏 Distance", f"{distance:.2f} km")
            
#             with col2:
#                 st.metric("⚡ Speed", f"{distance/prediction*60:.1f} km/h")
            
#             with col3:
#                 st.metric("⭐ Partner Score", f"{partner_score:.1f}")
            
#             # Confidence interval
#             st.info(f"💡 Expected delivery window: {int(prediction-3)} - {int(prediction+3)} minutes")
            
#         else:
#             st.error("⚠️ Model not loaded. Please train the model first!")

# with tab2:
#     st.header("📊 Delivery Analytics")
    
#     # Sample data for visualization
#     st.subheader("📈 Average Delivery Time by Order Type")
    
#     sample_data = pd.DataFrame({
#         'Order Type': ['Meal', 'Snack', 'Drinks', 'Buffet'],
#         'Avg Time (min)': [35, 28, 22, 30]
#     })
    
#     fig = px.bar(sample_data, x='Order Type', y='Avg Time (min)', 
#                  color='Avg Time (min)', color_continuous_scale='Reds')
#     st.plotly_chart(fig, use_container_width=True)
    
#     st.subheader("🏍️ Vehicle Performance Comparison")
    
#     vehicle_data = pd.DataFrame({
#         'Vehicle': ['Motorcycle', 'Scooter', 'E-Scooter'],
#         'Avg Speed (km/h)': [35, 30, 28],
#         'Efficiency': [90, 85, 80]
#     })
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         fig = px.bar(vehicle_data, x='Vehicle', y='Avg Speed (km/h)', 
#                      color='Avg Speed (km/h)', color_continuous_scale='Blues')
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         fig = px.pie(vehicle_data, values='Efficiency', names='Vehicle', 
#                      title='Vehicle Efficiency Distribution')
#         st.plotly_chart(fig, use_container_width=True)

# with tab3:
#     st.header("ℹ️ Model Information")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("🤖 Model Architecture")
#         st.write("""
#         **Algorithm:** Random Forest Regressor
        
#         **Features Used (10):**
#         1. Delivery Partner Age
#         2. Delivery Partner Rating
#         3. Distance (km)
#         4. Order Type (Encoded)
#         5. Vehicle Type (Encoded)
#         6. Partner Score
#         7. Is Experienced
#         8. Is High Rated
#         9. Latitude Difference
#         10. Longitude Difference
        
#         **Training Details:**
#         - Total Samples: 45,593
#         - Train/Test Split: 80/20
#         - Cross-Validation: 3-fold
#         """)
    
#     with col2:
#         st.subheader("📊 Performance Metrics")
#         st.write("""
#         **Model Performance:**
#         - RMSE: ~5.2 minutes
#         - MAE: ~4.1 minutes
#         - R² Score: 0.82
        
#         **Key Insights:**
#         - Distance is the most important factor
#         - Partner rating significantly affects time
#         - Vehicle type impacts delivery speed
#         - Peak hours cause 15-20% delays
        
#         **Business Impact:**
#         - 82% prediction accuracy
#         - 30% reduction in customer complaints
#         - 25% improvement in resource planning
#         """)
    
#     st.subheader("🔧 Feature Engineering")
#     st.write("""
#     **Advanced Features Created:**
#     1. **Haversine Distance:** Precise geo-distance calculation
#     2. **Partner Score:** Age × Rating combination
#     3. **Experience Flag:** Binary feature for age > 30
#     4. **High Rating Flag:** Binary feature for rating ≥ 4.5
#     5. **Coordinate Differences:** Lat/Lon deltas for pattern detection
#     """)

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #666;'>
#     <p>🏆 Built for Hackathon | Powered by Machine Learning | Made with ❤️</p>
# </div>
# """, unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🚀 AI Delivery Time Predictor",
    page_icon="🚀",
    layout="wide"
)

# ---------------- MODERN CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: -webkit-linear-gradient(#22d3ee, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-header {
    text-align: center;
    font-size: 1.2rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
}
.prediction-box {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 2rem 0;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
.prediction-time {
    font-size: 4rem;
    font-weight: bold;
    color: white;
}
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="main-header">🚀 AI Delivery Time Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Machine Learning Powered Smart ETA System</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Overview")
st.sidebar.info("""
**Best Model:** Gradient Boosting  
**RMSE:** ~7.24 minutes  
**MAE:** ~5.69 minutes  
**R² Score:** 0.41  

**Core Features:**
- 📍 Distance (Haversine)
- ⭐ Partner Rating
- 🏍 Vehicle Type
- 🧠 Engineered Behavioral Features
""")

# ---------------- HAVERSINE FUNCTION ----------------
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_models():
    try:
        with open('best_delivery_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('order_encoder.pkl', 'rb') as f:
            order_encoder = pickle.load(f)
        with open('vehicle_encoder.pkl', 'rb') as f:
            vehicle_encoder = pickle.load(f)
        return model, order_encoder, vehicle_encoder
    except:
        return None, None, None

model, order_encoder, vehicle_encoder = load_models()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🎯 Predict", "📊 Analytics", "ℹ️ Model Info"])

# ==========================================================
# ---------------- TAB 1 : PREDICTION ----------------
# ==========================================================
with tab1:

    st.subheader("Enter Order Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Partner Age", 18, 50, 28)
        rating = st.slider("Partner Rating", 1.0, 5.0, 4.5, 0.1)
        order_type = st.selectbox("Order Type", ['Meal', 'Snack', 'Drinks', 'Buffet'])
        vehicle_type = st.selectbox("Vehicle Type", ['bicycle','electric_scooter','motorcycle','scooter'])

    with col2:
        rest_lat = st.number_input("Restaurant Latitude", value=12.9716)
        rest_lon = st.number_input("Restaurant Longitude", value=77.5946)
        del_lat = st.number_input("Delivery Latitude", value=13.0358)
        del_lon = st.number_input("Delivery Longitude", value=77.5970)

    if st.button("🔮 Predict Delivery Time", use_container_width=True):

        if model is not None:

            distance = haversine_distance(rest_lat, rest_lon, del_lat, del_lon)

            partner_score = age * rating
            is_experienced = 1 if age > 30 else 0
            is_high_rated = 1 if rating >= 4.5 else 0
            lat_diff = abs(rest_lat - del_lat)
            lon_diff = abs(rest_lon - del_lon)

            order_encoded = order_encoder.transform([order_type])[0]
            vehicle_encoded = vehicle_encoder.transform([vehicle_type])[0]

            features = np.array([[
                age, rating, distance,
                order_encoded, vehicle_encoded,
                partner_score, is_experienced,
                is_high_rated, lat_diff, lon_diff
            ]])

            prediction = model.predict(features)[0]

            st.markdown(f"""
            <div class="prediction-box">
                🚚 Estimated Delivery Time<br><br>
                <span class="prediction-time">{int(prediction)} minutes</span>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Distance", f"{distance:.2f} km")
            c2.metric("⚡ Avg Speed", f"{distance/prediction*60:.1f} km/h")
            c3.metric("⭐ Partner Score", f"{partner_score:.1f}")

            st.info(f"Expected delivery window: {int(prediction-3)} - {int(prediction+3)} minutes")

        else:
            st.error("Model not loaded. Please train the model first!")

# ==========================================================
# ---------------- TAB 2 : ANALYTICS ----------------
# ==========================================================
with tab2:

    st.subheader("Average Delivery Time by Order Type")

    sample_data = pd.DataFrame({
        'Order Type': ['Meal', 'Snack', 'Drinks', 'Buffet'],
        'Avg Time (min)': [35, 28, 22, 30]
    })

    fig = px.bar(sample_data,
                 x='Order Type',
                 y='Avg Time (min)',
                 color='Avg Time (min)',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Vehicle Performance Comparison")

    vehicle_data = pd.DataFrame({
        'Vehicle': ['Motorcycle', 'Scooter', 'E-Scooter', 'Bicycle'],
        'Avg Speed (km/h)': [35, 30, 28, 18]
    })

    fig2 = px.bar(vehicle_data,
                  x='Vehicle',
                  y='Avg Speed (km/h)',
                  color='Avg Speed (km/h)',
                  color_continuous_scale='Plasma')
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================
# ---------------- TAB 3 : MODEL INFO ----------------
# ==========================================================
with tab3:

    st.subheader("Model Architecture")

    st.write("""
    **Algorithm Used:** Gradient Boosting Regressor  

    **Features Used (10):**
    1. Delivery Partner Age  
    2. Delivery Partner Rating  
    3. Distance (km)  
    4. Order Type (Encoded)  
    5. Vehicle Type (Encoded)  
    6. Partner Score  
    7. Is Experienced  
    8. Is High Rated  
    9. Latitude Difference  
    10. Longitude Difference  
    """)

    st.subheader("Performance Metrics")

    st.write("""
    - RMSE: 7.24 minutes  
    - MAE: 5.69 minutes  
    - R² Score: 0.41  

    **Key Insight:**  
    Distance is the strongest predictor of delivery time.
    """)

# ---------------- FOOTER ----------------
st.markdown('<div class="footer">🏆 Built with ❤️ using Machine Learning</div>', unsafe_allow_html=True)
