import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Books Dashboard", layout="wide")
st.title("Books to Scrape – Data Dashboard")

df = pd.read_csv("cleaned_books.csv")
st.success("✅ Data Loaded Successfully from Local File!")


if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)
df.columns = [col.lower() for col in df.columns]  
df = df.drop_duplicates()


st.subheader("First 10 Records [Books]")
st.dataframe(df.head(10))


if 'price' in df.columns:
    st.subheader("Price Distribution of Books")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['price'], bins=30, kde=True, ax=ax1)
    ax1.set_title("Price Distribution")
    ax1.set_ylabel("Number of Books")
    st.pyplot(fig1)

if 'rating' in df.columns:
    st.subheader("Number of Books by Rating")
    fig, ax = plt.subplots(figsize=(10, 6))
    df['rating'].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=['skyblue', 'plum', 'khaki', 'lightgreen', 'lightcoral'], ax=ax)
    ax.set_title("Rating Distribution")
    ax.set_ylabel("")
    st.pyplot(fig)

# Correlation Heatmap
numeric_df = df.select_dtypes(include=['float64', 'int64'])
st.subheader("Heatmap Correlation between Valuation and Price")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

# Barplot:
st.subheader("Average Price by Rating")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='rating', y='price', data=df, hue='rating', palette="Set2", ax=ax)
ax.set_title("Price Distribution by Rating")
ax.set_xlabel("Rating")
ax.set_ylabel("Average Price")
plt.tight_layout()
st.pyplot(fig)

# Boxplot: 
st.subheader("Price Distribution Based on Book Availability")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='availability', y='price', data=df, ax=ax)
ax.set_title("Price Distribution by Availability")
ax.set_xlabel("Availability Status")
ax.set_ylabel("Price")
plt.tight_layout()
st.pyplot(fig)

# Summary Metrics
if 'price' in df.columns:
    st.subheader("Summary Statistics")
    st.metric("Average Price", f"{df['price'].mean():.2f} £")
    st.metric("Max Price", f"{df['price'].max():.2f} £")
    st.metric("Min Price", f"{df['price'].min():.2f} £")
    st.metric("Total Number of Books:", f"{len(df)} Books")

st.write("Price Standard Deviation:", df['price'].std())


rating_mapping = {'Bad': 1, 'Good': 2, 'Excellent': 3}
df['Rating_Numeric'] = df['rating'].map(rating_mapping)

st.write("Price Skewness:", df['price'].skew())
st.write("Are the books available?")
st.write(df["availability"].value_counts())

st.write("Distribution of Rating:")
st.write(df["rating"].value_counts())


if 'price' in df.columns and 'rating' in df.columns:
    avg_price_by_rating = df.groupby("rating")["price"].mean().sort_index()
    st.write("Average Price by Rating")
    st.write(avg_price_by_rating)
