import streamlit as st
import pandas as pd
import time

# --- 1. Configuration & Data ---
st.set_page_config(
    page_title="Renaissance Unified Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Expanded Data Set (Now 6 items for a clean 2-row grid)
ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Medium": "Digital Arts", "Price": 550, "AR_Ready": True, "Category": "Abstract", "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset"},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Medium": "Sculptor", "Price": 12000, "AR_Ready": True, "Category": "Modern", "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture"},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Medium": "Painter", "Price": 150, "AR_Ready": False, "Category": "Landscape", "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting"},
    {"ID": 4, "Title": "Neon Dreams", "Artist": "Sarah Chen", "Medium": "Digital Arts", "Price": 850, "AR_Ready": True, "Category": "Cyberpunk", "Img": "https://placehold.co/600x400/FF00FF/FFFFFF?text=Neon"},
    {"ID": 5, "Title": "Marble Echo", "Artist": "David Stone", "Medium": "Sculptor", "Price": 4200, "AR_Ready": False, "Category": "Modern", "Img": "https://placehold.co/600x400/708090/FFFFFF?text=Marble"},
    {"ID": 6, "Title": "Fragmented Soul", "Artist": "Elena Rossi", "Medium": "Painter", "Price": 3100, "AR_Ready": True, "Category": "Abstract", "Img": "https://placehold.co/600x400/4B0082/FFFFFF?text=Abstract"}
]

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- 2. Refined Page 1: Art Discovery Portal ---
def page_art_discovery():
    st.title("🎨 Art Discovery Portal")
    
    # Filtering Logic
    with st.container(border=True):
        f1, f2, f3 = st.columns([2, 2, 1])
        search_query = f1.text_input("🔍 Search Artist or Title", placeholder="Start typing...", help="Search updates as you type")
        price_val = f2.select_slider("Price Range ($)", options=sorted(list(set([i['Price'] for i in ART_DATA] + [0, 15000]))), value=(0, 15000))
        cat_filter = f3.selectbox("Filter Category", ["All"] + list(set(i['Category'] for i in ART_DATA)))

    # Grid Display
    filtered = [
        i for i in ART_DATA if (search_query.lower() in i['Title'].lower() or search_query.lower() in i['Artist'].lower())
        and (price_val[0] <= i['Price'] <= price_val[1])
        and (cat_filter == "All" or i['Category'] == cat_filter)
    ]

    st.divider()
    
    # Clean 3-column grid (2 rows for 6 items)
    cols = st.columns(3)
    for idx, item in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(item['Img'], use_column_width=True)
                st.subheader(item['Title'])
                st.write(f"**{item['Artist']}** | :green[${item['Price']:,}]")
                
                if item['AR_Ready']:
                    st.caption("📱 AR Enabled")
                
                if st.button("Add to Cart", key=f"btn_{item['ID']}", use_container_width=True, type="secondary"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['Title']}!", icon="🛒")

# --- 3. Refined Page 2: Cart & Checkout (Based on Reference Image) ---
def page_cart_checkout():
    st.title("💳 Secure Payment")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Return to the portal to add art.")
        return

    # Layout: Cart items on the left, Payment UI on the right
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.subheader("Order Summary")
        total_amt = sum(item['Price'] for item in st.session_state.cart)
        for idx, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2 = st.columns([1, 3])
                c1.image(item['Img'], width=60)
                c2.write(f"**{item['Title']}**\n\n${item['Price']:,}")
                if st.button("Remove", key=f"rem_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        st.divider()
        st.metric("Total Amount", f"ZAR {total_amt:,}")

    with col_right:
        # Replicating the Design from the Image
        st.markdown("### Add money")
        st.caption("Amount (ZAR)")
        st.markdown(f"## {total_amt:,.2f}")
        
        st.divider()
        
        # Payment Method Simulation
        st.markdown("##### Select Payment Method")
        
        # Pay by Bank Section (Recommended)
        with st.container(border=True):
            pay_bank = st.radio(
                "Payment Options",
                ["Pay by bank", "Card (Visa/Mastercard)", "Capitec Pay", "Manual EFT"],
                label_visibility="collapsed"
            )
            
            if "Pay by bank" in pay_bank:
                st.markdown("**Pay by bank** :orange-background[Recommended]")
                st.write("Make a **fast, secure** payment from your bank account. Pay in one click every time.")
                # Simulated Bank Logos
                st.markdown("🏦 `Absa` `FNB` `Nedbank` `Standard Bank` `Tyme` `Capitec` ")
                st.caption("Available for all major South African banks.")
        
        st.write("")
        if st.button("Continue to Secure Pay", type="primary", use_container_width=True):
            with st.status("Initializing Secure Bank Link...", expanded=True) as status:
                st.write("Connecting to your bank API...")
                time.sleep(1.5)
                st.write("Verifying transaction credentials...")
                time.sleep(1)
                status.update(label="Transaction Successful!", state="complete", expanded=False)
            st.balloons()
            st.session_state.cart = []
            st.success("Payment received! Your digital certificates are ready.")

# --- Navigation ---
def main():
    st.sidebar.title("⚜️ Renaissance")
    pg = st.sidebar.radio("Navigate", ["Art Discovery Portal", "Cart & Checkout"])
    st.sidebar.divider()
    st.sidebar.metric("Cart Count", len(st.session_state.cart))

    if pg == "Art Discovery Portal": page_art_discovery()
    elif pg == "Cart & Checkout": page_cart_checkout()

if __name__ == "__main__":
    main()
