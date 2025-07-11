# 📚 Book Recommender System

An interactive and modular book recommender using machine learning and NLP techniques. This system classifies books by genre and emotion, and recommends similar books using vector search. A simple Gradio dashboard is included for quick exploration.

---

## 🚀 Features

- 📖 Content-based recommendations from book descriptions
- 💬 Sentiment analysis & genre classification using NLP
- 🔍 Vector-based similarity search with Sentence Transformers
- 🖼️ Gradio app for interactive recommendation browsing

---

## 🗂️ Folder Structure

```bash
Book-Recommender-System/
│
├── data/                        # Cleaned and tagged datasets
│   ├── books_cleaned.csv
│   ├── books_with_categories.csv
│   ├── books_with_emotions.csv
│   └── tagged_description.txt
│
├── notebooks/                   # Jupyter notebooks
│   ├── data_exploration.ipynb
│   ├── sentiment_analysis.ipynb
│   ├── text_classification.ipynb
│   └── vector_search.ipynb
│
├── app/                         # Gradio dashboard
│   ├── gradio_dashboard.py
│   └── cover_not_found.jpg
│
├── .env                         # Environment variables (optional)
├── .gitignore                   # Files/folders to exclude from Git
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview
