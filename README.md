# Project: Professor Evaluation Project

## Author
Maya Fetzer  
Semester: Fall 2024  
Course: CHEG 472  

## Purpose
This repository holds the code to run an app that will allow students to rate a professor. The professor will then get a wordcloud and recommedations to improve their teaching style based on student feedback. 

## Public App
Here is the public app for the professor evaluation.
https://profeval.streamlit.app/

## Files in this repository
ProfessorEval.py - the python code that analyzes a dataset and creates a professor evaluation app
professor_feedback.csv - an example dataset that rates three imaginary calculus professors
requirement.txt - the requirements file for this code

## Prerequisites

### Python
Ensure you have Python 3.10 or later installed.

### Libraries
Install the following libraries using pip:

```
pip install streamlit
pip install pandas
pip install matplotlib
pip install textblob
pip install wordcloud
pip install altair
```

## Explanation

- **Streamlit**: Provides a simple way to create interactive web applications with Python.
- **Matplotlib**: Used for creating visualizations like plots and charts.
- **Pandas**: Offers data structures and analysis tools for working with tabular data.
- **NumPy**: Provides efficient numerical operations and arrays.
- **TextBlob**: A library for processing textual data, offering functionalities like sentiment analysis and text translation.
- **WordCloud**: Used to generate word clouds from text data, offering an intuitive way to visualize word frequency.
- **Altair**: A declarative statistical visualization library based on Vega and Vega-Lite for producing insightful, interactive charts.
