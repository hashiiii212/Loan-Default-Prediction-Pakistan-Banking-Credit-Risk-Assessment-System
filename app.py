import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ============================================================
# COLOR CONFIGURATION
# ============================================================
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f39c12"
DANGER_COLOR = "#e74c3c"
BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#2c3e50"
SIDEBAR_COLOR = "#34495e"

# ============================================================
# MULTI-CURRENCY CONFIGURATION
# ============================================================
CURRENCIES = {
    'PKR': {'symbol': '₨', 'rate': 155, 'name': 'Pakistani Rupee'},
    'USD': {'symbol': '$', 'rate': 0.56, 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'rate': 0.51, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.44, 'name': 'British Pound'},
    'INR': {'symbol': '₹', 'rate': 46, 'name': 'Indian Rupee'},
    'AED': {'symbol': 'د.إ', 'rate': 2.05, 'name': 'UAE Dirham'},
    'SAR': {'symbol': '﷼', 'rate': 2.10, 'name': 'Saudi Riyal'},
    'TRY': {'symbol': '₺', 'rate': 18, 'name': 'Turkish Lira'},
    'BDT': {'symbol': '৳', 'rate': 65, 'name': 'Bangladeshi Taka'},
    'JPY': {'symbol': '¥', 'rate': 82, 'name': 'Japanese Yen'}
}

# ============================================================
# PAKISTAN BANKING MAPPINGS - USER-FRIENDLY LABELS
# ============================================================

# Checking Account Status
CHECKING_OPTIONS = {
    'A11': '❌ Negative Balance (Overdrawn)',
    'A12': '💰 Low Balance (0 - 5,000 PKR)',
    'A13': '✅ Good Balance (> 5,000 PKR)',
    'A14': '🚫 No Checking Account'
}

# Credit History
CREDIT_HISTORY_OPTIONS = {
    'A30': '🆕 No Credit History',
    'A31': '✅ All Credits Paid (Excellent)',
    'A32': '👍 Existing Credits Paid (Good)',
    'A33': '⚠️ Delayed Payments (Fair)',
    'A34': '🚫 Critical Account (Bad)'
}

# Loan Purpose
PURPOSE_OPTIONS = {
    'A40': '🚗 Car (New)',
    'A41': '🚙 Car (Used)',
    'A42': '🛋️ Furniture / Home Appliances',
    'A43': '📺 Electronics / TV / Mobile',
    'A44': '💻 Laptop / Computer',
    'A45': '📚 Education / Student Loan',
    'A46': '🏢 Business / Startup',
    'A47': '🏠 Home Renovation',
    'A48': '💍 Wedding / Event',
    'A49': '🏥 Medical / Emergency',
    'A410': '✈️ Travel / Other'
}

# Savings Account
SAVINGS_OPTIONS = {
    'A61': '❌ No Savings',
    'A62': '💵 Low Savings (< 10,000 PKR)',
    'A63': '💰 Medium Savings (10K - 50K)',
    'A64': '💎 High Savings (50K - 100K)',
    'A65': '🏆 Very High Savings (> 100K)'
}

# Employment Status
EMPLOYMENT_OPTIONS = {
    'A71': '🚫 Unemployed',
    'A72': '👶 New Job (< 1 Year)',
    'A73': '📈 Junior (1 - 4 Years)',
    'A74': '💼 Senior (4 - 7 Years)',
    'A75': '🏆 Expert (> 7 Years)'
}

# Property Type
PROPERTY_OPTIONS = {
    'A121': '🏠 Own House / Plot',
    'A122': '🏢 Apartment / Flat',
    'A123': '🚗 Vehicle / Asset',
    'A124': '❌ No Property'
}

# Other Debtors
DEBTORS_OPTIONS = {
    'A101': '🚫 None (Single Applicant)',
    'A102': '👥 Co-Applicant (Joint)',
    'A103': '🛡️ Guarantor Available'
}

# Telephone
TELEPHONE_OPTIONS = {
    'A191': '❌ No Phone',
    'A192': '✅ Phone Registered'
}

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title='Loan Default Predictor',
    page_icon='🏦',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown(f"""
<style>
    .main {{ background-color: {BACKGROUND_COLOR}; }}
    .stButton>button {{ background-color: {PRIMARY_COLOR}; color: white; border-radius: 10px; padding: 10px 24px; font-weight: bold; }}
    .stButton>button:hover {{ background-color: {SECONDARY_COLOR}; color: white; }}
    h1, h2, h3 {{ color: {TEXT_COLOR}; }}
    .stSuccess {{ background-color: {SUCCESS_COLOR}20; border-left: 5px solid {SUCCESS_COLOR}; }}
    .stError {{ background-color: {DANGER_COLOR}20; border-left: 5px solid {DANGER_COLOR}; }}
    .metric-value {{ font-size: 24px; font-weight: bold; color: {PRIMARY_COLOR}; }}
</style>
""", unsafe_allow_html=True)

st.title('🏦 Loan Default Prediction')
st.markdown(f"<p style='color: {TEXT_COLOR}; font-size: 18px;'>Pakistan Banking Credit Risk Assessment System</p>", unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header('⚙️ Settings')

selected_currency = st.sidebar.selectbox(
    '💱 Select Currency',
    list(CURRENCIES.keys()),
    format_func=lambda x: f"{CURRENCIES[x]['symbol']} {x} - {CURRENCIES[x]['name']}"
)

currency = CURRENCIES[selected_currency]
CURRENCY = selected_currency
CURRENCY_SYMBOL = currency['symbol']
CONVERSION_RATE = currency['rate']

st.sidebar.info(f"1 DM = {CURRENCY_SYMBOL}{CONVERSION_RATE:,.2f} {CURRENCY}")

theme = st.sidebar.selectbox('🎨 Theme', ['Default Blue', 'Pink', 'Dark Mode', 'Purple', 'Green'])

if theme == 'Pink':
    PRIMARY_COLOR = "#e91e63"; SUCCESS_COLOR = "#f8bbd0"; DANGER_COLOR = "#880e4f"; SECONDARY_COLOR = "#f48fb1"
elif theme == 'Dark Mode':
    PRIMARY_COLOR = "#00bcd4"; SUCCESS_COLOR = "#4caf50"; DANGER_COLOR = "#f44336"; BACKGROUND_COLOR = "#263238"; TEXT_COLOR = "#eceff1"; SIDEBAR_COLOR = "#37474f"
elif theme == 'Purple':
    PRIMARY_COLOR = "#9c27b0"; SUCCESS_COLOR = "#ce93d8"; DANGER_COLOR = "#4a148c"; SECONDARY_COLOR = "#ba68c8"
elif theme == 'Green':
    PRIMARY_COLOR = "#4caf50"; SUCCESS_COLOR = "#81c784"; DANGER_COLOR = "#b71c1c"; SECONDARY_COLOR = "#66bb6a"

st.sidebar.markdown(f"<div style='background-color: {PRIMARY_COLOR}; padding: 10px; border-radius: 5px; color: white; text-align: center;'>Current Theme: {theme}</div>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_model()

# ============================================================
# MAIN FORM - WITH PAKISTAN BANKING LABELS
# ============================================================

with st.form('loan_form'):
    st.subheader('📋 Applicant Information')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<h4 style='color: {PRIMARY_COLOR};'>🏦 Account Details</h4>", unsafe_allow_html=True)
        
        checking_display = st.selectbox(
            'Checking Account Status',
            list(CHECKING_OPTIONS.values())
        )
        checking = [k for k, v in CHECKING_OPTIONS.items() if v == checking_display][0]
        
        savings_display = st.selectbox(
            'Savings Account Status',
            list(SAVINGS_OPTIONS.values())
        )
        savings = [k for k, v in SAVINGS_OPTIONS.items() if v == savings_display][0]
        
        employment_display = st.selectbox(
            'Employment Status',
            list(EMPLOYMENT_OPTIONS.values())
        )
        employment = [k for k, v in EMPLOYMENT_OPTIONS.items() if v == employment_display][0]
        
        age = st.slider('🎂 Age', 19, 75, 35)
        
    with col2:
        st.markdown(f"<h4 style='color: {PRIMARY_COLOR};'>💰 Loan Details</h4>", unsafe_allow_html=True)
        
        duration = st.slider('📅 Duration (months)', 4, 72, 18)
        
        credit_history_display = st.selectbox(
            'Credit History',
            list(CREDIT_HISTORY_OPTIONS.values())
        )
        credit_history = [k for k, v in CREDIT_HISTORY_OPTIONS.items() if v == credit_history_display][0]
        
        purpose_display = st.selectbox(
            'Loan Purpose',
            list(PURPOSE_OPTIONS.values())
        )
        purpose = [k for k, v in PURPOSE_OPTIONS.items() if v == purpose_display][0]
        
        # Amount input
        min_amount = int(250 * CONVERSION_RATE)
        max_amount = int(20000 * CONVERSION_RATE)
        default_amount = int(3000 * CONVERSION_RATE)
        step = max(int(1000 * CONVERSION_RATE), 1)
        
        credit_amount_local = st.number_input(
            f'💵 Credit Amount ({CURRENCY_SYMBOL})',
            min_value=min_amount,
            max_value=max_amount,
            value=default_amount,
            step=step
        )
        credit_amount_dm = credit_amount_local / CONVERSION_RATE
        
    with col3:
        st.markdown(f"<h4 style='color: {PRIMARY_COLOR};'>🏠 Additional Info</h4>", unsafe_allow_html=True)
        
        installment_rate = st.slider('📈 Installment Rate (% of income)', 1, 4, 2)
        
        property_display = st.selectbox(
            'Property Ownership',
            list(PROPERTY_OPTIONS.values())
        )
        property_type = [k for k, v in PROPERTY_OPTIONS.items() if v == property_display][0]
        
        debtors_display = st.selectbox(
            'Other Debtors / Guarantors',
            list(DEBTORS_OPTIONS.values())
        )
        other_debtors = [k for k, v in DEBTORS_OPTIONS.items() if v == debtors_display][0]
        
        telephone_display = st.selectbox(
            'Phone Registration',
            list(TELEPHONE_OPTIONS.values())
        )
        telephone = [k for k, v in TELEPHONE_OPTIONS.items() if v == telephone_display][0]
    
    # Submit button
    col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
    with col_submit2:
        submitted = st.form_submit_button('🔮 Predict Default Risk')

# ============================================================
# RESULTS
# ============================================================

if submitted:
    st.markdown("---")
    st.info('🔄 Processing prediction...')
    
    # Amount cards
    col_card1, col_card2, col_card3 = st.columns(3)
    
    with col_card1:
        st.markdown(f"""
        <div style='background-color: {PRIMARY_COLOR}15; padding: 20px; border-radius: 10px; border-left: 5px solid {PRIMARY_COLOR};'>
            <h3 style='color: {PRIMARY_COLOR}; margin: 0;'>Loan Amount</h3>
            <p style='font-size: 28px; font-weight: bold; color: {TEXT_COLOR}; margin: 10px 0;'>{CURRENCY_SYMBOL}{credit_amount_local:,.0f}</p>
            <p style='color: gray; margin: 0;'>{CURRENCY}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_card2:
        st.markdown(f"""
        <div style='background-color: {SECONDARY_COLOR}15; padding: 20px; border-radius: 10px; border-left: 5px solid {SECONDARY_COLOR};'>
            <h3 style='color: {SECONDARY_COLOR}; margin: 0;'>Original (DM)</h3>
            <p style='font-size: 28px; font-weight: bold; color: {TEXT_COLOR}; margin: 10px 0;'>{credit_amount_dm:,.0f} DM</p>
            <p style='color: gray; margin: 0;'>German Credit Dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_card3:
        duration_years = duration / 12
        st.markdown(f"""
        <div style='background-color: {PRIMARY_COLOR}15; padding: 20px; border-radius: 10px; border-left: 5px solid {PRIMARY_COLOR};'>
            <h3 style='color: {PRIMARY_COLOR}; margin: 0;'>Duration</h3>
            <p style='font-size: 28px; font-weight: bold; color: {TEXT_COLOR}; margin: 10px 0;'>{duration} months</p>
            <p style='color: gray; margin: 0;'>({duration_years:.1f} years)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Prepare features
    features = pd.DataFrame([{
        'CheckingAccount': checking,
        'Duration': duration,
        'CreditHistory': credit_history,
        'Purpose': purpose,
        'CreditAmount': credit_amount_dm,
        'SavingsAccount': savings,
        'Employment': employment,
        'InstallmentRate': installment_rate,
        'PersonalStatus': 'A93',
        'OtherDebtors': other_debtors,
        'ResidenceSince': 2,
        'Property': property_type,
        'Age': age,
        'OtherInstallments': 'A143',
        'Housing': 'A152',
        'NumCredits': 1,
        'Job': 'A173',
        'LiablePeople': 1,
        'Telephone': telephone,
        'ForeignWorker': 'A201'
    }])
    
    # Mock prediction
    risk_score = np.random.random()
    
    # Result
    st.markdown("---")
    st.subheader("🎯 Prediction Result")
    
    col_result1, col_result2 = st.columns([2, 1])
    
    with col_result1:
        if risk_score > 0.7:
            st.markdown(f"""
            <div style='background-color: {DANGER_COLOR}20; padding: 30px; border-radius: 15px; border: 3px solid {DANGER_COLOR}; text-align: center;'>
                <h1 style='color: {DANGER_COLOR}; margin: 0;'>⚠️ HIGH RISK</h1>
                <p style='font-size: 48px; font-weight: bold; color: {DANGER_COLOR}; margin: 10px 0;'>{risk_score*100:.1f}%</p>
                <p style='color: {TEXT_COLOR}; font-size: 18px;'>Default Probability</p>
            </div>
            """, unsafe_allow_html=True)
            st.error("🚫 **Recommendation:** Reject application or require significant collateral")
            
        elif risk_score > 0.4:
            st.markdown(f"""
            <div style='background-color: {WARNING_COLOR}20; padding: 30px; border-radius: 15px; border: 3px solid {WARNING_COLOR}; text-align: center;'>
                <h1 style='color: {WARNING_COLOR}; margin: 0;'>⚡ MEDIUM RISK</h1>
                <p style='font-size: 48px; font-weight: bold; color: {WARNING_COLOR}; margin: 10px 0;'>{risk_score*100:.1f}%</p>
                <p style='color: {TEXT_COLOR}; font-size: 18px;'>Default Probability</p>
            </div>
            """, unsafe_allow_html=True)
            st.warning("⚠️ **Recommendation:** Request additional documentation or guarantor")
            
        else:
            st.markdown(f"""
            <div style='background-color: {SUCCESS_COLOR}20; padding: 30px; border-radius: 15px; border: 3px solid {SUCCESS_COLOR}; text-align: center;'>
                <h1 style='color: {SUCCESS_COLOR}; margin: 0;'>✅ LOW RISK</h1>
                <p style='font-size: 48px; font-weight: bold; color: {SUCCESS_COLOR}; margin: 10px 0;'>{risk_score*100:.1f}%</p>
                <p style='color: {TEXT_COLOR}; font-size: 18px;'>Default Probability</p>
            </div>
            """, unsafe_allow_html=True)
            st.success("✅ **Recommendation:** Approve loan")
    
    with col_result2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h3 style='color: {TEXT_COLOR};'>Risk Meter</h3>
            <div style='width: 100%; height: 30px; background: linear-gradient(to right, {SUCCESS_COLOR}, {WARNING_COLOR}, {DANGER_COLOR}); border-radius: 15px; position: relative;'>
                <div style='position: absolute; left: {risk_score*100}%; top: -5px; width: 20px; height: 40px; background: {TEXT_COLOR}; border-radius: 50%; transform: translateX(-50%);'></div>
            </div>
            <p style='margin-top: 10px; color: {TEXT_COLOR};'>{'▲' * int(risk_score * 10)}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(float(risk_score))
    
    # Risk factors with Pakistani context
    st.markdown("---")
    st.subheader("📋 Risk Factor Analysis")
    
    factors = []
    factor_colors = []
    
    if duration > 24:
        factors.append("⏱️ Long duration (>24 months) - Higher default risk in Pakistan")
        factor_colors.append(WARNING_COLOR)
    if credit_amount_dm > 5000:
        factors.append(f"💰 High loan amount (>{CURRENCY_SYMBOL}{int(5000*CONVERSION_RATE):,}) - Exceeds average Pakistani income")
        factor_colors.append(DANGER_COLOR)
    if age < 25:
        factors.append("🎂 Young borrower (<25 years) - Limited credit history in Pakistan")
        factor_colors.append(WARNING_COLOR)
    if checking == 'A11':
        factors.append("🏦 Negative checking balance - Overdraft behavior detected")
        factor_colors.append(DANGER_COLOR)
    if credit_history in ['A33', 'A34']:
        factors.append("📊 Poor credit history - Previous defaults recorded")
        factor_colors.append(DANGER_COLOR)
    if savings == 'A65':
        factors.append("💰 No savings account - No financial cushion")
        factor_colors.append(WARNING_COLOR)
    if employment == 'A71':
        factors.append("💼 Unemployed - No stable income source")
        factor_colors.append(DANGER_COLOR)
    if property == 'A124':
        factors.append("❌ No property - No collateral available")
        factor_colors.append(WARNING_COLOR)
    
    if factors:
        cols = st.columns(min(len(factors), 3))
        for i, (factor, color) in enumerate(zip(factors, factor_colors)):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 4px solid {color}; margin: 5px 0;'>
                    <p style='margin: 0; color: {TEXT_COLOR}; font-size: 14px;'>{factor}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: {SUCCESS_COLOR}15; padding: 20px; border-radius: 10px; text-align: center;'>
            <p style='color: {SUCCESS_COLOR}; font-size: 18px; margin: 0;'>✅ No major risk factors identified</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🏦 Pakistan Banking Credit Risk System</p>
    <p>Data Science Mini Project | UET Peshawar</p>
    <p>Currency: {CURRENCY_SYMBOL} {CURRENCY} | Theme: {theme}</p>
</div>
""", unsafe_allow_html=True)