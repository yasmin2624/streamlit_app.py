import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Books Dashboard",
    layout="wide",
    page_icon="📚"
)

# Custom styling
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    h1 {color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;}
    h2 {color: #2980b9;}
    .stMetric {background-color: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    .stMetric label {font-size: 0.9rem; color: #7f8c8d;}
    .stMetric div {font-size: 1.4rem; color: #2c3e50;}
    .css-1aumxhk {background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# Title and header
st.title("📚 Books Analytics Dashboard")
st.markdown("Analyze book pricing, ratings, and availability from the Books to Scrape dataset.")

# Data loading
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/yasmin2624/streamlit_app.py/main/cleaned_books.csv"
    df = pd.read_csv(url)
    
    # تحويل التقييمات الرقمية إلى فئات نصية
    rating_map = {
        1: 'Poor',
        2: 'Fair',
        3: 'Good',
        4: 'Very Good',
        5: 'Excellent'
    }
    df['rating_category'] = df['Rating'].map(rating_map)
    
    return df

with st.spinner('Loading data...'):
    df = load_data()
    st.success("Data loaded successfully!")

# Data cleaning
df = df.rename(columns={
    'Title': 'title',
    'Price': 'price',
    'Availability': 'availability',
    'Rating': 'rating'
})
df = df.drop_duplicates()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    min_price, max_price = st.slider(
        "Price Range (£)",
        float(df['price'].min()),
        float(df['price'].max()),
        (float(df['price'].min()), float(df['price'].max()))
    )
    
    # تحويل التقييمات المتاحة بناء على البيانات الفعلية
    available_ratings = sorted(df['rating_category'].unique())
    selected_ratings = st.multiselect(
        "Select Ratings",
        options=available_ratings,
        default=available_ratings
    )
    
    availability = st.selectbox(
        "Availability",
        options=['All', 'True', 'False'],
        index=0
    )

# Apply filters
filtered_df = df[
    (df['price'] >= min_price) & 
    (df['price'] <= max_price) & 
    (df['rating_category'].isin(selected_ratings))
]

if availability != 'All':
    filtered_df = filtered_df[filtered_df['availability'] == (availability == 'True')]

# Key metrics
st.subheader("Key Metrics")
cols = st.columns(4)
cols[0].metric("Total Books", len(filtered_df))
cols[1].metric("Avg Price", f"£{filtered_df['price'].mean():.2f}")
cols[2].metric("Highest Price", f"£{filtered_df['price'].max():.2f}")
cols[3].metric("Most Common Rating", filtered_df['rating_category'].mode()[0])

# Data preview
with st.expander("View Data Preview"):
    st.dataframe(
        filtered_df.head(10),
        column_config={
            "price": st.column_config.NumberColumn("Price", format="£%.2f"),
            "rating": "Rating (Numeric)",
            "rating_category": "Rating Category",
            "availability": "Stock Status"
        },
        hide_index=True,
        use_container_width=True
    )

# Visualization tabs
tab1, tab2 = st.tabs(["Price Analysis", "Rating Analysis"])

with tab1:
    st.subheader("Price Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_df['price'], bins=25, kde=True, color='#3498db')
    plt.title("Distribution of Book Prices", pad=20)
    plt.xlabel("Price (£)")
    plt.ylabel("Count")
    st.pyplot(fig1)
    
    st.subheader("Price by Availability")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        x='availability',
        y='price',
        data=filtered_df,
        palette=['#3498db', '#e74c3c']
    )
    plt.title("Price Distribution by Availability", pad=20)
    plt.xlabel("Availability")
    plt.ylabel("Price (£)")
    st.pyplot(fig2)

with tab2:
    st.subheader("Rating Analysis")
    
    if not filtered_df.empty:
        # 1. Rating Distribution - Pie Chart
        st.subheader("Rating Distribution")
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        
        rating_order = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
        rating_counts = filtered_df['rating_category'].value_counts().reindex(rating_order, fill_value=0)
        
        colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
        
        # Create pie chart
        wedges, texts, autotexts = ax3.pie(
            rating_counts,
            labels=rating_counts.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
            textprops={'fontsize': 12}
        )
        
        # Equal aspect ratio ensures the pie is drawn as a circle
        ax3.axis('equal')  
        plt.title("Book Ratings Distribution", pad=20, fontsize=14)
        
        # Add legend
        ax3.legend(
            wedges,
            rating_counts.index,
            title="Rating Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        st.pyplot(fig3)
        
        # باقي الكود يبقى كما هو...
        # 2. Average Price by Rating
        st.subheader("Average Price by Rating")
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        
        avg_prices = filtered_df.groupby('rating_category')['price'].mean().reindex(rating_order, fill_value=0)
        
        bars = sns.barplot(
            x=avg_prices.index,
            y=avg_prices.values,
            palette=colors,
            ax=ax4
        )
        
        # Add data labels
        for bar in bars.patches:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2, height,
                    f'£{height:.2f}',
                    ha='center', va='bottom')
        
        plt.title("Average Price by Rating", pad=20)
        plt.xlabel("Rating")
        plt.ylabel("Average Price (£)")
        st.pyplot(fig4)
        
        # 3. Price Distribution by Rating
        st.subheader("Price Distribution by Rating")
        fig5, ax5 = plt.subplots(figsize=(12, 6))
        
        sns.boxplot(
            data=filtered_df,
            x='rating_category',
            y='price',
            order=rating_order,
            palette=colors,
            ax=ax5
        )
        
        plt.title("Price Distribution by Rating", pad=20)
        plt.xlabel("Rating")
        plt.ylabel("Price (£)")
        st.pyplot(fig5)
        
    else:
        st.warning("No data available for the selected filters")
# Insights
st.subheader("Key Insights")
insights = """
1. **Price Patterns**: Most books are priced between £10-£50, with a few premium outliers.
2. **Rating Impact**: Higher rated books generally command higher prices.
3. **Availability**: In-stock books show more price variability than out-of-stock ones.
4. **Rating Distribution**: Check which rating category has the most books.
"""
st.markdown(insights)

# Footer
st.markdown("---")
st.caption("© 2023 Books Analytics Dashboard | Data from Books to Scrape")