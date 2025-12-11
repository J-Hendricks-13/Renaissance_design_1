import streamlit as st
import pandas as pd
import random

# --- Configuration and Data ---
st.set_page_config(
    page_title="Renaissance App Proposal Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Dummy Data: Artists and Art Pieces
# Tier mapping for access and features
ARTIST_TIERS = {
    "Emerging": {"color": "gray", "description": "Free tier, limited uploads, basic profile.", "fee_pct": 20},
    "Semi-Pro": {"color": "blue", "description": "Subscription tier, higher visibility, 3D/AR upload access.", "fee_pct": 10},
    "Studio/Gallery": {"color": "gold", "description": "Premium tier, multiple locations, VR support, commission management.", "fee_pct": 5}
}

# Art Data
ART_DATA = [
    {
        "ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Medium": "Digital Arts",
        "Price": 550, "Tier": "Semi-Pro", "AR_Ready": True, "VR_Ready": False,
        "Description": "A vibrant, abstract piece designed for AR viewing in a home setting."
    },
    {
        "ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Medium": "Sculptor",
        "Price": 12000, "Tier": "Studio/Gallery", "AR_Ready": True, "VR_Ready": True,
        "Description": "A large-scale metal sculpture. VR feature allows a tour of the physical studio where it was crafted."
    },
    {
        "ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Medium": "Painter",
        "Price": 150, "Tier": "Emerging", "AR_Ready": False, "VR_Ready": False,
        "Description": "A small, traditional oil on canvas. Limited digital presence."
    },
    {
        "ID": 4, "Title": "Metropolis Rhapsody", "Artist": "Art Collective 7", "Medium": "Graphic Designer",
        "Price": 3500, "Tier": "Studio/Gallery", "AR_Ready": True, "VR_Ready": True,
        "Description": "Architectural design concept, includes full 3D model for VR walkthrough."
    },
    {
        "ID": 5, "Title": "Winter's Poem", "Artist": "Poet Laureate", "Medium": "Literary Arts",
        "Price": 50, "Tier": "Semi-Pro", "AR_Ready": False, "VR_Ready": False,
        "Description": "First edition digital copy of a celebrated contemporary poem."
    }
]

df = pd.DataFrame(ART_DATA)

# --- NEW PAGE: Artist/Art Management ---
def page_artist_management():
    st.title("👨‍🎨 Artist & Art Management (FR-UM-02, FR-AM-01, FR-AM-02)")
    st.markdown("### Artist-Seller Profile and Storefront Setup")

    st.subheader("1. Profile & Tier Status")
    current_tier = st.selectbox("Current Membership Tier", list(ARTIST_TIERS.keys()), index=1)
    st.info(f"You currently have the **{current_tier}** tier. Benefits include: {ARTIST_TIERS[current_tier]['description']}")
    st.button("Upgrade My Tier", help="Gain lower fees and more immersive features.")
    st.markdown("---")

    st.subheader("2. Art Management: New Listing")
    with st.form("new_art_listing"):
        st.write("Create a new artwork listing.")
        title = st.text_input("Artwork Title", "My New Masterpiece")
        medium = st.selectbox("Medium (Type of Artist)", ["Painter", "Sculptor", "Digital Arts", "Literary Arts"])
        price_type = st.radio("Sale Type", ["Fixed Price", "Auction (FR-EC-02)"])
        
        col_price, col_immersive = st.columns(2)
        with col_price:
            price = st.number_input(f"{price_type} ($)", min_value=1.0, value=500.0)
        with col_immersive:
            is_ar = st.checkbox("AR Ready Upload (3D/Model)", True)
            is_vr = st.checkbox("VR Ready (Gallery Tour)", False)

        description = st.text_area("Description and Tags", "A piece using bold colors...")
        submitted = st.form_submit_button("Publish Artwork")

        if submitted:
            st.success(f"Artwork '{title}' submitted! Status: Draft. Checkboxes confirm AR:{is_ar}, VR:{is_vr}")

    st.markdown("---")
    st.subheader("3. Sales and Inventory Status")
    st.dataframe(df[['Title', 'Medium', 'Price', 'Tier']].head(3).style.highlight_max(axis=0), use_container_width=True)
    st.caption("Sales history and net payout details are handled by the Transaction Service (See Sales Split Simulator).")

# --- NEW PAGE: User/Buyer Experience ---
def page_user_buyer():
    st.title("👤 User & Buyer Experience (FR-UM-01, FR-DS-03, FR-EC-01)")
    st.markdown("### User-Buyer Registration and Account Management")
    
    st.subheader("1. User Profile Setup")
    st.text_input("User Name", "ArtLover25")
    st.text_input("Email", "buyer@example.com")
    st.selectbox("Communication Preferences", ["Email only", "Push Notifications", "Both"])
    st.button("Save Profile Changes")
    st.markdown("---")
    
    st.subheader("2. Artist Followership (FR-DS-03)")
    st.markdown("Users can follow artists to personalize their discovery feed.")
    followed_artists = st.multiselect("Artists You Follow", ["Alex Turner", "Maria Rodriguez", "Poet Laureate"], default=["Maria Rodriguez"])
    st.info(f"Your main feed (Art Discovery Portal) now prioritizes new art from: {', '.join(followed_artists)}.")
    st.markdown("---")

    st.subheader("3. Shopping & Purchasing (FR-EC-01)")
    col_cart, col_checkout = st.columns(2)
    with col_cart:
        st.metric("Items in Cart", 2)
        st.markdown("**Total Estimated Cost:** $600.00")
    with col_checkout:
        st.button("Proceed to Secure Checkout", use_container_width=True)
        st.caption("The checkout process integrates multiple payment gateways and secure shipping options.")
        
# --- NEW PAGE: Communication and Alerts ---
def page_communication():
    st.title("💬 Communication & Alerts (FR-CM-01, FR-CM-02, FR-NF-01)")
    st.markdown("### Fostering Community and Direct Communication")
    
    st.subheader("1. Public Comments (FR-CM-01)")
    st.info("Simulated Public Comment Feed on 'Digital Sunset'")
    st.chat_message("user").write("Amazing colors! How long did this take to render?")
    st.chat_message("artist").write("Thank you! It was about 40 hours of modeling and rendering.")
    st.text_area("Post a new public comment...")
    st.button("Post Comment")
    st.markdown("---")

    st.subheader("2. Private Chat (FR-CM-02)")
    st.markdown("Enabling secure, private communication for commission negotiation and sale details.")
    st.selectbox("Active Private Chats", ["Alex Turner (Digital Sunset Commission)", "Support Team"])
    st.chat_message("user").write("I'm interested in commissioning a similar piece, 20% larger. Are you open to that?")
    st.chat_message("artist").write("Yes, let's discuss the final pricing and timeline here.")
    st.text_input("Send a secure message...")
    st.button("Send Message", key="send_private")
    st.markdown("---")

    st.subheader("3. Real-Time Push Notifications (FR-NF-01)")
    st.markdown("Simulated notifications received by a User-Buyer:")
    st.dataframe(pd.DataFrame({
        "Alert Type": ["New Art", "Bid Update", "Chat Message"],
        "Content": [
            "Maria Rodriguez posted 'The New Muse'!",
            "Your bid on 'A Quiet Day' was outbid.",
            "Alex Turner sent you a message regarding your commission."
        ]
    }), use_container_width=True)

# --- NEW PAGE: System Technical Overview ---
def page_technical_overview():
    st.title("⚙️ System Technical Overview")
    st.markdown("### Core Architecture and Non-Functional Requirements")

    st.subheader("1. System Structure: Service-Oriented Architecture (SOA) (NF-AR-01)")
    st.markdown("The system uses an SOA approach with independent, loosely coupled services. [Image of Service-Oriented Architecture Diagram]")
    st.markdown("""
    This architecture ensures **Scalability** and **Maintainability**.
    * **Core Services:** User, Artwork, Transaction, Search & Feed, Communication, and Notification.
    * **API Gateway:** Centralized access point for all Frontend Clients (Mobile/Web).
    * **Data Storage:** Persistent database (NF-SR-02) for transactional data (e.g., PostgreSQL) and specialized data stores for search/caching (e.g., Elasticsearch, Redis).
    """)
    st.markdown("---")

    st.subheader("2. Supported Artist Types and Data (FR-AM-01)")
    st.markdown("The platform is designed to handle diverse data types based on the artist's medium:")
    st.dataframe(pd.DataFrame({
        "Type of Artist": ["Visual Artist", "Performing Artist", "Literary Arts", "Design Arts"],
        "Example Mediums": ["Painter, Sculptor, Digital Arts", "Musician, Dancer, Actor", "Novelist, Poet, Playwright", "Graphic Designer, Industrial Designer"],
        "Primary Data Type": ["Images/3D Models/AR Assets", "Video/Audio Files", "Digital Text/E-book", "Design Schematics"]
    }), use_container_width=True)
    st.markdown("---")

    st.subheader("3. Non-Functional Requirements (NFRs)")
    
    col_perf, col_security = st.columns(2)
    with col_perf:
        st.markdown("**Performance & Availability (NF-PR-01, NF-PR-02)**")
        st.markdown("""
        - **Responsiveness:** 95% of page loads under 2 seconds.
        - **Availability:** Target 99.5% uptime.
        - **Offline Functionality (NF-SR-03):** Critical data (browsed art, profiles) cached for limited offline viewing.
        """)
    
    with col_security:
        st.markdown("**Security & Persistence (NF-SR-01, NF-SR-02)**")
        st.markdown("""
        - **Data Security:** All sensitive data (PII, passwords) encrypted at rest and in transit (TLS 1.3+, AES-256).
        - **Data Persistence:** Use of a robust database with regular backups for all transactional and user data.
        """)


# --- EXISTING PAGES (Updated from previous turn) ---

def page_art_browser():
    """Simulates the main user browsing experience with search and filters."""
    st.title("🎨 Art Discovery Portal (FR-DS-01, FR-DS-02)")
    st.markdown("### Browse, Search, and Filter")
    st.markdown("Use the sidebar to filter the available pieces, simulating the platform's sophisticated search algorithm.")

    # --- Sidebar for Filtering ---
    st.sidebar.header("Advanced Search & Filter")

    # 1. Search Bar
    search_query = st.sidebar.text_input("Search by Title or Keyword", "")

    # 2. Medium Filter
    all_mediums = ["All"] + sorted(df['Medium'].unique().tolist())
    selected_medium = st.sidebar.selectbox("Filter by Medium", all_mediums)

    # 3. Tier Filter (Simulating access/quality)
    all_tiers = ["All"] + list(ARTIST_TIERS.keys())
    selected_tier = st.sidebar.multiselect("Filter by Artist Tier", all_tiers, default=["All"])
    if "All" in selected_tier and len(selected_tier) > 1:
        selected_tier.remove("All")
    elif "All" in selected_tier and len(selected_tier) == 1:
        selected_tier = list(ARTIST_TIERS.keys())

    # 4. Immersive Capability Filter (The differentiator)
    ar_filter = st.sidebar.checkbox("Show AR-Enabled Art Only", value=False)
    vr_filter = st.sidebar.checkbox("Show VR-Enabled Art Only", value=False)


    # --- Apply Filters ---
    filtered_df = df.copy()

    # Search
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Title'].str.contains(search_query, case=False) |
            filtered_df['Artist'].str.contains(search_query, case=False) |
            filtered_df['Description'].str.contains(search_query, case=False)
        ]

    # Medium
    if selected_medium != "All":
        filtered_df = filtered_df[filtered_df['Medium'] == selected_medium]

    # Tier
    filtered_df = filtered_df[filtered_df['Tier'].isin(selected_tier)]

    # AR/VR
    if ar_filter:
        filtered_df = filtered_df[filtered_df['AR_Ready'] == True]
    if vr_filter:
        filtered_df = filtered_df[filtered_df['VR_Ready'] == True]


    # --- Display Results ---
    if filtered_df.empty:
        st.info("No art pieces match your current filters. Try broadening your search!")
    else:
        st.metric(label="Total Results Found", value=len(filtered_df))
        cols_per_row = 3
        cols = st.columns(cols_per_row)

        for i, row in filtered_df.iterrows():
            with cols[i % cols_per_row]:
                
                with st.container(border=True): # Gives a nice visual grouping/border for the card
                    # Image
                    st.image("https://placehold.co/600x400/1e293b/FFFFFF?text=ART+ID+"+str(row['ID']), 
                             caption=f"{row['Title']} by {row['Artist']}", use_column_width=True)
                    
                    # Title and Price
                    st.subheader(f"{row['Title']}")
                    st.markdown(f"**Price:** <span style='font-size: 1.2em; color: #10b981;'>${row['Price']:,}</span>", unsafe_allow_html=True)
                    
                    # Description
                    with st.expander("Details"):
                        st.markdown(f"**Artist:** {row['Artist']}")
                        st.markdown(f"**Medium:** {row['Medium']}")
                        st.markdown(f"*{row['Description']}*")
                
                # Highlight Immersive Features
                immersive_tags = []
                if row['AR_Ready']:
                    immersive_tags.append("📱 AR View")
                if row['VR_Ready']:
                    immersive_tags.append("👓 VR Gallery")

                st.markdown(f"**Tier:** <span style='background-color:#{ARTIST_TIERS[row['Tier']]['color']}30; padding: 4px; border-radius: 5px; font-size: 0.8em;'>{row['Tier']}</span>", unsafe_allow_html=True)

                if immersive_tags:
                    st.markdown(" ".join(f"<span style='background-color:#34d399; padding: 3px 6px; border-radius: 5px; color: white; font-size: 0.75em;'>{tag}</span>" for tag in immersive_tags), unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #ef4444; font-size: 0.8em;'>Standard Listing</span>", unsafe_allow_html=True)

                st.button("View Details", key=f"details_{row['ID']}", use_container_width=True)
                st.markdown("---")


def page_sales_simulator():
    """Simulates the core business logic: percentage splitting."""
    st.title("💰 Commission & Sales Split Simulator (Business Model)")
    st.markdown("### Transparency in Transactions")
    st.markdown("This feature demonstrates how the **Renaissance Transaction Service** automatically manages the percentage splitting between all stakeholders (Artist, Platform, and optional Studio/Gallery).")

    st.subheader("1. Configure the Sale")
    col1, col2 = st.columns(2)

    with col1:
        sale_price = st.number_input("Final Sale Price ($)", min_value=100.0, max_value=100000.0, value=2500.0, step=100.0)
        
    with col2:
        selected_artist_tier = st.selectbox("Artist Membership Tier", list(ARTIST_TIERS.keys()), index=2)
        platform_fee_rate = ARTIST_TIERS[selected_artist_tier]["fee_pct"]
        st.caption(f"Platform Fee for **{selected_artist_tier}** is **{platform_fee_rate}%**.")

    st.subheader("2. Stakeholder Involvement (Commissions/Studios)")
    studio_involvement = st.checkbox("Is a Studio/Gallery involved in this sale?", value=True)
    
    studio_fee_rate = 0
    if studio_involvement:
        studio_fee_rate = st.slider("Studio/Gallery Commission Rate (%)", min_value=0, max_value=30, value=15)
        st.warning(f"Note: Total commission (Platform + Studio) must be less than 100%. Current max split: {platform_fee_rate + studio_fee_rate}%")

    
    # --- Calculation ---
    total_commission_rate = platform_fee_rate + studio_fee_rate
    
    platform_fee = sale_price * (platform_fee_rate / 100)
    studio_fee = sale_price * (studio_fee_rate / 100)
    artist_payout = sale_price - platform_fee - studio_fee
    
    artist_percent = 100 - total_commission_rate

    if artist_payout < 0:
        st.error("Error: Total Commission Rate exceeds 100%. Please adjust the rates.")
        return

    st.subheader(f"3. Transaction Breakdown for a ${sale_price:,.2f} Sale")

    st.markdown(
        f"""
        <div style='border: 2px solid #3b82f6; border-radius: 10px; padding: 20px; background-color: #eff6ff;'>
            <p style='font-size: 1.2em; font-weight: bold;'>Artist Payout (Revenue after fees):</p>
            <p style='font-size: 2em; color: #10b981;'>${artist_payout:,.2f} <span style='font-size: 0.6em; font-weight: normal; color: #4b5563;'>({artist_percent:.1f}% of Sale)</span></p>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("#### Commission Distribution Details")
    
    col_plat, col_studio = st.columns(2)
    
    with col_plat:
        st.metric(
            label=f"Renaissance Platform Fee ({platform_fee_rate}%)", 
            value=f"${platform_fee:,.2f}", 
            delta=f"Ensures scalability and marketing exposure."
        )
    with col_studio:
        if studio_involvement:
            st.metric(
                label=f"Studio/Gallery Cut ({studio_fee_rate}%)", 
                value=f"${studio_fee:,.2f}",
                delta="Direct payment to the managing studio or gallery."
            )
        else:
            st.info("No Studio/Gallery commission applied.")
            
    st.markdown("---")
    st.info("**Key Feature:** This transparent, automated process eliminates disputes and simplifies legal and financial tracking for all parties.")


def page_immersive_demo():
    """Focuses on the AR/VR features as the core differentiator."""
    st.title("👓 Immersive Art Experience Demo")
    st.markdown("### The Competitive Edge: AR & VR Integration")
    st.markdown("Renaissance is designed to solve the physical limitations of art display by leveraging **Augmented and Virtual Reality** technology.")
    
    st.subheader("1. Augmented Reality (AR) Preview")
    st.markdown("Using our mobile app, buyers can immediately see how a 2D painting or 3D sculpture looks *in their actual space*.")
    
    st.image("https://placehold.co/800x400/10b981/FFFFFF?text=Simulated+AR+View", caption=": A 3D digital sculpture placed convincingly in a photo of a living room.", use_column_width=True)
    
    st.info("""
    **Demo Scenario:** The user selects "Digital Sunset" (Semi-Pro Tier) in the Art Browser, which is flagged as 'AR Ready'. 
    They click a button, and the app uses their phone camera feed to place the digital art piece on their wall, correctly scaled.
    """)
    
    st.subheader("2. Virtual Reality (VR) Gallery Tours")
    st.markdown("For large, high-value works (typically Studio/Gallery Tier), users can explore the artist's environment or a curated exhibition.")
    
    st.image("https://placehold.co/800x400/0ea5e9/FFFFFF?text=Simulated+VR+Gallery", caption=": A panoramic view inside a modern, digital art gallery accessible via VR headset.", use_column_width=True)

    st.warning("""
    **Demo Scenario:** The user selects "The Iron Muse" (Studio/Gallery Tier), which is 'VR Ready'. 
    They connect via a VR headset and are transported into the artist's private virtual studio, allowing them to walk around the sculpture and view its texture and scale in a fully immersive 3D environment.
    """)
    
    
# --- Main App Logic ---
def main():
    
    st.sidebar.markdown(
        """
        # ⚜️ Renaissance Proposal Demo
        A prototype for an e-commerce platform for artists and crafters, highlighting key functionalities.
        """
    )
    
    # Simple navigation with all the new pages
    app_mode = st.sidebar.radio("Navigation", [
        "Art Discovery Portal", 
        "Commission & Sales Split Simulator", 
        "Immersive Art Experience Demo",
        "------", # Separator
        "Artist/Art Management", 
        "User/Buyer Experience",
        "Communication & Alerts",
        "System Technical Overview",
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Artist Tier Descriptions")
    for tier, data in ARTIST_TIERS.items():
        st.sidebar.markdown(f"**{tier}:** {data['description']}")


    if app_mode == "Art Discovery Portal":
        page_art_browser()
    elif app_mode == "Commission & Sales Split Simulator":
        page_sales_simulator()
    elif app_mode == "Immersive Art Experience Demo":
        page_immersive_demo()
    elif app_mode == "Artist/Art Management":
        page_artist_management()
    elif app_mode == "User/Buyer Experience":
        page_user_buyer()
    elif app_mode == "Communication & Alerts":
        page_communication()
    elif app_mode == "System Technical Overview":
        page_technical_overview()

if __name__ == "__main__":
    main()