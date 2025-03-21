import pandas as pd

def convert_name_format(full_name):
    """
    Converts a name from 'First Name (Middle ...) Last Name' format to 'Last Name (including any middle parts), First Name'.
    The first token is considered the first name, and all remaining tokens form the last name.
    """
    parts = full_name.strip().split()
    if len(parts) < 2:
        # If there's only one part, return as is
        return full_name
    first_name = parts[0]
    last_name = " ".join(parts[1:])
    return f"{last_name}, {first_name}"

# Load the CSV file
input_csv = 'Fellowships.csv'
df = pd.read_csv(input_csv)

# Check if the 'Full Name' column exists
if 'Full Name' in df.columns:
    # Apply the conversion to each name in the column
    df['Full Name'] = df['Full Name'].apply(convert_name_format)
    
    # Write the updated DataFrame to a new CSV file
    output_csv = 'Fellowships_updated.csv'
    df.to_csv(output_csv, index=False)
    print(f"Converted names have been saved to {output_csv}")
else:
    print("The 'Full Name' column was not found in the CSV.")
