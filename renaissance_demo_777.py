import streamlit as st
import pandas as pd
import time

# --- 1. Configuration & Data ---
st.set_page_config(
    page_title="Renaissance Unified Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Data Set with Categories
ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Medium": "Digital Arts", "Price": 550,
     "Tier": "Semi-Pro", "AR_Ready": True, "VR_Ready": False, "Category": "Abstract",
     "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset", "Desc": "Vibrant abstract for AR home viewing."},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Medium": "Sculptor", "Price": 12000,
     "Tier": "Studio/Gallery", "AR_Ready": True, "VR_Ready": True, "Category": "Modern",
     "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture",
     "Desc": "Large-scale metal sculpture with studio VR tour."},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Medium": "Painter", "Price": 150, "Tier": "Emerging",
     "AR_Ready": False, "VR_Ready": False, "Category": "Landscape",
     "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting",
     "Desc": "Traditional oil on canvas."},
    {"ID": 4, "Title": "Neon Dreams", "Artist": "Sarah Chen", "Medium": "Digital Arts", "Price": 850, "Tier": "Semi-Pro",
     "AR_Ready": True, "VR_Ready": False, "Category": "Cyberpunk",
     "Img": "https://placehold.co/600x400/FF00FF/FFFFFF?text=Neon",
     "Desc": "Cyberpunk aesthetic for digital displays."}
]

# Session State Initialization
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- 2. Improved Page Definitions ---

def page_art_discovery():
    st.title("🎨 Art Discovery Portal")
    
    # --- Filter Bar ---
    with st.expander("🛠️ Advanced Search & Filters", expanded=True):
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            search = st.text_input("Search by Title, Artist, or Style", placeholder="e.g. 'Modern'")
        with f_col2:
            price_range = st.slider("Price Range ($)", 0, 15000, (0, 15000))
        with f_col3:
            category = st.selectbox("Category", ["All", "Abstract", "Modern", "Landscape", "Cyberpunk"])

    st.divider()

    # --- Gallery Logic ---
    # Filtering the data
    filtered_data = [
        item for item in ART_DATA 
        if (search.lower() in item['Title'].lower() or search.lower() in item['Artist'].lower())
        and (price_range[0] <= item['Price'] <= price_range[1])
        and (category == "All" or item['Category'] == category)
    ]

    if not filtered_data:
        st.warning("No artwork matches your current filters.")
    
    # Responsive Grid
    cols = st.columns(3)
    for i, item in enumerate(filtered_data):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(item['Img'], use_column_width=True)
                
                # Visual Badges
                badge_html = ""
                if item['AR_Ready']: badge_html += '<span style="background:#10b981; color:white; padding:2px 6px; border-radius:4px; font-size:10px; margin-right:5px;">AR READY</span>'
                if item['VR_Ready']: badge_html += '<span style="background:#3b82f6; color:white; padding:2px 6px; border-radius:4px; font-size:10px;">VR TOUR</span>'
                st.markdown(badge_html, unsafe_allow_html=True)
                
                st.subheader(item['Title'])
                st.write(f"**Artist:** {item['Artist']}")
                st.markdown(f"### :green[${item['Price']:,}]")

                # Expanded Details
                with st.expander("View Story & Specs"):
                    st.write(item['Desc'])
                    st.caption(f"Medium: {item['Medium']} | Tier: {item['Tier']}")

                # Cart Action
                if st.button(f"Add to Cart", key=f"add_{item['ID']}", use_container_width=True):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['Title']} to cart!", icon="🛒")

def page_cart_checkout():
    st.title("🛒 Your Gallery Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is currently empty. Explore the portal to find unique pieces!")
        return

    col_items, col_summary = st.columns([2, 1])

    with col_items:
        st.subheader("Items in Cart")
        # List items with a "Remove" option
        for idx, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 2, 1])
                c1.image(item['Img'], width=80)
                c2.markdown(f"**{item['Title']}**\n\n{item['Artist']}")
                c3.write(f"${item['Price']:,}")
                if c3.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()

    with col_summary:
        st.subheader("Order Summary")
        subtotal = sum(item['Price'] for item in st.session_state.cart)
        tax = subtotal * 0.08  # Mock 8% tax
        total = subtotal + tax
        
        st.write(f"Subtotal: ${subtotal:,.2f}")
        st.write(f"Estimated Tax (8%): ${tax:,.2f}")
        st.divider()
        st.markdown(f"## Total: :green[${total:,.2f}]")
        
        # Checkout Flow
        with st.expander("💳 Payment Details", expanded=True):
            method = st.radio("Payment Method", ["Credit Card", "Crypto (Ethereum)", "Renaissance Credits"])
            card_no = st.text_input("Card / Wallet Address", placeholder="0000 0000 0000 0000")
            
            if st.button("Complete Purchase", type="primary", use_container_width=True):
                if not card_no:
                    st.error("Please enter payment details.")
                else:
                    with st.status("Verifying Transaction...", expanded=True) as status:
                        st.write("Authenticating with blockchain...")
                        time.sleep(1)
                        st.write("Generating Digital Certificate of Authenticity...")
                        time.sleep(1)
                        status.update(label="Purchase Successful!", state="complete", expanded=False)
                    
                    st.balloons()
                    st.success(f"Success! {len(st.session_state.cart)} items are now in your collection.")
                    st.session_state.cart = []
                    time.sleep(2)
                    st.rerun()

# --- Placeholder Pages for Navigation Consistency ---
def page_immersive_demo(): st.title("👓 Immersive Demo")
def page_profile_management(): st.title("👤 My Profile")
def page_tech_overview(): st.title("⚙️ Tech Overview")

# --- 3. Main Navigation Logic ---
def main():
    st.sidebar.title("⚜️ Renaissance")
    
    # Persistent Cart Preview in Sidebar
    st.sidebar.metric("Items in Cart", len(st.session_state.cart))
    
    page = st.sidebar.radio("Navigate", [
        "Art Discovery Portal",
        "Cart & Checkout",
        "Immersive Demo",
        "My Profile",
        "Technical Overview"
    ])

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