import pandas as pd

# Load the Excel file
file_path = 'restoran.xlsx'
try:
    data = pd.read_excel(file_path)

    # Display the content of the Excel file
    print("Contents of the Excel file:")
    print(data)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")