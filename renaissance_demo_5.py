import streamlit as st
import pandas as pd
import time

# --- 1. Configuration & Data ---
st.set_page_config(
    page_title="Renaissance Unified Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared Business Logic: Artist Tiers
ARTIST_TIERS = {
    "Emerging": {"color": "#94a3b8", "fee": 20, "desc": "Free tier, limited uploads, basic profile."},
    "Semi-Pro": {"color": "#3b82f6", "fee": 10, "desc": "Subscription tier, AR/3D access."},
    "Studio/Gallery": {"color": "#eab308", "fee": 5, "desc": "Premium tier, VR support, lowest fees."}
}

# Unified Data Set
ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Medium": "Digital Arts", "Price": 550,
     "Tier": "Semi-Pro", "AR_Ready": True, "VR_Ready": False,
     "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset", "Desc": "Vibrant abstract for AR home viewing."},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Medium": "Sculptor", "Price": 12000,
     "Tier": "Studio/Gallery", "AR_Ready": True, "VR_Ready": True,
     "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture",
     "Desc": "Large-scale metal sculpture with studio VR tour."},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Medium": "Painter", "Price": 150, "Tier": "Emerging",
     "AR_Ready": False, "VR_Ready": False, "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting",
     "Desc": "Traditional oil on canvas."},
]

# Session State for Commerce (Version 4 Functionality)
if 'cart' not in st.session_state:
    st.session_state.cart = []


# --- 2. Page Definitions ---

def page_art_discovery():
    """Version 1 Portal + Version 4 Cart Integration"""
    st.title("🎨 Art Discovery Portal")
    st.markdown("### Browse & Purchase (Integrated Cart)")

    # Filtering Sidebar (v1)
    st.sidebar.subheader("Filter Gallery")
    search = st.sidebar.text_input("Search Title/Artist")
    ar_only = st.sidebar.checkbox("AR Enabled Only")

    # Display Gallery
    cols = st.columns(3)
    for i, item in enumerate(ART_DATA):
        if ar_only and not item['AR_Ready']: continue

        with cols[i % 3]:
            with st.container(border=True):
                st.image(item['Img'], use_column_width=True)
                st.subheader(item['Title'])
                st.write(f"**Artist:** {item['Artist']} | **Price:** :green[${item['Price']:,}]")

                # Details Dropdown Functionality (v1)
                with st.expander("🔍 View Technical Details"):
                    st.write(f"**Medium:** {item['Medium']}")
                    st.write(f"*Description:* {item['Desc']}")
                    if item['AR_Ready']: st.info("📱 This piece is AR Ready")

                # Purchase Button linked to Cart (v4)
                if st.button(f"Add to Cart", key=f"cart_{item['ID']}", use_container_width=True, type="primary"):
                    st.session_state.cart.append(item)
                    st.toast(f"{item['Title']} added to cart!")


def page_immersive_demo():
    """Version 1: Core Differentiator Page"""
    st.title("👓 Immersive Art Experience")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Augmented Reality (AR)")
        st.image("https://placehold.co/800x400/10b981/FFFFFF?text=Mobile+AR+Preview", use_column_width=True)
        st.caption("Simulated view of digital art placed on a physical wall via mobile camera.")
    with col2:
        st.subheader("Virtual Reality (VR)")
        st.image("https://placehold.co/800x400/0ea5e9/FFFFFF?text=VR+Gallery+Tour", use_column_width=True)
        st.caption("Full 360° VR immersion into an artist's personal studio.")


def page_profile_management():
    """Version 2: Clean Profile Management Aesthetic"""
    st.title("👤 My Collector Profile")
    col_pfp, col_stats = st.columns([1, 3])
    with col_pfp:
        st.markdown(
            '<div style="width: 150px; height: 150px; background-color: #ef4444; border-radius: 50%; margin: auto;"></div>',
            unsafe_allow_html=True)
    with col_stats:
        st.subheader("ArtLover25")
        st.write("Digital Art Collector & AR Enthusiast")
        c1, c2, c3 = st.columns(3)
        c1.metric("Following", 45)
        c2.metric("Followers", 120)
        c3.metric("Collection Value", "$14,500")
    st.divider()
    st.button("My Commission History", use_container_width=True)
    st.button("Account Settings", use_container_width=True)


def page_cart_checkout():
    """Version 4: Commerce Logic"""
    st.title("💳 Secure Checkout")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"**{item['Title']}** by {item['Artist']} — ${item['Price']}")
            total += item['Price']
        st.divider()
        st.subheader(f"Total: ${total:,}")
        if st.button("Finalize Purchase", type="primary"):
            with st.spinner("Processing..."):
                time.sleep(1.5)
                st.success("Transaction Complete! Certificates sent to your profile.")
                st.session_state.cart = []


def page_tech_overview():
    """Version 1: System Technical Overview"""
    st.title("⚙️ System Architecture")

# FIX: Wrap the placeholder in a markdown string so it doesn't break the code
    st.markdown("### System Design Concept")
    st.write("[Image of Service - Oriented Architecture Diagram]")

st.markdown("""
    ### Service-Oriented Architecture (SOA)
    * **User Service:** Auth, Profile & Tiers.
    * **Transaction Service:** Payout splits (Artist vs. Platform).
    * **Immersive Engine:** AR/VR asset delivery.
    * **Search Service:** Elasticsearch powered metadata search.
    """)
st.divider()
st.subheader("Non-Functional Targets")
st.table(pd.DataFrame({
    "Requirement": ["Availability", "Latency", "Security"],
    "Target": ["99.9% Uptime", "< 200ms API response", "AES-256 Encryption"]
}))


# --- 3. Main Navigation Logic ---
def main():
    st.sidebar.title("⚜️ Renaissance Final")

    # Navigation mapping
    page = st.sidebar.radio("Navigate Pages", [
        "Art Discovery Portal",
        "Cart & Checkout",
        "Immersive Demo",
        "My Profile",
        "Technical Overview"
    ])

    st.sidebar.divider()
    st.sidebar.metric("Cart Items", len(st.session_state.cart))

    if page == "Art Discovery Portal":
        page_art_discovery()
    elif page == "Cart & Checkout":
        page_cart_checkout()
    elif page == "Immersive Demo":
        page_immersive_demo()
    elif page == "My Profile":
        page_profile_management()
    elif page == "Technical Overview":
        page_tech_overview()


if __name__ == "__main__":
    main()