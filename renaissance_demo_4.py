import streamlit as st
import pandas as pd
import time

# --- Configuration ---
st.set_page_config(
    page_title="Renaissance Enterprise Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- State Management (The "Engine" of the Demo) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'payout_sim_val' not in st.session_state:
    st.session_state.payout_sim_val = 2500.0

# --- Shared Data ---
ARTIST_TIERS = {
    "Emerging": {"color": "#94a3b8", "fee": 20, "desc": "Basic storefront, 20% platform fee."},
    "Semi-Pro": {"color": "#3b82f6", "fee": 10, "desc": "AR/3D enabled, 10% platform fee."},
    "Studio/Gallery": {"color": "#eab308", "fee": 5, "desc": "VR Tours, multiple seats, 5% platform fee."}
}

ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Price": 550, "Tier": "Semi-Pro", "AR": True,
     "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset"},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Price": 12000, "Tier": "Studio/Gallery",
     "AR": True, "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture"},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Price": 150, "Tier": "Emerging", "AR": False,
     "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting"}
]


# --- UI Helper Components ---
def add_to_cart(item):
    st.session_state.cart.append(item)
    st.toast(f"Added {item['Title']} to your collection!", icon="🛒")


# --- Page 1: The Discovery Portal (Version 2 Style UI + Version 1 Logic) ---
def page_discovery():
    st.title("🎨 Art Discovery Portal")
    st.markdown("### High-Engagement Content Feed")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search artists or styles...", placeholder="Search...")

    st.divider()

    # Display Art Cards
    cols = st.columns(3)
    for i, item in enumerate(ART_DATA):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(item['Img'], use_column_width=True)
                st.subheader(item['Title'])

                # Metadata Row
                c1, c2 = st.columns(2)
                c1.markdown(f"**Artist:** {item['Artist']}")
                c2.markdown(f"**Price:** :green[${item['Price']:,}]")

                # Feature Tags
                tier_color = ARTIST_TIERS[item['Tier']]['color']
                st.markdown(
                    f"<span style='background:{tier_color}33; color:{tier_color}; padding:2px 8px; border-radius:10px; font-size:0.8em;'>{item['Tier']}</span>",
                    unsafe_allow_html=True)

                if item['AR']:
                    st.markdown(
                        "<span style='background:#10b981; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em;'>📱 AR READY</span>",
                        unsafe_allow_html=True)

                st.write(" ")  # Spacer

                # THE BUY BUTTON (Functional)
                if st.button(f"Purchase {item['Title']}", key=f"buy_{item['ID']}", use_container_width=True,
                             type="primary"):
                    add_to_cart(item)


# --- Page 2: Management & Payouts (The Business Logic) ---
def page_management():
    st.title("📊 Artist Dashboard & Business Logic")

    tab1, tab2 = st.tabs(["Sales Simulator", "Inventory Management"])

    with tab1:
        st.subheader("Platform Revenue Calculator")
        st.info("Demonstrating the automated fee split based on Artist Tier.")

        col_a, col_b = st.columns(2)
        with col_a:
            val = st.number_input("Mock Sale Price ($)", value=st.session_state.payout_sim_val)
            tier = st.selectbox("Select Artist Tier", list(ARTIST_TIERS.keys()))

        fee_pct = ARTIST_TIERS[tier]['fee']
        platform_cut = val * (fee_pct / 100)
        artist_payout = val - platform_cut

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Gross Sale", f"${val:,.2f}")
        m2.metric("Platform Fee", f"${platform_cut:,.2f}", f"-{fee_pct}%")
        m3.metric("Artist Net", f"${artist_payout:,.2f}", delta_color="normal")

        # Architecture Visual Mention
        st.markdown(
            "> **Technical Note:** This calculation is handled by the *Transaction Microservice* (SOA Architecture) ensuring high precision and audit trails.")

    with tab2:
        st.subheader("Current Listings")
        st.dataframe(pd.DataFrame(ART_DATA), use_container_width=True)
        st.button("➕ Upload New 3D/AR Asset")


# --- Page 3: Checkout & User (The E-commerce Finish) ---
def page_checkout():
    st.title("💳 Checkout & Account")

    if not st.session_state.cart:
        st.warning("Your cart is empty. Go to the Discovery Portal to add art!")
    else:
        st.subheader("Your Selection")
        total = 0
        for item in st.session_state.cart:
            with st.expander(f"{item['Title']} - ${item['Price']}", expanded=True):
                st.write(f"Artist: {item['Artist']} | Format: {item['Tier']} Tier Digital/Physical")
                if st.button("Remove", key=f"rem_{item['ID']}"):
                    st.session_state.cart.remove(item)
                    st.rerun()
            total += item['Price']

        st.divider()
        st.markdown(f"## Total: :green[${total:,}]")
        if st.button("Complete Secure Transaction", use_container_width=True, type="primary"):
            with st.spinner("Processing via Secure Gateway..."):
                time.sleep(2)
                st.success("Transaction Successful! Assets available in your VR Gallery.")
                st.balloons()
                st.session_state.cart = []


# --- Main Navigation ---
def main():
    st.sidebar.title("⚜️ Renaissance")
    st.sidebar.markdown("*Enterprise E-commerce Demo*")

    nav = st.sidebar.radio("Navigation", ["Discovery Portal", "Dashboard & Logic", "Cart & Checkout"])

    st.sidebar.divider()
    st.sidebar.subheader("Cart Status")
    st.sidebar.metric("Items", len(st.session_state.cart))

    if nav == "Discovery Portal":
        page_discovery()
    elif nav == "Dashboard & Logic":
        page_management()
    else:
        page_checkout()


if __name__ == "__main__":
    main()