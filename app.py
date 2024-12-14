import pandas as pd
import streamlit as st

# Load datasets
try:
    drug1 = pd.read_csv('drug1.csv')
    drug2 = pd.read_csv('drug2.csv')
    interaction_data = pd.read_csv('interaction_data.csv')

    # Print a preview of each dataset for verification
    print("Drug1 Dataset:")
    print(drug1.head())
    
    print("\nDrug2 Dataset:")
    print(drug2.head())
    
    print("\nInteraction Data Dataset:")
    print(interaction_data.head())
except Exception as e:
    print(f"Error loading datasets: {e}")
    raise

# Ensure column names are stripped of extra spaces
drug1.columns = drug1.columns.str.strip()
drug2.columns = drug2.columns.str.strip()
interaction_data.columns = interaction_data.columns.str.strip()

# Check if required columns exist
required_columns = {'drug1_id', 'drug2_id', 'Interaction Description'}
for col in required_columns:
    if col not in interaction_data.columns:
        raise KeyError(f"Required column '{col}' not found in interaction_data.")

if 'drug1_id' not in drug1.columns:
    raise KeyError("Required column 'drug1_id' not found in drug1.")
if 'drug2_id' not in drug2.columns:
    raise KeyError("Required column 'drug2_id' not found in drug2.")

# Merge the datasets for a unified view
interaction_data = interaction_data.merge(drug1, on='drug1_id', how='left', suffixes=('', '_drug1'))
interaction_data = interaction_data.merge(drug2, on='drug2_id', how='left', suffixes=('', '_drug2'))

# Display merged dataset for debugging
print("\nMerged Dataset:")
print(interaction_data.head())

# Rename columns for easier use in Streamlit
interaction_data.rename(columns={
    'drug1_name': 'Drug1 Name',
    'drug2_name': 'Drug2 Name',
    'Interaction Description': 'Description'
}, inplace=True)

# Streamlit UI
st.title("Drug Interaction Predictor")

# Dropdown menus for selecting drugs
drug1_options = drug1['drug1_name'].dropna().unique()
drug2_options = drug2['drug2_name'].dropna().unique()

selected_drug1 = st.selectbox("Select Drug 1", drug1_options)
selected_drug2 = st.selectbox("Select Drug 2", drug2_options)

# Filter interactions based on selected drugs
if st.button("Predict Interaction"):
    results = interaction_data[
        (interaction_data['Drug1 Name'] == selected_drug1) &
        (interaction_data['Drug2 Name'] == selected_drug2)
    ]

    if not results.empty:
        st.write(f"**Interactions between {selected_drug1} and {selected_drug2}:**")
        for description in results['Description']:
            st.write(f"- {description}")
    else:
        st.write(f"No interactions found between {selected_drug1} and {selected_drug2}.")
