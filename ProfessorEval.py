import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud
import altair as alt
import os

# Define file path for the dataset (can be adjusted as needed)
dataset_file = "professor_feedback.csv"

# Step 0: Load pre-existing dataset or create a new one if it doesn't exist
if os.path.exists(dataset_file):
    feedback_df = pd.read_csv(dataset_file)
else:
    # Initialize an empty DataFrame if the dataset doesn't exist yet
    feedback_df = pd.DataFrame(columns=['Professor', 'Clarity', 'Engagement', 'Course Structure', 'Responsiveness', 'Overall Effectiveness', 'Feedback Text'])

# Title
st.title("Professor's Performance Evaluation System")

# Step 1: Feedback Collection
st.header("Submit Feedback")

# Dropdown to select a professor
professor = st.selectbox("Select the Professor", ["Prof. A", "Prof. B", "Prof. C"])

# Collect quantitative feedback
clarity = st.slider("Clarity of explanations (1-5)", 1, 5, 3)
engagement = st.slider("Student engagement (1-5)", 1, 5, 3)
course_structure = st.slider("Course structure (1-5)", 1, 5, 3)
responsiveness = st.slider("Responsiveness to questions (1-5)", 1, 5, 3)
overall_effectiveness = st.slider("Overall effectiveness (1-5)", 1, 5, 3)

# Collect qualitative feedback
feedback_text = st.text_area("Open-ended feedback (optional)")

# Step 2: Add new feedback to the dataset
if st.button("Submit Feedback"):
    # Create a new entry for the current feedback
    new_feedback = {
        'Professor': professor.split()[-1],  # Extracts 'A', 'B', or 'C'
        'Clarity': clarity,
        'Engagement': engagement,
        'Course Structure': course_structure,
        'Responsiveness': responsiveness,
        'Overall Effectiveness': overall_effectiveness,
        'Feedback Text': feedback_text
    }
    
    # Append the new feedback to the DataFrame using pd.concat
    feedback_df = pd.concat([feedback_df, pd.DataFrame([new_feedback])], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    feedback_df.to_csv(dataset_file, index=False)
    
    st.success("Feedback submitted successfully!")
    st.write("### Updated Feedback Data:")
    st.write(feedback_df)

# Filter feedback for the selected professor
selected_professor_df = feedback_df[feedback_df['Professor'] == professor.split()[-1]]

# Step 3: Quantitative Evaluation (Visualization of the Dataset)
st.header(f"Quantitative Evaluation for {professor}")

if not selected_professor_df.empty:
    # Show average ratings for the selected professor
    st.write(f"### Average Ratings Overview for {professor}")
    average_ratings = selected_professor_df[['Clarity', 'Engagement', 'Course Structure', 'Responsiveness', 'Overall Effectiveness']].mean()
    st.write(average_ratings)

    # Visualize the average ratings for the selected professor
    st.write(f"### Average Ratings Bar Chart for {professor}")
    fig, ax = plt.subplots()
    average_ratings.plot(kind='bar', ax=ax)
    plt.title(f"Average Ratings Across Categories for {professor}")
    st.pyplot(fig)

    # Identify areas for improvement (ratings below 3)
    st.write(f"### Areas for Improvement for {professor}:")
    for category in ['Clarity', 'Engagement', 'Course Structure', 'Responsiveness', 'Overall Effectiveness']:
        if average_ratings[category] < 3:
            st.write(f"- {category}: Needs improvement (average rating < 3).")

# Step 4: Qualitative Evaluation (Sentiment Analysis and Word Cloud)
st.header(f"Qualitative Evaluation for {professor}")

if not selected_professor_df['Feedback Text'].dropna().empty:
    # Apply sentiment analysis to the selected professor's feedback using TextBlob
    selected_professor_df['Sentiment'] = selected_professor_df['Feedback Text'].apply(
        lambda text: TextBlob(text).sentiment.polarity if isinstance(text, str) else None
    )

    # Show average sentiment score for the selected professor
    avg_sentiment = selected_professor_df['Sentiment'].mean()
    st.write(f"### Average Sentiment Score for {professor}: {avg_sentiment:.2f} (Range: -1 to 1)")

    exclude_words = ['the', 'and', 'to', 'of', 'a', 'in', 'professor', 'Prof', 'Prof.', 'class', 'always', 'material', 'professors','had','made','want','he','they','she','I']  

    # Generate word cloud for the selected professor's feedback
    st.write(f"### Word Cloud for {professor}'s Feedback")
    all_feedback_text = ' '.join(selected_professor_df['Feedback Text'].dropna())

    # Create a set of stopwords
    stopwords = set(WordCloud().stopwords).union(set(exclude_words))

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(all_feedback_text)

    # Plotting the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Step 5: Overall Performance Insights with Altair
st.header(f"Performance Insights for {professor}")

if not selected_professor_df.empty:
    performance_data = selected_professor_df[['Clarity', 'Engagement', 'Course Structure', 'Responsiveness', 'Overall Effectiveness']].mean().reset_index()
    performance_data.columns = ['Criteria', 'Score']

    chart = alt.Chart(performance_data).mark_bar().encode(
        x='Criteria',
        y='Score',
        color='Criteria',
    ).properties(title=f"{professor}'s Teaching Performance")
    
    st.altair_chart(chart)

# Final Note
st.write(f"Thank you for your feedback! It will help improve {professor}'s teaching performance.")
