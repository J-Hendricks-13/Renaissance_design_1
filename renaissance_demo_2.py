import streamlit as st
import pandas as pd
import random
import time

# --- Configuration and Data ---
st.set_page_config(
    page_title="Renaissance Mobile App Demo",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide the default sidebar for mobile look
)

# 1. Dummy Data: Artists and Art Pieces
ARTIST_TIERS = {
    "Emerging": {"color": "gray", "fee_pct": 20},
    "Semi-Pro": {"color": "blue", "fee_pct": 10},
    "Studio/Gallery": {"color": "gold", "fee_pct": 5}
}

ART_DATA = [
    {"ID": 1, "Title": "Digital Sunset", "Artist": "Alex Turner", "Medium": "Digital Arts",
     "Price": 550, "Tier": "Semi-Pro", "AR_Ready": True, "Image": "https://placehold.co/600x400/228B22/FFFFFF?text=Sunset"},
    {"ID": 2, "Title": "The Iron Muse", "Artist": "Maria Rodriguez", "Medium": "Sculptor",
     "Price": 12000, "Tier": "Studio/Gallery", "AR_Ready": True, "Image": "https://placehold.co/600x400/8B4513/FFFFFF?text=Sculpture"},
    {"ID": 3, "Title": "A Quiet Day", "Artist": "John Smith", "Medium": "Painter",
     "Price": 150, "Tier": "Emerging", "AR_Ready": False, "Image": "https://placehold.co/600x400/1E90FF/FFFFFF?text=Painting"},
    {"ID": 4, "Title": "Metropolis Rhapsody", "Artist": "Art Collective 7", "Medium": "Graphic Designer",
     "Price": 3500, "Tier": "Studio/Gallery", "AR_Ready": True, "Image": "https://placehold.co/600x400/FFD700/000000?text=Design"},
    {"ID": 5, "Title": "Winter's Poem", "Artist": "Poet Laureate", "Medium": "Literary Arts",
     "Price": 50, "Tier": "Semi-Pro", "AR_Ready": False, "Image": "https://placehold.co/600x400/FF6347/FFFFFF?text=Poem"}
] * 10 # Repeat data to create a longer scrollable feed

df = pd.DataFrame(ART_DATA)
# Add some dummy transactions/orders
ORDERS_DATA = [
    {"ID": 101, "Item": "Digital Sunset", "Artist": "Alex Turner", "Price": 550, "Status": "Delivered"},
    {"ID": 102, "Item": "Metropolis Rhapsody", "Artist": "Art Collective 7", "Price": 3500, "Status": "Shipped"},
    {"ID": 103, "Item": "A Quiet Day", "Artist": "John Smith", "Price": 150, "Status": "Processing"}
]
df_orders = pd.DataFrame(ORDERS_DATA)


# --- Reusable Components (For the Mobile look) ---

def custom_header(title, icon="🔥"):
    """Creates a simplified, top-bar style header."""
    st.markdown(f'<div style="text-align: center; font-size: 1.5em; font-weight: bold; padding: 10px 0; border-bottom: 1px solid #eee;">{icon} {title}</div>', unsafe_allow_html=True)
    st.markdown("---")

def art_feed_card(row):
    """Renders a single art piece as an Instagram-style post/card."""
    artist_name = row['Artist']
    tier = row['Tier']
    
    # 1. Profile Bar (like IG post header)
    col_profile, col_title, col_icon = st.columns([1, 8, 1])
    with col_profile:
        # Placeholder for a round profile image
        st.markdown(f'<div style="width: 40px; height: 40px; background-color: #{ARTIST_TIERS[tier]["color"]}aa; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2em; font-weight: bold;">{artist_name[0]}</div>', unsafe_allow_html=True)
    with col_title:
        st.markdown(f"**{artist_name}** <span style='font-size: 0.8em; color: gray;'>- {tier}</span>", unsafe_allow_html=True)
        st.caption(row['Title'])
    with col_icon:
        st.button("...", key=f"menu_{row['ID']}")

    # 2. Art Image (the main content)
    st.image(row['Image'], use_column_width=True)
    
    # 3. Engagement Icons (Like, Comment, Save)
    col_like, col_comment, col_ar, col_price = st.columns([1, 1, 1, 7])
    with col_like:
        st.button("❤️", key=f"like_{row['ID']}")
    with col_comment:
        st.button("💬", key=f"comment_{row['ID']}")
    with col_ar:
        if row['AR_Ready']:
             st.button("📱 AR", key=f"ar_{row['ID']}", help="View in Augmented Reality")
    with col_price:
        st.markdown(f"<p style='text-align: right; font-size: 1.4em; color: #10b981;'>**${row['Price']:,}**</p>", unsafe_allow_html=True)
        
    # 4. Description/Details
    st.caption(f"**{row['Artist']}**: {row['Title']} - *{row['Medium']}*")
    st.button("Purchase / View Details", key=f"buy_{row['ID']}", use_container_width=True)
    st.markdown("---")


# --- PAGE DEFINITIONS ---

def page_discover():
    """FR-DS-01, FR-DS-02: Content Feed and Search."""
    custom_header("Discover Art Feed", icon="✨")
    
    # Search Bar (Top of the feed like IG)
    search_query = st.text_input("Search Artworks, Artists, or Keywords", "", placeholder="Search (FR-DS-02)")
    
    # Live/Content Toggles (Under the search bar)
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.button("Feed", use_container_width=True)
    with col_t2:
        st.button("Live 🔥", use_container_width=True) # Placeholder for Live feature
    with col_t3:
        st.button("AR Ready", use_container_width=True)
    st.markdown("---")

    # Apply simple filtering based on the search query
    if search_query:
        filtered_df = df[
            df['Title'].str.contains(search_query, case=False) |
            df['Artist'].str.contains(search_query, case=False)
        ]
    else:
        filtered_df = df

    # Content Scrolling (Feed)
    if filtered_df.empty:
        st.info("No results found for your search.")
    else:
        for i, row in filtered_df.iterrows():
            art_feed_card(row)


def page_transactions_orders():
    """FR-EC-01, FR-EC-02, FR-UM-01: Transaction History and Orders."""
    custom_header("Transactions & Orders", icon="💳")
    
    st.subheader("My Purchase History")
    st.markdown("_Tracking the journey of your art from studio to your door._")
    
    for i, order in df_orders.iterrows():
        # Order Card
        col_id, col_item, col_status = st.columns([2, 5, 3])
        with col_id:
            st.caption(f"Order #{order['ID']}")
        with col_item:
            st.markdown(f"**{order['Item']}** by {order['Artist']}")
        with col_status:
            status_style = 'green' if order['Status'] == 'Delivered' else 'orange'
            st.markdown(f'<span style="color:{status_style}; font-weight:bold;">{order["Status"]}</span>', unsafe_allow_html=True)
        
        st.markdown(f"**Total:** ${order['Price']:,}")
        st.markdown("---")
        
    st.subheader("Sales Payouts (Artist View)")
    st.info("View your detailed payout simulator in the **Dashboard** page.")
    st.dataframe(df[['Artist', 'Title', 'Price']].head(2), use_container_width=True)


def page_dashboard():
    """FR-UM-01, FR-AM-02: Central hub for user metrics/management (Admin/Artist focused)."""
    custom_header("Dashboard", icon="📊")
    
    st.subheader("Your Performance Overview (Artist View)")
    
    col_sales, col_views, col_tier = st.columns(3)
    with col_sales:
        st.metric("Total Sales (YTD)", "$16,200", delta="12% from last month")
    with col_views:
        st.metric("Profile Views", "8,450", delta="5% from last month")
    with col_tier:
        st.metric("Current Tier", "Studio/Gallery", delta_color="off")
        
    st.markdown("---")
    
    st.subheader("Quick Actions")
    st.button("Manage My Art Listings", use_container_width=True)
    st.button("Run Sales Split Simulator", use_container_width=True)
    st.button("Upgrade Membership (Lower Fees)", use_container_width=True)
    
    st.markdown("---")
    st.subheader("Immersive Assets Status")
    st.markdown("*5 of your 12 artworks are AR Ready.*")
    st.progress(5/12)


def page_messages():
    """FR-CM-01, FR-CM-02: Communication and Social Engagement."""
    custom_header("Messages & Engagement", icon="💬")
    
    # Top Tab Bar for Social
    st.markdown('<h3 style="text-align: center;">Social Engagement</h3>', unsafe_allow_html=True)
    col_inbox, col_notifs, col_live = st.columns(3)
    with col_inbox:
        st.button("Inbox (3)", use_container_width=True)
    with col_notifs:
        st.button("Notifications (7)", use_container_width=True)
    with col_live:
        st.button("Live Events", use_container_width=True)

    st.markdown("---")
    
    st.subheader("Private Chats (Commissions & Sales)")
    
    st.chat_message("user", avatar="👤").write("I'd like to commission a larger version of The Iron Muse.")
    st.chat_message("artist", avatar="👨‍🎨").write("Sounds great! Let's discuss size and materials. I'll send a price quote.")
    
    st.text_input("Reply to Maria Rodriguez...", placeholder="Type your secure message...")
    st.button("Send Secure Message", use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Public Post Comments")
    st.caption("A feed of comments on your most recent post.")
    st.dataframe(pd.DataFrame({"User": ["ArtCritic", "Buyer123"], "Comment": ["Stunning work!", "How much for shipping?"], "Likes": [12, 5]}), use_container_width=True)


def page_profile():
    """FR-UM-01: User Profile and Account Settings."""
    custom_header("My Profile", icon="👤")
    
    # Profile Header
    col_pfp, col_stats = st.columns([2, 5])
    with col_pfp:
        # Placeholder for PFP
        st.markdown('<div style="width: 100px; height: 100px; background-color: #ef4444; border-radius: 50%; margin: 10px auto;"></div>', unsafe_allow_html=True)
    with col_stats:
        st.subheader("ArtLover25")
        st.markdown("Digital Art Collector & AR Enthusiast")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.metric("Following", 45)
        with col_f2:
            st.metric("Followers", 120)
            
    st.markdown("---")
    
    st.subheader("My Galleries & Collections")
    st.button("My Favorites (Liked Art)", use_container_width=True)
    st.button("My Commission History", use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Account Settings")
    st.selectbox("Language Preference", ["English", "Spanish", "French"])
    st.button("Log Out", use_container_width=True)


# --- Corrected Main App Logic (Mobile Navbar Implementation) ---
def main_app():
    
    # 1. Simulate Mobile Navigation via Tabs
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Discover"
        
    page_options = {
        "Discover": "✨", 
        "Transactions": "💳", 
        "Dashboard": "📊", 
        "Messages": "💬", 
        "Profile": "👤"
    }

    # Custom CSS to hide the default Streamlit footer/menu and style the fixed bottom navigation bar
    st.markdown(
        """
        <style>
        #MainMenu, footer {visibility: hidden;}
        /* Fixed Bottom Navigation Style */
        .fixed-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #ffffff;
            border-top: 1px solid #ddd;
            padding: 5px 0;
            z-index: 9999;
            display: flex;
            justify-content: space-around;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Optional shadow */
        }
        .nav-icon {
            text-align: center;
            font-size: 1.5em; /* Icon size */
            cursor: pointer;
            padding: 5px;
            color: gray; /* Default color */
        }
        .active-nav-icon {
            color: #ef4444 !important; /* Highlight color for active page */
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    # --- Check for URL Parameter to Handle Navigation ---
    # This is a robust way to handle navigation without relying on st.button's limitations
    query_params = st.query_params
    
    if "nav" in query_params:
        nav_page = query_params["nav"][0] if isinstance(query_params["nav"], list) else query_params["nav"]
        if nav_page in page_options:
            st.session_state['current_page'] = nav_page


    # --- Render Navigation Bar ---
    # We use st.markdown with links to update the URL query parameter
    nav_html = '<div class="fixed-bottom-nav">'
    cols = st.columns(len(page_options))
    
    for page_name, icon in page_options.items():
        is_active = st.session_state['current_page'] == page_name
        icon_class = "active-nav-icon" if is_active else ""
        
        # Create a link that updates the URL query parameter (e.g., ?nav=Dashboard)
        # We need to manually construct the link to the current Streamlit URL with the new parameter
        # Since we can't reliably get the full URL, the most common fix is using an explicit button instead
        
        # Reverting to the button method, but separating the icon from the button label
        with cols[list(page_options.keys()).index(page_name)]:
            
            # Use a button with a non-HTML label to switch the state
            if st.button(icon, key=f"nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()

            # The visual highlight is the issue. Let's use a cleaner approach:
            # We will use st.button, but apply CSS to make it look like an icon link
            # We must use the icon as the label since no HTML is allowed.
            # The CSS above handles the button styling.
            
            # Add a visual indicator below the icon for the active page
            if is_active:
                st.markdown(f'<div style="height: 3px; background-color: #ef4444; width: 100%; margin-top: -10px; border-radius: 5px;"></div>', unsafe_allow_html=True)
            else:
                # Add a spacer to keep the layout consistent
                st.markdown(f'<div style="height: 3px; width: 100%;"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # End of fixed-bottom-nav container

    # Add a buffer space at the bottom so content isn't hidden by the nav bar
    st.markdown("<br><br><br><br>", unsafe_allow_html=True) 

    # 2. Render the selected page content
    if st.session_state['current_page'] == "Discover":
        page_discover()
    elif st.session_state['current_page'] == "Transactions":
        page_transactions_orders()
    elif st.session_state['current_page'] == "Dashboard":
        # The Dashboard page is where we'll incorporate the Sales Split Simulator
        page_dashboard() 
    elif st.session_state['current_page'] == "Messages":
        page_messages()
    elif st.session_state['current_page'] == "Profile":
        page_profile()

if __name__ == "__main__":
    main_app()