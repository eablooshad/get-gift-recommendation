from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load and prepare data once at startup
def load_data():
    try:
        df1 = pd.read_csv('data/inventory.csv')
        df2 = pd.read_csv('data/toy-inventory.csv')
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        exit()  # Stop execution if files are missing

    # Standardize 'Product ID' column to string type across DataFrames
    for df in [df1, df2]:
        if 'Product ID' not in df.columns:
            print(f"Error: 'Product ID' column not found in DataFrame.")
            exit()
        df['Product ID'] = df['Product ID'].astype(str)

    # Align columns by adding missing columns with None values
    all_columns = set(df1.columns).union(set(df2.columns))
    for df in [df1, df2]:
        for col in all_columns:
            if col not in df.columns:
                df[col] = None

    # Merge data and handle missing descriptions
    combined_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates(subset='Product ID')
    if 'Description' in combined_df.columns:
        combined_df['Description'] = combined_df['Description'].fillna("N/A")

    # Debugging: Print the shape and head of combined_df
    print(f"Combined DataFrame shape: {combined_df.shape}")
    print(combined_df.head())

    return combined_df


# Load data and retrieve unique categories
combined_df = load_data()
if 'Category' not in combined_df.columns:
    print("Error: 'Category' column not found in combined DataFrame.")
    exit()

categories = combined_df['Category'].dropna().unique().tolist()
print(f"Unique categories: {categories}")

# Routes
@app.route('/')
def index():
    # Render homepage with category options
    return render_template('index.html', categories=categories)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Retrieve selected categories from the form
    selected_categories = request.form.getlist('categories')
    print(f"Selected categories: {selected_categories}")  # Debugging: Print selected categories

    # Filter items based on selected categories, default to all if none selected
    filtered_data = (
        combined_df[combined_df['Category'].isin(selected_categories)]
        if selected_categories else combined_df
    )

    # Convert filtered data to a dictionary for rendering
    toys = filtered_data.to_dict(orient='records')

    # Debugging: Print number of toys returned and a sample of the data
    print(f"Number of toys returned: {len(toys)}")
    print(toys[:5])  # Print first 5 toys for inspection
    

    return render_template('recommendations.html', toys=toys)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)