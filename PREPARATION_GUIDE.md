# Student Registration System: Preparation & Learning Guide

Welcome! If you are a beginner looking to understand, build, or explain this project, this guide covers all the core concepts, Python modules, and tools used in this codebase.

---

## Table of Contents
1. [Prerequisites & Installation](#1-prerequisites--installation)
2. [Streamlit UI Concepts](#2-streamlit-ui-concepts)
3. [MongoDB & PyMongo Operations](#3-mongodb--pymongo-operations)
4. [Data Management with Pandas](#4-data-management-with-pandas)
5. [Analytics Visualizations with Plotly](#5-analytics-visualizations-with-plotly)
6. [File System Operations in Python](#6-file-system-operations-in-python)
7. [Basic Data Validation](#7-basic-data-validation)

---

## 1. Prerequisites & Installation

To run this project, you need:
1. **Python** (version 3.8 or newer).
2. **MongoDB Community Edition** (installed and running locally on port `27017`).
3. **External Libraries**: Installed via pip:
   ```bash
   pip install streamlit pandas plotly Pillow pymongo
   ```
---

## 2. Streamlit UI Concepts

Streamlit is a Python framework that lets you build web applications by writing pure Python code.

### A. Input Widgets
These widgets capture user input and return values:
* `st.text_input("Label")`: Captures single-line strings.
* `st.text_area("Label")`: Captures multi-line strings (useful for addresses).
* `st.selectbox("Label", options=[...])`: Creates dropdown lists.
* `st.radio("Label", options=[...])`: Renders mutually exclusive radio buttons.
* `st.checkbox("Label")`: Returns a boolean (`True`/`False`) representing checked status.
* `st.date_input("Label")`: Displays an interactive calendar input.
* `st.file_uploader("Label", type=[...])`: Accepts uploaded files (e.g. image bytes).

### B. Layouts & Structure
To place widgets side-by-side or inside visual blocks:
* **Columns**:
  ```python
  col_left, col_right = st.columns(2)
  name = col_left.text_input("Name")
  email = col_right.text_input("Email")
  ```
* **Containers with Borders**: Renders a card-like bounding box around components.
  ```python
  with st.container(border=True):
      st.write("Inside a card wrapper!")
  ```

### C. Session State & Navigation
Streamlit re-runs the entire python script from top to bottom whenever a user interacts with a widget. To preserve variables across these runs (like the active menu tab or successful registration flags), we use **Session State**:
```python
# Initialize state
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Read/write state
st.session_state.current_page = "📝 Registration"

# Force Streamlit to immediately re-run the page to reflect updates
st.rerun()
```

---

## 3. MongoDB & PyMongo Operations

MongoDB is a **NoSQL Database** that stores records as documents (which look exactly like Python dictionaries) instead of tables with rows and columns.

### A. Connecting to MongoDB
We use `pymongo` to connect to our local server:
```python
import pymongo

# Connect to local database server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select database name
db = client["student_db"]

# Select collection name (equivalent to SQL table)
collection = db["students"]
```

### B. MongoDB CRUD (Create, Read, Update, Delete)
* **Create (Insert)**:
  ```python
  student = {"name": "Alice", "course": "Python"}
  result = collection.insert_one(student)
  new_id = str(result.inserted_id) # Unique 24-character ID
  ```
* **Read (Query)**:
  ```python
  # Fetch all documents
  all_docs = collection.find()
  
  # Fetch one document matching criteria
  one_doc = collection.find_one({"name": "Alice"})
  ```
* **Update**:
  ```python
  from bson.objectid import ObjectId
  
  # Update matching document
  collection.update_one(
      {"_id": ObjectId("60d5ec... ")}, 
      {"$set": {"course": "Django"}}
  )
  ```
* **Delete**:
  ```python
  collection.delete_one({"_id": ObjectId("60d5ec... ")})
  ```
* **Search with Regular Expressions (Regex)**:
  Used to perform partial searches (e.g. matching any name containing "ali", case-insensitive):
  ```python
  collection.find({"name": {"$regex": "ali", "$options": "i"}})
  ```

---

## 4. Data Management with Pandas

Pandas is used to format, filter, and aggregate query records.

### A. Creating DataFrames
A `DataFrame` is a tabular representation of data. We can convert a list of dictionaries (from MongoDB) directly into a DataFrame:
```python
import pandas as pd

students = [
    {"name": "Alice", "course": "Python"},
    {"name": "Bob", "course": "Data Science"}
]
df = pd.DataFrame(students)
```

### B. Cleaning & Filtering
* **Dropping Columns**: We drop MongoDB's binary `_id` column to prevent errors when charting:
  ```python
  df = df.drop(columns=["_id"])
  ```
* **Matching Criteria**:
  ```python
  # Count records created today
  today_records = df[df["created_date"] == "2026-07-27"]
  ```

---

## 5. Analytics Visualizations with Plotly

Plotly Express makes it easy to generate interactive web graphs from a Pandas DataFrame.

### A. Pie Chart (Distribution)
Used to show percentages (e.g., student distributions by course):
```python
import plotly.express as px

course_counts = df["course"].value_counts().reset_index()
fig = px.pie(course_counts, names="course", values="count")
st.plotly_chart(fig)
```

### B. Line Chart (Trends)
Used to show changes over time:
```python
# Group by date and count registrations
trend_df = df.groupby("created_date").size().reset_index(name="Registrations")
fig = px.line(trend_df, x="created_date", y="Registrations")
st.plotly_chart(fig)
```

---

## 6. File System Operations in Python

We save uploaded Aadhaar files directly onto the server's local storage.

### A. Creating Folders
Ensure target folders exist without crashing if they are already present:
```python
import os
os.makedirs("uploads/front", exist_ok=True)
```

### B. Writing Uploaded Files
`st.file_uploader` returns a buffer of bytes. We write this buffer into a file on disk:
```python
# Read the buffer and write binary ("wb")
with open("uploads/front/my_file.png", "wb") as f:
    f.write(uploaded_file.getbuffer())
```

---

## 7. Basic Data Validation

We run data checks before saving records to MongoDB:
* **String Cleaning**:
  * `.strip()`: Removes leading and trailing spaces.
  * `.replace("-", "")`: Removes hyphens from phone numbers.
* **Digit Check**:
  * `.isdigit()`: Checks if string contains only numerical characters.
* **Email check**:
  * Check if `"@"` and `"."` are present inside the text string.
