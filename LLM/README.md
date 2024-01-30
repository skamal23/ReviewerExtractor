# NASA_Internship_ADS_Summarization
Summarization model for ADS_search program developed in tandem with NASA HQ and other interns during Fall 2023

**Purpose:** This repository is the result of my Fall 2023 Internship with NASA HQ. The goal was the enhance tools that have been created by previous interns that will enable NASA Headquarters Astrophysics Program Scientists to identify the expertise of potential peer reviewers based on their publication history through the NASA ADS archive. 

The goal of creating this expertise finder is to use the tool to find possible reviewers at underserved and small research insitutions that normally do not particpate in the proposal process. Our hope is that by directly reaching out to subject matter experts at these insitutions, we can divserify the overall pool of applicants to NASA Astrophysics funds in the future. 

This code represents an enhanced version of Expertise Finder v2.0, developed by Mallory Helfenbein (https://github.com/MalloryHelfenbein/NASA_Internship) and Máire Volz (https://github.com/maireav/NASA-Internship). The results of Expertise Finder v2.0 must be used for this code to function properly.

The purpose of enhancing the expertise finder is to reduce the potential of missing vital information regarding authors areas of expertise. By summarizing the entirity of published papers, and combining that information for a given author, the user can develop a more in depth underestanding of their expertise, that may have been missed by reviewing only the abstracts. 

The LLM and Pre-trained model used for summarization purposes https://huggingface.co/pszemraj/led-large-book-summary

Dataset used for training https://huggingface.co/datasets/kmfoda/booksum

**What this code does:** The main function of this code is to summarize arXiv published papers via the results of Expertise Finder v2.0. From there, the final dataframe includes the original n-grams, bi-grams and tri-grams associated with the abstracts, along with the concated summaries, and the summary n-grams, bi-grams and tri-grams. The program accesses arXiv, and huggingface where a pre-trained model is pulled from. The huggingface model is currently open-source and does not require a huggingface API token. The user is able to run this code to develop a deeper understanding of authors areas of expertise for the purpose of reviewing grant and funding proposals. 

**What the User Needs:** The user needs to access Expertise Finder v2.0 (https://github.com/MalloryHelfenbein/NASA_Internship) and follow the README files instructions. 

**Current Files**
- TextAnalysis.py: Python file with functions that determine top n-grams, bi-grams and tri-grams for each authors publication history. This finds the frequency of the appearance of the words in a given set of text. 
- stopwords.txt: Text file with a list of stop words for language processing, so that common everyday words aren't included in the results of the TextAnalysis functions. Several words were added to this file following the work of Helfenbein et al. 2023, to account for common words appearing in the summarization model results. 
- ADS_Summarization.ipynb: A notebook that contains the steps and instructions for the summarization process. 

**Warnings, Notes, and Recommendations:** The code should be run on a GPU runtime, otherwise the runtime will drastically increase, and potentially crash on CPU. It is recommended that the user processes under 100 papers per summarization run, due to extended runtime and GPU limits. 100 papers would take a user approximately 1-2 hours to run fully, depending on GPU capabilities. 
