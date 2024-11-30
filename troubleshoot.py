from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data once at startup
try:
    df1 = pd.read_csv('data/inventory.csv')
    df2 = pd.read_csv('data/toy-inventory.csv')
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()  # Stop if either CSV is missing

# Ensure 'Product ID' column is of the same type in both dataframes (string/object)
df1['Product ID'] = df1['Product ID'].astype(str)
df2['Product ID'] = df2['Product ID'].astype(str)

print("Columns in df1:", df1.columns)
print("Columns in df2:", df2.columns)
