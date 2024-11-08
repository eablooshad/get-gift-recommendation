from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data once at startup
data = pd.read_csv('data/inventory.csv')

# Get unique categories for the category checkboxes
categories = data['Category'].unique().tolist()

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the selected categories from the form
    selected_categories = request.form.getlist('categories')
    
    # Filter the data based on selected categories
    if selected_categories:
        filtered_data = data[data['Category'].isin(selected_categories)]
    else:
        filtered_data = data  # If no category is selected, show all items as a default

    return render_template('recommendations.html', toys=filtered_data.to_dict(orient='records'))
