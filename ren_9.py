import streamlit as st
import pandas as pd
import time

# --- 1. Configuration ---
st.set_page_config(
    page_title="Renaissance Unified Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to mimic the sleek UI from your reference
st.markdown("""
<style>
    .bank-badge {
        background-color: #FFF0E6;
        color: #FF4B00;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    .payment-card {
        border: 1px solid #E6E6E6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Data (6 Items for Full Grid) ---
ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Price": 550, "AR": True, "Cat": "Abstract", "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset"},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Price": 12000, "AR": True, "Cat": "Modern", "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture"},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Price": 150, "AR": False, "Cat": "Landscape", "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting"},
    {"ID": 4, "Title": "Neon Dreams", "Artist": "Sarah Chen", "Price": 850, "AR": True, "Cat": "Cyberpunk", "Img": "https://placehold.co/600x400/FF00FF/FFFFFF?text=Neon"},
    {"ID": 5, "Title": "Marble Echo", "Artist": "David Stone", "Price": 4200, "AR": False, "Cat": "Modern", "Img": "https://placehold.co/600x400/708090/FFFFFF?text=Marble"},
    {"ID": 6, "Title": "Fragmented Soul", "Artist": "Elena Rossi", "Price": 3100, "AR": True, "Cat": "Abstract", "Img": "https://placehold.co/600x400/4B0082/FFFFFF?text=Abstract"}
]

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- 3. Page 1: Art Discovery Portal ---
def page_art_discovery():
    st.title("🎨 Art Discovery Portal")
    
    # Filter Bar
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        search = c1.text_input("🔍 Search Artist or Title", placeholder="Start typing...")
        price_range = c2.slider("Price Range (ZAR)", 0, 15000, (0, 15000))
        cat = c3.selectbox("Category", ["All"] + list(set(i['Cat'] for i in ART_DATA)))

    filtered = [
        i for i in ART_DATA if (search.lower() in i['Title'].lower() or search.lower() in i['Artist'].lower())
        and (price_range[0] <= i['Price'] <= price_range[1])
        and (cat == "All" or i['Cat'] == cat)
    ]

    st.divider()
    
    # Clean 2x3 Grid
    cols = st.columns(3)
    for idx, item in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(item['Img'], use_column_width=True)
                st.subheader(item['Title'])
                st.write(f"**{item['Artist']}** | :green[ZAR {item['Price']:,}]")
                if st.button("Add to Cart", key=f"add_{item['ID']}", use_container_width=True):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['Title']}!", icon="🛒")

# --- 4. Page 2: Cart & Checkout (THE PICTURE REPLICA) ---
def page_cart_checkout():
    if not st.session_state.cart:
        st.title("💳 Checkout")
        st.info("Your cart is empty.")
        return

    # Total Calculation
    total_val = sum(item['Price'] for item in st.session_state.cart)

    # UI starts here - Centered "Mobile" look
    _, center_col, _ = st.columns([1, 1.5, 1])
    
    with center_col:
        st.markdown("### ← Add money")
        st.caption("Amount (ZAR)")
        st.markdown(f"# {total_val:,.2f}")
        
        # Preset buttons like in the image
        st.write("` 100 ` ` 200 ` ` 500 ` ` Own amount `")
        
        st.divider()

        # "Pay by bank" section (Recommended)
        st.markdown(f"⚡ **Pay by bank** <span class='bank-badge'>Recommended</span>", unsafe_allow_html=True)
        st.write("Make a **fast, secure** payment from your bank account. Pay in one click every time.")
        
        # Simulated Bank Icons
        st.markdown("🟥 🟦 🟩 🟨 🟧")
        st.caption("Add bank references so users know upfront whether this is a payment method they can use.")
        
        st.divider()

        # Other Options
        st.markdown("💳 **Card** `VISA` `Mastercard` ")
        st.divider()
        st.markdown("🏦 **Capitec Pay**")
        st.divider()
        st.markdown("🏛️ **Manual EFT**")
        st.write("")
        
        if st.button("Continue", type="primary", use_container_width=True):
            with st.status("Processing Pay by Bank...", expanded=True) as status:
                st.write("Connecting to South African banking gateway...")
                time.sleep(1.5)
                status.update(label="Transaction Complete!", state="complete", expanded=False)
            st.balloons()
            st.session_state.cart = []
            st.success("Art secured! Check your profile for certificates.")

# --- Main App Logic ---
def main():
    st.sidebar.title("⚜️ Renaissance")
    pg = st.sidebar.radio("Navigate", ["Art Discovery Portal", "Cart & Checkout"])
    st.sidebar.divider()
    st.sidebar.metric("Cart", f"{len(st.session_state.cart)} Items")

    if pg == "Art Discovery Portal": page_art_discovery()
    elif pg == "Cart & Checkout": page_cart_checkout()

if __name__ == "__main__":
    main()
