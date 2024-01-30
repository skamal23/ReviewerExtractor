# Reviewer Extractor

This **Reviewer Extractor** code is from my Fall 2023 NASA internship: Expanding Diversity in the NASA Astrophysics Panel.

## What it does

The Reviewer Extractor allows the user to search through the Expertise Finder (version 2) outputs. It is typically a csv file (one is included in this repository) or the user can upload their own. The GUI filters the input dataframe and displays only raws that include the searched "words" under the specified column. The user can then save this filtered dataframe into a file directly to their computer.

The code will allow the user to search for words in the following columns:
- Input Author
- Input Institution
- Bibcode
- Abstract
- Panels

While the repository contains a test file, if you choose to use a custom csv file, it **MUST** contain **ALL** the columns listed above (even if the column is empty), in order to propoerl display and properly search.

## What is required
### Imports

- pandas (1.5.3 or later)
- tkinter 
- tkinter.messagebox

### Files needed:
- preloaded csv file

Place this file within the same directory, as the path will be necessary in order for the code to function correctly.

## How to use it

The user can either use the csv file already referenced within the code or click on the `load csv file` button. Once a csv file to search has been established, the user can input
text into the search bar. Afterwards, they are to select which column to search (remember: the file must contain the column name that the user wants to search in). Finally, select 
the `search` button. Columns that contain the input will be displayed in a dataframe within the tkinter window. The user can then choose to save this filtered dataframe by selecting
`Save CSV` button, which will then prompt a popup window to appear, asking the user to name the csv file and selecting a destination on where it can be saved. 

