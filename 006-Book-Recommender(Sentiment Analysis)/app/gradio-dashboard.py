import pandas as pd
import numpy as np
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma

import gradio as gr

# Load environment variables
load_dotenv()

# Load book data
books = pd.read_csv("books_with_emotions.csv")
books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
books["large_thumbnail"] = np.where(
    books["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    books["large_thumbnail"],
)

# Load and split documents
raw_documents = TextLoader("tagged_description.txt", encoding="utf-8").load()
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# Create embedding and Chroma DB
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_books = Chroma.from_documents(documents, embedding=embedding)

# Recommendation logic
def retrieve_semantic_recommendations(query, category="All", tone="All", initial_top_k=50, final_top_k=16):
    recs = db_books.similarity_search(query, k=initial_top_k)

    # Extract ISBNs from documents (assuming first token is ISBN)
    books_list = []
    for rec in recs:
        try:
            isbn = int(rec.page_content.strip('"').split()[0])
            books_list.append(isbn)
        except Exception:
            continue

    # Filter book DataFrame
    book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)

    if category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category]

    if tone == "Happy":
        book_recs = book_recs.sort_values(by="joy", ascending=False)
    elif tone == "Surprising":
        book_recs = book_recs.sort_values(by="surprise", ascending=False)
    elif tone == "Angry":
        book_recs = book_recs.sort_values(by="anger", ascending=False)
    elif tone == "Suspenseful":
        book_recs = book_recs.sort_values(by="fear", ascending=False)
    elif tone == "Sad":
        book_recs = book_recs.sort_values(by="sadness", ascending=False)

    return book_recs.head(final_top_k)

# Format results for Gradio Gallery
def recommend_books(query, category, tone):
    recommendations = retrieve_semantic_recommendations(query, category, tone)
    results = []

    for _, row in recommendations.iterrows():
        description = row.get("description", "")
        title = row.get("title", "Unknown Title")
        authors = row.get("authors", "Unknown Author")
        thumbnail = row.get("large_thumbnail", "cover-not-found.jpg")

        truncated_description = " ".join(description.split()[:30]) + "..."

        authors_split = authors.split(";")
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = authors

        caption = f"{title} by {authors_str}: {truncated_description}"
        results.append((thumbnail, caption))

    return results

# UI Dropdown Options
categories = ["All"] + sorted(books["simple_categories"].dropna().unique())
tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

# Gradio Dashboard
with gr.Blocks(theme=gr.themes.Monochrome()) as dashboard:
    gr.Markdown("# 📚 Semantic Book Recommender")

    with gr.Row():
        user_query = gr.Textbox(
            label="Please enter a description of a book:",
            placeholder="e.g., A story about forgiveness"
        )
        category_dropdown = gr.Dropdown(
            choices=categories,
            label="Please select a category:",
            value="All"
        )
        tone_dropdown = gr.Dropdown(
            choices=tones,
            label="Please select a tone:",
            value="All"
        )

    submit_button = gr.Button("Find recommendations")

    gr.Markdown("## 📖 Recommendations")
    output = gr.Gallery(label="Recommended books", columns=4, rows=4)

    submit_button.click(
        fn=recommend_books,
        inputs=[user_query, category_dropdown, tone_dropdown],
        outputs=output
    )

# Launch the app
if __name__ == "__main__":
    print("Launching Gradio app...")
    dashboard.launch(share=True)
