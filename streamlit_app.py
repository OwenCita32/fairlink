import streamlit as st
from snowflake.snowpark.context import get_active_session

# Judul
st.title("FairLink: AI Financial Inclusion Dashboard")
st.caption("Privacy-safe collaboration between Bank & Telco")

# Ambil session Snowflake aktif
session = get_active_session()

# Ambil data dari Secure View (Clean Room)
df = session.table(
    "ANALYTICS_ZONE.CREDIT_INCLUSION_INSIGHT"
).to_pandas()

# Validasi data
if df.empty:
    st.error("No data found in analytics zone.")
else:
    st.subheader("Inclusion Score Distribution")
    st.bar_chart(
        df.set_index("HASHED_EMAIL")["INCLUSION_SCORE"]
    )

# AI Insight Section
st.subheader("AI-Assisted Risk Insight")

if st.button("Generate AI Summary"):
    result = session.sql("""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mixtral-8x7b',
            'You are assisting a credit analyst. Based on anonymized inclusion scores shown in a dashboard, provide a concise summary of overall credit inclusion health. Focus on stability, risk segmentation, and cautious micro-loan suitability. Avoid generic definitions.'
        )
    """).collect()

    st.info(result[0][0])
