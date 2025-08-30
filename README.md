# 📚 Books Analytics Dashboard

## 📝 Overview

This project is an **interactive data analytics dashboard** built with [Streamlit](https://streamlit.io/). It provides insightful visualizations and analysis for book pricing, ratings, and availability using data from the *Books to Scrape* dataset.

The dashboard allows users to:

* Filter books by price, rating, and availability
* Explore pricing patterns
* Analyze ratings
* Discover trends in stock availability

All in an easy-to-use web interface.

---

## ✨ Features

* **Interactive Filters**: Filter books by price range, rating categories, and availability status.
* **Dynamic Visualizations**:

  * Price distribution (histogram, boxplots)
  * Rating distribution (pie chart, bar chart)
  * Average price by rating
* **Key Metrics**: Quick insights like total books, average price, highest price, and most common rating.
* **Data Preview**: View the top records matching the current filter selection.
* **Clean UI**: Custom styling with a modern look and feel.

---

## 🗂 Data Source

The app uses a pre-cleaned dataset derived from the [Books to Scrape](http://books.toscrape.com/) website:

**File**: `cleaned_books.csv`

Columns include:

* **Title** – book name
* **Price** – book price in GBP (£)
* **Rating** – numerical rating (1–5)
* **Rating Category** – mapped to textual labels (`Poor`, `Fair`, `Good`, `Very Good`, `Excellent`)
* **Availability** – stock status (in-stock / out-of-stock)

---

## 🛠 Requirements

* Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

Libraries used:

* `streamlit`
* `pandas`
* `matplotlib`
* `seaborn`

---

## 🚀 Usage

Run the Streamlit app locally:

```bash
streamlit run streamlit_app.py
```

Then open the provided local URL (e.g., `http://localhost:8501`) in your browser.

---

## 📂 Project Structure

```
.
├── streamlit_app.py      # Main dashboard application
├── cleaned_books.csv     # Cleaned dataset
├── Untitled17.ipynb      # Jupyter notebook (analysis / preprocessing)
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## 📊 Example Insights

* **Price Patterns**: Most books are priced between £10–£50, with a few premium outliers.
* **Rating Impact**: Higher-rated books generally command higher prices.
* **Availability**: In-stock books show more price variability than out-of-stock ones.
* **Rating Distribution**: Identifies which rating category dominates the dataset.

---

## 🤝 Contributing

Contributions are welcome!

Please fork the repository, create a feature branch, and submit a pull request.

---

## 📄 License

This project is released under the MIT License. See the LICENSE file for details.
