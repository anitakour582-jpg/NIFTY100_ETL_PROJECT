"""
NIFTY 100 Analytics Dashboard

Sprint 4 - Day 22
Streamlit Application Entry Point
"""

import streamlit as st


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------------
# Main Dashboard
# -----------------------------------

def main():

    st.title("📊 Nifty 100 Analytics Dashboard")

    st.sidebar.title("Navigation")

    st.sidebar.success(
        "Dashboard loaded successfully"
    )

    st.markdown(
        """
        ## Welcome to Nifty 100 Analytics

        This dashboard provides:

        - Company analysis
        - Financial screener
        - Peer comparison
        - Sector analysis
        - Capital allocation insights
        - Valuation analytics

        Use the sidebar to navigate between screens.
        """
    )


if __name__ == "__main__":
    main()