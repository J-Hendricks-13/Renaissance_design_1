import streamlit as st
import pandas as pd
import time

# --- 1. Configuration ---
st.set_page_config(
    page_title="Renaissance Pro Demo",
    layout="wide", # Ensures full-screen utilization
    initial_sidebar_state="expanded"
)

# Custom CSS for high-end interactivity
st.markdown("""
<style>
    /* Full-width container styling */
    .main-payment-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Interactive Hover Effect for Payment Methods */
    .payment-option-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #eee;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 15px;
    }
    .payment-option-card:hover {
        border-color: #FF4B00;
        background-color: #fff9f6;
        transform: translateY(-2px);
    }

    /* Reference Image Badge Styling */
    .bank-badge {
        background-color: #FF4B00;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Bank Color Row from your reference */
    .bank-dot {
        height: 15px;
        width: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Data Persistence ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Mock Art Data (Expanded to 6 for the grid)
ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Price": 550, "Img": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset"},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Price": 12000, "Img": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture"},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Price": 150, "Img": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting"},
    {"ID": 4, "Title": "Neon Dreams", "Artist": "Sarah Chen", "Price": 850, "Img": "https://placehold.co/600x400/FF00FF/FFFFFF?text=Neon"},
    {"ID": 5, "Title": "Marble Echo", "Artist": "David Stone", "Price": 4200, "Img": "https://placehold.co/600x400/708090/FFFFFF?text=Marble"},
    {"ID": 6, "Title": "Fragmented Soul", "Artist": "Elena Rossi", "Price": 3100, "Img": "https://placehold.co/600x400/4B0082/FFFFFF?text=Abstract"}
]

# --- 3. Page: Art Discovery ---
def page_art_discovery():
    st.title("🎨 Art Discovery Portal")
    
    # Wide Search Bar
    search = st.text_input("🔍 Search unique collections...", placeholder="Search Artist, Title, or Medium")
    
    st.divider()
    
    # 3-Column Responsive Grid
    cols = st.columns(3)
    for idx, item in enumerate(ART_DATA):
        if search.lower() in item['Title'].lower() or search.lower() in item['Artist'].lower():
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(item['Img'], use_column_width=True)
                    st.subheader(item['Title'])
                    st.write(f"By {item['Artist']} — **ZAR {item['Price']:,}**")
                    if st.button("Add to Collection", key=f"add_{item['ID']}", use_container_width=True):
                        st.session_state.cart.append(item)
                        st.toast(f"{item['Title']} added!", icon="✅")

# --- 4. Page: Cart & Checkout (Interactive & Expanded) ---
def page_cart_checkout():
    if not st.session_state.cart:
        st.info("Your cart is empty. Start your collection in the portal!")
        return

    total_val = sum(item['Price'] for item in st.session_state.cart)

    # Layout: Horizontal Expansion
    st.markdown("### 💳 Checkout Strategy")
    
    main_col1, main_col2 = st.columns([1, 2], gap="large")

    with main_col1:
        st.subheader("Your Selection")
        for idx, item in enumerate(st.session_state.cart):
            with st.expander(f"{item['Title']} - ZAR {item['Price']:,}", expanded=False):
                st.image(item['Img'])
                if st.button("Remove Item", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        st.divider()
        st.metric("Total Payable", f"ZAR {total_val:,.2f}")

    with main_col2:
        # Mimicking the Reference Image UI logic with interactivity
        st.markdown("""
            <div style='text-align: left; margin-bottom: 20px;'>
                <span style='color: #666;'>← Add money</span><br>
                <span style='font-size: 14px; color: #888;'>Amount (ZAR)</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='margin-top: -20px;'>{total_val:,.2f}</h1>", unsafe_allow_html=True)
        
        # Interactive Tabs to replace the "Wasted Space" subsections
        tab_bank, tab_card, tab_others = st.tabs(["⚡ Pay by Bank", "💳 Card Payment", "🏛️ Alternative Methods"])

        with tab_bank:
            st.markdown(f"""
                <div class="payment-option-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; font-size: 18px;">Pay by bank</span>
                        <span class="bank-badge">Recommended</span>
                    </div>
                    <p style="color: #444; margin-top: 10px;">Make a <b>fast, secure</b> payment from your bank account. Pay in one click every time.</p>
                    <div style="margin: 15px 0;">
                        <span class="bank-dot" style="background-color: #E21E26;"></span>
                        <span class="bank-dot" style="background-color: #0069B3;"></span>
                        <span class="bank-dot" style="background-color: #009639;"></span>
                        <span class="bank-dot" style="background-color: #FFCD00;"></span>
                        <span class="bank-dot" style="background-color: #000000;"></span>
                    </div>
                    <p style="font-size: 12px; color: #888;">Add bank references so users know upfront whether this is a payment method they can use.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Confirm & Pay via Bank", type="primary", use_container_width=True):
                with st.status("Linking to Secure Banking Gateway...", expanded=True) as s:
                    time.sleep(1)
                    s.update(label="Payment Verified!", state="complete")
                st.balloons()
                st.session_state.cart = []
                st.rerun()

        with tab_card:
            st.write("Securely pay using your Visa or Mastercard.")
            c_col1, c_col2 = st.columns(2)
            c_col1.text_input("Card Number", placeholder="0000 0000 0000 0000")
            c_col2.text_input("CVV", placeholder="123")
            st.button("Pay with Card", use_container_width=True)

        with tab_others:
            st.markdown("### Capitec Pay")
            st.write("Instant approval via your Capitec App.")
            st.button("Link Capitec Account", use_container_width=True)
            st.divider()
            st.markdown("### Manual EFT")
            st.info("Banking details will be emailed to you. Artwork released upon clearance.")

# --- Navigation ---
def main():
    pg = st.sidebar.radio("Navigation", ["Art Discovery Portal", "Cart & Checkout"])
    st.sidebar.divider()
    st.sidebar.metric("Cart Count", len(st.session_state.cart))
    
    if pg == "Art Discovery Portal": page_art_discovery()
    else: page_cart_checkout()

if __name__ == "__main__":
    main()
