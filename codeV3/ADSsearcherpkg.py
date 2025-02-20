import requests
from urllib.parse import urlencode
import numpy as np
import TextAnalysis as TA
import itertools
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from LlamaModelV2 import generate_expertise, get_groq, string_to_list


import pandas as pd


def do_search(auth_name, inst, t, q):
    results = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?{}".format(q),
        headers={'Authorization': 'Bearer ' + t}
    )
    data = results.json()["response"]["docs"]
    pdates = [d['pubdate'] for d in data]
    affiliations = [d['aff'][0] for d in data]
    bibcodes = [d['bibcode'] for d in data]
    f_auth = [d['first_author'] for d in data]
    keysw = [d.get('keyword', []) for d in data]
    titles = [d.get('title', '') for d in data]
    abstracts = [d.get('abstract', '') for d in data]
    ids = [d.get('identifier', []) for d in data]

    df = pd.DataFrame({
        'Input Author': [auth_name] * len(data),
        'Input Institution': [inst] * len(data),
        'First Author': f_auth,
        'Bibcode': bibcodes,
        'Title': titles,
        'Publication Date': pdates,
        'Keywords': keysw,
        'Affiliations': affiliations,
        'Abstract': abstracts,
        'Identifier': ids,
        'Data Type': ['']*len(data)
    })

    if auth_name is None:
        df['Input Author'] = f_auth
    return df

def format_year(year):
    if isinstance(year, (int, np.integer)):
        startd = str(year - 1)
        endd = str(year + 4)
        return f'[{startd} TO {endd}]'
    elif isinstance(year, float):
        year = int(year)
        startd = str(year - 1)
        endd = str(year + 4)
        return f'[{startd} TO {endd}]'
    elif isinstance(year, str):
        if len(year) == 4:
            startd = str(int(year) - 1)
            endd = str(int(year) + 4)
            return f'[{startd} TO {endd}]'
        elif year.startswith("[") and year.endswith("]") and " TO " in year:
            return year  # Return the string as is if it's a year range
        else:
            return year
    else:
        raise ValueError("Year must be an integer, float, or a string representing a year or a year range.")

def ads_search(name=None, institution=None, year=None, refereed='property:notrefereed OR property:refereed', \
               token=None, stop_dir=None, second_auth=False,groq_analysis=True):
    
    final_df = pd.DataFrame()
    query_parts = []
    if name:
        if second_auth:
            query_parts.append(f'(pos(author:"^{name}",1) OR pos(author:"{name}",2))')
        else:
            query_parts.append(f'author:"^{name}"')
    if institution:
        query_parts.append(f'pos(institution:"{institution}",1)')
    if year:
        years = format_year(year)
        query_parts.append(f'pubdate:{years}')

    if not query_parts:
        print("You did not give me enough to search on, please try again.")
        return final_df
    
    query = " AND ".join(query_parts)
    print(f"I will search for papers matching the following criteria:\n{query}\n")

    encoded_query = urlencode({
        "q": query,
        "fl": "title, first_author, bibcode, abstract, aff, pubdate, keyword, identifier",
        "fq": "database:astronomy," + str(refereed),
        "rows": 3000,
        "sort": "date desc"
    })

    try:
        print('I am now querying ADS.\n')
        results = requests.get(
            "https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query),
            headers={'Authorization': 'Bearer ' + token}
        )
        data = results.json()["response"]["docs"]
    except:
        print('Oops, something went wrong.\n')

    df = do_search(name, institution, token, encoded_query)

    # Try affiliation instead of institution if the DataFrame is empty
    if df.empty:
        print('DataFrame is empty! Trying affiliation instead of institution.')
        if institution:
            query_parts = [f'pos(aff:"{institution}",1)']
            if year:
                query_parts.append(f'pubdate:{years}')
            alt_query = " AND ".join(query_parts)
            print(f"Trying alternative search: {alt_query}")
            encoded_query = urlencode({
                "q": query,
                "fl": "title, first_author, bibcode, abstract, aff, pubdate, keyword,identifier",
                "fq": "database:astronomy," + str(refereed),
                "rows": 3000,
                "sort": "date desc"
            })
            df = do_search(name, institution, token, encoded_query)

    # Run further analysis if the DataFrame is not empty
    if not df.empty:
        data2 = merge(df)
        data3 = data_type(data2)
        data4 = n_grams(data3, stop_dir)
        if groq_analysis:
            print("Running Groq subtopics analysis on ADS results...")
            data4 = generate_expertise(data4, groq_client=get_groq())
            print("Groq analysis complete.")
        return data4
    else:
        print("No results found.")
        dummy_data = {
            'Input Author': name if name else "None",
            'Input Institution': institution if institution else "None",
            'First Author': "None",
            'Bibcode': "None",
            'Title': "None",
            'Publication Date': "None",
            'Keywords': "None",
            'Affiliations': "None",
            'Abstract': "None",
            'Identifier': "None",
            'Data Type': "None",
            'Top 10 Words': "None",
            'Top 10 Bigrams': "None",
            'Top 10 Trigrams': "None"
        }
        return pd.DataFrame([dummy_data])


def data_type(df):
    journals = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE', 'A&A', 'zndo','yCat','APh', 'PhRvL']
    df['Data Type'] = ''
    for index, row in df.iterrows():
        bibcodes_str = row['Bibcode']
        bibcodes = bibcodes_str.split(', ')
        total_papers = len(bibcodes)
        clean_count = sum(any(journal in bibcode for journal in journals) for bibcode in bibcodes)
        if clean_count >= total_papers / 2:
            data_type_label = 'Clean'
        else:
            data_type_label = 'Dirty'
        df.at[index, 'Data Type'] = data_type_label
    return df
        
def merge(df):
    df['Publication Date'] = df['Publication Date'].astype(str)
    df['Abstract'] = df['Abstract'].astype(str)
    df['Keywords'] = df['Keywords'].apply(lambda keywords: keywords if keywords else []) # <- Fix for Keywords
    df['Title'] = df['Title'].apply(lambda titles: titles if titles else []) 
    df['Identifier'] = df['Identifier'].apply(lambda ids: ids if ids else []) 
    df.fillna('None', inplace=True)

    merged = df.groupby('Input Author').aggregate({'Input Institution': ', '.join,
                                                 'First Author': ', '.join,
                                                 'Bibcode': ', '.join,
                                                 'Title': lambda x: list(itertools.chain.from_iterable(x)), 
                                                 'Publication Date': ', '.join,
                                                 'Keywords': lambda x: list(itertools.chain.from_iterable(x)), # <- Fix for Keywords
                                                 'Affiliations': ', '.join,
                                                 'Abstract': ', '.join,
                                                 'Data Type': ', '.join,
                                                 'Identifier': lambda x: list(itertools.chain.from_iterable(x))  
                                                 }).reset_index()
    return merged

def n_grams(df, directorypath):
    top10Dict = {'Top 10 Words': [],
                 'Top 10 Bigrams': [],
                 'Top 10 Trigrams': []}

    for i in df.values:
        abstracts = i[8]
        top10words = TA.topwords(abstracts, directorypath)
        top10bigrams = TA.topbigrams(abstracts, directorypath)
        top10trigrams = [( " ".join(trigram), count) for trigram, count in list(TA.toptrigrams(abstracts, directorypath))]
        top10bigrams = [( " ".join(bigram), count) for bigram, count in list(TA.topbigrams(abstracts, directorypath))]
        top10Dict['Top 10 Words'].append(top10words)
        top10Dict['Top 10 Bigrams'].append(top10bigrams)
        top10Dict['Top 10 Trigrams'].append(top10trigrams)

    top10Df = df
    top10Df['Top 10 Words'] = top10Dict['Top 10 Words']
    top10Df['Top 10 Bigrams'] = top10Dict['Top 10 Bigrams']
    top10Df['Top 10 Trigrams'] = top10Dict['Top 10 Trigrams']

    top10Df = top10Df[['Input Author', 'Input Institution', 'First Author', 'Bibcode', 'Title', 'Publication Date',
                       'Keywords', 'Affiliations', 'Abstract', 'Identifier', 'Top 10 Words', 'Top 10 Bigrams',
                       'Top 10 Trigrams', 'Data Type']]
    return top10Df


def get_user_input(dataframe):
    """
    Gets user input for searching a dataframe, compatible with Jupyter notebooks.
    
    Args:
        dataframe: pandas DataFrame containing the data to search
        
    Returns:
        dict: Dictionary containing search parameters and search type
    """
    
    available_search_types = {
        "name": "Name Search - search by author name",
        "institution": "Institution Search - search by institution",
        "fellow": "Fellow Search - search by name, institution, and year"
    }
    
    print("\nWhat type of search do you want to conduct?")
    for key, description in available_search_types.items():
        print(f"-Enter '{key}' for {description}")
    

    # Get search type
    while True:
        try:
            search_type = input("\nEnter search type: ('name', 'institution', or 'fellow'):\n").lower()
            if search_type in available_search_types:
                break
            print("Invalid search type. Please enter 'name', 'institution', or 'fellow'.")
        except NameError:
            print("Error getting input. Please try again.")
    
    print(f"You are running '{search_type}' search.\n")


    print("Listed are the available columns from your dataset:", ", ".join(dataframe.columns))
    # Get relevant column names based on search type
    search_params = {'search_type': search_type}
    
    if search_type == 'name':
        name_input = input("Enter the name of the column that contains the data for 'name' search: ").strip()
        if name_input:
            matching_columns = [col for col in dataframe.columns if col.lower() == name_input.lower()]
            search_params['name_column'] = matching_columns[0] if matching_columns else "Name"
        else:
            search_params['name_column'] = "Name"
        search_params['year_range'] = '[2003 TO 2030]'

        # Second author search
        while True:
            include_second = input("Do you want to include search by second author? (y/n) [n]: ").strip().lower() or "n"
            if include_second in ["y", "n"]:
                break
            print("Invalid choice. Please enter 'y' for yes or 'n' for no.")
        search_params['second_author'] = (include_second == "y")
        
    elif search_type == 'institution':
        inst_input = input("Enter the name of the column that contains the data for 'institution' search: ").strip()
        if inst_input:
            matching_columns = [col for col in dataframe.columns if col.lower() == inst_input.lower()]
            search_params['institution_column'] = matching_columns[0] if matching_columns else "Institution"
        else:
            search_params['institution_column'] = "Institution"
        search_params['year_range'] = '[2003 TO 2030]'
    
    elif search_type == 'fellow':
        name_input = input("Enter the name of the column that contains the data for 'name' search [Name]: ").strip()
        inst_input = input("Enter the name of the column that contains the data for 'institution' search [Institution]: ").strip()
        year_input = input("Enter the name of the column that contains the data for 'year' search [Fellowship Year]: ").strip()
        if name_input:
            matching_name = [col for col in dataframe.columns if col.lower() == name_input.lower()]
            search_params['name_column'] = matching_name[0] if matching_name else "Name"
        else:
            search_params['name_column'] = "Name"

        if inst_input:
            matching_inst = [col for col in dataframe.columns if col.lower() == inst_input.lower()]
            search_params['institution_column'] = matching_inst[0] if matching_inst else "Institution"
        else:
            search_params['institution_column'] = "Institution"

        if year_input:
            matching_year = [col for col in dataframe.columns if col.lower() == year_input.lower()]
            search_params['year_column'] = matching_year[0] if matching_year else "Fellowship Year"
        else:
            search_params['year_column'] = "Fellowship Year"
    run_groq = input("Do you want to run Groq subtopics analysis on the ADS results? (y/n) [n]: ").strip().lower() or "n"
    search_params['groq_analysis'] = (run_groq == "y")
    return search_params

def run_file_search(filename, token, stop_dir):
    """
    Runs search based on user's choice of search type.

    Args:
        filename (str): Path to the input CSV file
        token (str): ADS API token
        stop_dir (str): Path to stopwords file

    Returns:
        pandas.DataFrame: Search results
    """
    dataframe = pd.read_csv(filename)
    final_df = pd.DataFrame()
    count = 0

    # Get user's search preferences
    search_params = get_user_input(dataframe)
    print("Searching for results...")
    search_type = search_params['search_type']

    for i in range(len(dataframe)):
        if search_type == 'name':
            # Name-only search
            name = dataframe[search_params['name_column']][i]
            second_auth = search_params.get('second_author', False)
            data1 = ads_search(
                name=name,
                institution=None,
                year=search_params['year_range'],
                token=token,
                stop_dir=stop_dir,
                second_auth=second_auth,
                groq_analysis=False
            )
            search_identifier = f"name: {name} (including {'second' if second_auth else 'only first'} author)"

        elif search_type == 'institution':
            # Institution-only search
            institution = dataframe[search_params['institution_column']][i]
            data1 = ads_search(
                name=None,
                institution=institution,
                year=search_params['year_range'],
                token=token,
                stop_dir=stop_dir,
                second_auth=second_auth,
                groq_analysis=False
            )
            data1['Input Institution'] = institution
            search_identifier = f"institution: {institution}"

        elif search_type == 'fellow':
            # Fellow search (name + institution + year)
            name = dataframe[search_params['name_column']][i]
            institution = dataframe[search_params['institution_column']][i]
            year = str(int(dataframe[search_params['year_column']][i]))
            
            data1 = ads_search(
                name=name,
                institution=institution,
                year=year,
                token=token,
                stop_dir=stop_dir,
                second_auth=second_auth,
                groq_analysis=False
            )
            data1['Input Institution'] = institution
            search_identifier = f"fellow: {name} at {institution} in {year}"

        # Process results if found
        if not data1.empty:
            data2 = merge(data1)
            data3 = data_type(data2)
            data4 = n_grams(data3, stop_dir)
            final_df = pd.concat([final_df, data4], ignore_index=True)
            count += 1
            print(f"Completed {count} searches - Processed {search_identifier}")
        else:
            print(f"No results found for {search_identifier}")
        
    if search_params.get('groq_analysis', False) and not final_df.empty:
        print("Running Groq subtopics analysis on aggregated ADS results...")
        final_df = generate_expertise(final_df, groq_client=get_groq())
        print("Groq analysis complete.")
    return final_df

