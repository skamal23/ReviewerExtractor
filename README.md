# ReviewerExtractor
This repository contains the main code for the Reviewer Extractor (Volz et al., in prep).<br>
**Purpose** 
The Reviewer Extractor is a tool that is designed to help NASA Headquarters Astrophysics Program Scientists to 

- Collect data on institutional demographics of researchers across many type of affiliations through the NASA ADS archive based on their publication record
- Identify suitable peer reviews participants based on their derived expertise

Using these tools we tried to reach out to possible reviewers from institutions that normally do not participate, 
and hopefully expand the pool of applicants to NASA Astrophysics. 

The code represents a version 2.0 of a previous work done by Máire Volz see [Gihub repository](https://github.com/maireav/NASA-Internship). <br \>
In the examples, we provide a method of finding experts in specific matters independent from their institutions. Additionally, we show a method that provides specific inromation on researchers at MSIs (Minority Serving Institutions) that have published in Astronomy-focused journals. 

**What the code does:** 
The main aspect is the notebook called "ADS_search.ipynb". The main function can be called in different ways (see examples), but the general idea is to identify researchers with specific expertise, identified by their past publications (refereed or not). 

"Under the hood", this program accesses ADS through the ADS specific API and searches for the specific data according to the user's inputs (some are mandatory and some are optional). The output is a .csv file with all the information collected via the API('First Author', 'Bibcode', 'Title', 'Publication Date', 'Keywords', 'Affiliations', and 'Abstract') and the N-grams created by our code, for visual inspection by the user. The user can then easily determine the expertise of each author ADS returned. 

**What the User needs:**
The user needs an ADS API Access Token (can be found here:  https://ui.adsabs.harvard.edu/help/api/), which searches the input into ADS. Other libraries needed include: nltk and pandas version 1.5. 


**Current files:**
Some files are needed to run the actual search, while others are utilized in post-processing and expertise identification (e.g. N-grams creation): 
- ADSsearcherpkg: Python file that has all of the functions used to find the expertises of the authors and produce an organized data frame with each row being an individual author and columns: 'Input Author','Input Institution', 'First Author', 'Bibcode', 'Title', 'Publication Date', 'Keywords', 'Affiliations', 'Abstract', 'Data Type'
- TextAnalysis.py: Python file that has all the functions in order to determine the top words, bigrams and trigrams in each publication.
- stopwords.txt: Text file that has a list of the stop words for language processing. 
- ADS_search.ipynb: A notebook that contains the different examples of how to use the ADSsearcherpkg functions with different input cases. These input cases include just an author, just an institution, and a csv file of 3 authors with their corresponding institutions.
# History
The routines, snippets, and main code were developed by NASA Headquarters interns in the 2022-2023 internship period: 
* The version 1 (codeV1 directory) was developed by Máire Volz during her internship at NASA HQ in 2022-2023. 
* The version 2 (codeV2 directory) is the **most up-to-date** version of the code and it is the **only one** that will be maintained. It was developed by Mallory Helfenbein (NASA HQ intern 2023).
* The LLM summarization model (LLM directory) was developed by Isabelle Hoare (NASA HQ intern 2023)
* The GUIs were developed by Kaniyah Harris (NASA HQ intern 2023).

# Code requirements
# Code citation
# Contact information
Antonino Cucchiara, PhD.  
NASA HQ  
Email: antonino.cucchiara@nasa.gov
