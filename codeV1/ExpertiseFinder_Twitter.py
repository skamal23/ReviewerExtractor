import pandas as pd
import ads
import requests
from TextAnalysis import *
from cleantext import clean

###################################################################################################################################################################################################################################################################################################################################################################################################

def twitterDataFinder(token, directorypath, rawData, start, count):
    '''
    This function combines the functionality of expertiseFinderTwitter() and dirtycleaner_moreStrict_Twitter() with an additional step: in addition to finding the top 10 words, bigrams, and trigrams for NASA ADS resutls, the return data frame of this function includes the top words, bigrams, and trigrams for each person's twitter bio.
    
    token: Your ADS token
    directorypath: The location of the stopwords file "stopwords.txt"
    rawData: The original data frame 
    start: The index at which to begin analyzing data
    count: How many indecies after "start" to stop analyzing data
    '''    
    # STEP 1: Create a new data frame with a column containing 'LastName, FirstName' data. 
    withNamesDf = cleanTwitterData(rawData)
    withNamesDf.drop(withNamesDf[withNamesDf['LastName, FirstName'] == 'NaN'].index, inplace = True)
    withNamesDf = withNamesDf.reset_index(drop = True)
    
    # STEP 2: Create n-gram columns on Twitter bio text.
    withNGramsDf = twitterNGrams(withNamesDf, directorypath)
    
    # STEP 3: Find the NASA ADS papers for each author.
    top10df, top10dirty = expertiseFinderTwitter(token, directorypath, withNGramsDf, start, count)
    
    # STEP 4: Make three new data frames--one that contains all of the names that have ONLY DIRTY data from Step 3 (dirtyDf), one that contains all of the names that have CLEAN data from Step 3 (cleanDf), and one that contains all of the names that have NO data from Step 3 (missingDf).
    dirtyDf, cleanDf, missingDf = dirtyCleaner_moreStrict_Twitter(top10dirty, top10df, withNGramsDf[start:start+count])
    
    # STEP 5: Combine the clean and dirty and missing data from Step 4, creating a 'Data Type' column. Also combine Twitter n-gram data and the NASA ADS n-gram data
    twitterADS_cleanDf = withNGramsDf[start:start+count]
    
    twitterADS_cleanDf['First Author'] = ""
    twitterADS_cleanDf['Bibcode'] = ""
    twitterADS_cleanDf['Title'] = ""
    twitterADS_cleanDf['Year'] = ""
    twitterADS_cleanDf['Keywords'] = ""
    twitterADS_cleanDf['Affiliations'] = ""
    twitterADS_cleanDf['Abstract'] = ""
    twitterADS_cleanDf['ADS Top Words'] = ""
    twitterADS_cleanDf['ADS Top Bigrams'] = ""
    twitterADS_cleanDf['ADS Top Trigrams'] = ""
    twitterADS_cleanDf['Data Type'] = ""
    
    twitterADS_cleanDf = twitterADS_cleanDf.reset_index(drop = True)
    
    for i in range(len(twitterADS_cleanDf['LastName, FirstName'])):
        name1 = twitterADS_cleanDf['LastName, FirstName'][i]

        for j in range(len(cleanDf['True Author'])):
            name2 = cleanDf['True Author'][j]
            firstauth2 = cleanDf['First Author'][j]
            bib2 = cleanDf['Bibcode'][j]
            tit2 = cleanDf['Title'][j]
            year2 = cleanDf['Year'][j]
            keyw2 = cleanDf['Keywords'][j]
            aff2 = cleanDf['Affiliations'][j]
            abs2 = cleanDf['Abstract'][j]
            topw2 = cleanDf['Top 10 Words'][j]
            topb2 = cleanDf['Top 10 Bigrams'][j]
            topt2 = cleanDf['Top 10 Trigrams'][j]

            if name1 == name2:
                twitterADS_cleanDf.at[i, 'First Author'] = firstauth2
                twitterADS_cleanDf.at[i, 'Bibcode'] = bib2
                twitterADS_cleanDf.at[i, 'Title'] = tit2
                twitterADS_cleanDf.at[i, 'Year']  = year2
                twitterADS_cleanDf.at[i, 'Keywords'] = keyw2
                twitterADS_cleanDf.at[i, 'Affiliations']  = aff2
                twitterADS_cleanDf.at[i, 'Abstract'] = abs2
                twitterADS_cleanDf.at[i, 'ADS Top Words'] = topw2
                twitterADS_cleanDf.at[i, 'ADS Top Bigrams'] = topb2
                twitterADS_cleanDf.at[i, 'ADS Top Trigrams'] = topt2
                twitterADS_cleanDf.at[i, 'Data Type'] = 'CLEAN'

        for j in range(len(dirtyDf['True Author'])):
            name3 = dirtyDf['True Author'][j]
            firstauth3 = dirtyDf['First Author'][j]
            bib3 = dirtyDf['Bibcode'][j]
            tit3 = dirtyDf['Title'][j]
            year3 = dirtyDf['Year'][j]
            keyw3 = dirtyDf['Keywords'][j]
            aff3 = dirtyDf['Affiliations'][j]
            abs3 = dirtyDf['Abstract'][j]
            topw3 = dirtyDf['Top 10 Words'][j]
            topb3 = dirtyDf['Top 10 Bigrams'][j]
            topt3 = dirtyDf['Top 10 Trigrams'][j]

            if name1 == name3:
                twitterADS_cleanDf.at[i, 'First Author'] = firstauth3
                twitterADS_cleanDf.at[i, 'Bibcode'] = bib3
                twitterADS_cleanDf.at[i, 'Title'] = tit3
                twitterADS_cleanDf.at[i, 'Year']  = year3
                twitterADS_cleanDf.at[i, 'Keywords'] = keyw3
                twitterADS_cleanDf.at[i, 'Affiliations']  = aff3
                twitterADS_cleanDf.at[i, 'Abstract'] = abs3
                twitterADS_cleanDf.at[i, 'ADS Top Words'] = topw3
                twitterADS_cleanDf.at[i, 'ADS Top Bigrams'] = topb3
                twitterADS_cleanDf.at[i, 'ADS Top Trigrams'] = topt3
                twitterADS_cleanDf.at[i, 'Data Type'] = 'DIRTY'

        for j in range(len(missingDf['LastName, FirstName'])):
            name4 = missingDf['LastName, FirstName'][j]

            if name1 == name4:
                twitterADS_cleanDf.at[i, 'Data Type'] = 'MISSING'
                
    # STEP 6: Rearrange and rename columns            
    twitterADS_cleanDf_2 = twitterADS_cleanDf[['Name', 
                                                'LastName, FirstName', 
                                                'IDnum', 
                                                'ScreenName', 
                                                'location', 
                                                'profile_loc',
                                                'URL',
                                                'description', 
                                                'Twitter Top Words', 
                                                'Twitter Top Bigrams', 
                                                'Twitter Top Trigrams', 
                                                'First Author', 
                                                'Bibcode', 
                                                'Title', 
                                                'Year', 
                                                'Keywords', 
                                                'Affiliations', 
                                                'Abstract', 
                                                'ADS Top Words', 
                                                'ADS Top Bigrams', 
                                                'ADS Top Trigrams', 
                                                'Data Type']]

    twitterADS_cleanDf_2.rename(columns = {'IDnum':'ID Number',
                                            'ScreenName':'Screen Name', 
                                            'location':'Location', 
                                            'profile_loc':'Profile Loc', 
                                            'description':'Description', 
                                            'Top Words':'Twitter Top Words', 
                                            'Top Bigrams':'Twitter Top Bigrams', 
                                            'Top Trigrams':'Twitter Top Trigrams'}, inplace = True)
    
    # STEP 7: Return the finished data frame !
    return twitterADS_cleanDf_2

################################################################################################################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################################################################################################################################################

def step12(start, count, rawFile):
    '''
    This function performs steps 1 and 2 for the expertiseFinder.
    '''
     # STEP 1: Import original data file. According to the start and count values taken at Step 0 of this program, in this step, I select only the desired indecies of the data frame.    
    rawDf = rawFile
    
    end = start+count
    rawDf = rawDf[start:end]
    
    # STEP 2: Once the data file is imported, pull out the important data:
    rawNames = list(rawDf['LastName, FirstName'])
    
    return rawNames

################################################################################################################################################################################################################################################################################################################################################################################################

def step3(rawNames):
    '''
    This function performs step 3 for the expertiseFinder. 
    
    The boolean in this function determines if affiliation will be used when searching for ADS papers or not. 
    '''
    # STEP 3: Search ADS API to find queries matching the first author and/or affiliation requirement.  
    queryData = []
    queryNames = []
    
    for i in range(len(rawNames)):
        name = rawNames[i]
        
        queries = ads.SearchQuery(first_author = '^'+name, 
                                  property = 'refereed', 
                                  sort = 'citation_count', 
                                  database = 'astronomy')
        queryData.append(queries)
        queryNames.append(name)
            
    searchQueries = [queryNames, queryData]
    
    return searchQueries

################################################################################################################################################################################################################################################################################################################################################################################################

def step4(searchQueries):
    '''
    This function performs step 4 in the expertiseFinder.
    '''
    # STEP 4: For every query in queryData, I now need to collect every bibcodes from that query's list of associated papers. 
    Bibcodes = []
    Names = []
    for i in range(len(searchQueries[1])):
        query = searchQueries[1][i]
        name = searchQueries[0][i]
        for paper in query:
            Bibcodes.append(paper.bibcode)
            Names.append(name)
            
    return Bibcodes, Names

################################################################################################################################################################################################################################################################################################################################################################################################

def step5(Bibcodes, Names):
    '''
    This function performs step 5 in the expertiseFinder.
    '''
    # STEP 5: In this step, I loop through every entry in the Bibcodes list and use the ads package to find the associated data: ['author', 'bibcode', 'title', 'citation_count', 'year', 'keyword', 'aff', 'abstract']. 
    FirstAuthors = []
    Titles = []
    Years = []
    Keywords = []
    Affs = []
    Abstracts = []
    
    for bib in Bibcodes:
        info = list(ads.SearchQuery(bibcode = bib, fl = ['author', 'bibcode', 'title', 'citation_count', 'year', 'keyword', 'aff', 'abstract']))[0]

        try:
            FirstAuthors.append(info.author[0])
        except:
            FirstAuthors.append('None')

        try:
            Titles.append(info.title[0])
        except:
            Titles.append('None')

        try:
            Years.append(int(info.year))
        except:
            Years.append('None')

        try:
            Affs.append(info.aff[0])
        except:
            Affs.append('None')

        try:
            Keywords.append(info.keyword[0])
        except:
            Keywords.append('None')

        try:
            Abstracts.append(info.abstract)
        except:
            Abstracts.append('None')

    dataDict = {'First Author': FirstAuthors, 
                'True Author': Names, 
                'Bibcode': Bibcodes, 
                'Title': Titles, 
                'Year': Years, 
                'Keywords': Keywords, 
                'Affiliations': Affs, 
                'Abstract': Abstracts}

    paperSearchDf = pd.DataFrame(dataDict)
    
    return paperSearchDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step6_Twitter(paperSearchDf):
    '''
    This function, containing numerous smaller functions, performs step 6 in expertiseFinder.
    '''
    # STEP 6: My next job is to clean up this df by finding First Authors (those listed on the paper pulled from NASA ADS) that match the True Author (the name pulled from the Twitter bio). This step also finds papers with the appropriate Journal Names in the Bibcode. These "clean" data are appended to cleanDict.
    cleanDict = {'First Author':[],
             'True Author': [],
             'Bibcode': [], 
             'Title': [], 
             'Year': [], 
             'Keywords': [], 
             'Affiliations': [], 
             'Abstract': []}

    for row in paperSearchDf.values:
        firstauthor = row[0]
        year = row[4]
        if year < 2002:
            paperSearchDf = paperSearchDf[paperSearchDf['First Author'] != firstauthor]
                
    for row in paperSearchDf.values:
        firstauthor = row[0]
        trueauthor = row[1]
        bibcode = row[2]
        title = row[3]
        year = row[4]
        keywords = row[5]
        affs = row[6]
        abstract = row[7]
        
        trueauthor_tokenized = word_tokenize(trueauthor)
        lastname_initial = trueauthor_tokenized[0] + ', ' + trueauthor_tokenized[2][0] + '.'
        
        winitial = trueauthor + " ?."

        journalNames = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE', 'A&A']
        
        if trueauthor == firstauthor:
            for name in journalNames:
                if name in bibcode:
                    ## print(abstract)
                    cleanDict['First Author'].append(firstauthor)
                    cleanDict['True Author'].append(trueauthor)
                    cleanDict['Bibcode'].append(bibcode)
                    cleanDict['Title'].append(title)
                    cleanDict['Year'].append(year)
                    cleanDict['Keywords'].append(keywords)
                    cleanDict['Affiliations'].append(affs)
                    cleanDict['Abstract'].append(abstract)

                    paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                    
        elif trueauthor in firstauthor:
            for name in journalNames:
                if name in bibcode:
                    ## print(abstract)
                    cleanDict['First Author'].append(firstauthor)
                    cleanDict['True Author'].append(trueauthor)
                    cleanDict['Bibcode'].append(bibcode)
                    cleanDict['Title'].append(title)
                    cleanDict['Year'].append(year)
                    cleanDict['Keywords'].append(keywords)
                    cleanDict['Affiliations'].append(affs)
                    cleanDict['Abstract'].append(abstract)

                    paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                    
        elif lastname_initial == firstauthor:
            for name in journalNames:
                if name in bibcode:
                    ## print(abstract)
                    cleanDict['First Author'].append(firstauthor)
                    cleanDict['True Author'].append(trueauthor)
                    cleanDict['Bibcode'].append(bibcode)
                    cleanDict['Title'].append(title)
                    cleanDict['Year'].append(year)
                    cleanDict['Keywords'].append(keywords)
                    cleanDict['Affiliations'].append(affs)
                    cleanDict['Abstract'].append(abstract)

                    paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
                    
        elif fnmatch.fnmatch(firstauthor, winitial) == True:            
            for name in journalNames:
                if name in bibcode:
                    cleanDict['First Author'].append(firstauthor)
                    cleanDict['True Author'].append(trueauthor)
                    cleanDict['Bibcode'].append(bibcode)
                    cleanDict['Title'].append(title)
                    cleanDict['Year'].append(year)
                    cleanDict['Keywords'].append(keywords)
                    cleanDict['Affiliations'].append(affs)
                    cleanDict['Abstract'].append(abstract)

                    paperSearchDf = paperSearchDf[paperSearchDf['Bibcode'] != bibcode]
    
    dirtyDataDf = paperSearchDf
    cleanDataDf = pd.DataFrame(cleanDict)
                    
    return cleanDataDf, dirtyDataDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step7_cleanDf(cleanDataDf):
    '''
    This function performs the clean data merger from step 7 in expertiseFinder.
    '''
    # STEP 7: Now it's time to merge by True Author ! The input here is the data frame from the previous step, and the return is a merged data frame.
    cleanDataDf['Year']= cleanDataDf['Year'].astype(str)
    cleanDataDf['Abstract']= cleanDataDf['Abstract'].astype(str)

    mergedDataDf = cleanDataDf.groupby('True Author').aggregate({'First Author':', '.join,
                                                                 'Bibcode':', '.join, 
                                                                 'Title':', '.join, 
                                                                 'Year':', '.join, 
                                                                 'Keywords':', '.join, 
                                                                 'Affiliations':', '.join, 
                                                                 'Abstract':', '.join}).reset_index()
    
    return mergedDataDf
    
#################################################################################################################################

def step7_dirtyDf(dirtyDataDf):
    '''
    This function performs the dirty data merger from step 7 in expertiseFinder.
    '''
    dirtyDataDf['Year'] = dirtyDataDf['Year'].astype(str)
    dirtyDataDf['Abstract'] = dirtyDataDf['Abstract'].astype(str)

    mergedDirtyDf = dirtyDataDf.groupby('True Author').aggregate({'First Author':', '.join,
                                                                  'Bibcode':', '.join, 
                                                                  'Title':', '.join, 
                                                                  'Year':', '.join, 
                                                                  'Keywords':', '.join, 
                                                                  'Affiliations':', '.join, 
                                                                  'Abstract':', '.join}).reset_index()
    
    return mergedDirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################

def step8(mergedDataDf, mergedDirtyDf, directorypath):
    '''
    This function performs step 8 in the expertiseFinder function.
    '''
    # STEP 8: Find the top 10 words, bigrams, and trigrams of the mergedDataDf.
    top10Dict = {'Top 10 Words':[], 
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}

    for row in mergedDataDf.values:
        abstracts = row[7]

        top10words = topwords(abstracts, directorypath)
        top10bigrams = topbigrams(abstracts, directorypath)
        top10trigrams = toptrigrams(abstracts, directorypath)

        top10Dict['Top 10 Words'].append(top10words)
        top10Dict['Top 10 Bigrams'].append(top10bigrams)
        top10Dict['Top 10 Trigrams'].append(top10trigrams)

    top10Df = mergedDataDf
    top10Df['Top 10 Words'] = top10Dict['Top 10 Words']
    top10Df['Top 10 Bigrams'] = top10Dict['Top 10 Bigrams']
    top10Df['Top 10 Trigrams'] = top10Dict['Top 10 Trigrams']
    
    
    top10DirtyDict = {'Top 10 Words':[], 
                      'Top 10 Bigrams':[],
                      'Top 10 Trigrams':[]}

    for row in mergedDirtyDf.values:
        abstracts = row[7]

        top10words = topwords(abstracts, directorypath)
        top10bigrams = topbigrams(abstracts, directorypath)
        top10trigrams = toptrigrams(abstracts, directorypath)

        top10DirtyDict['Top 10 Words'].append(top10words)
        top10DirtyDict['Top 10 Bigrams'].append(top10bigrams)
        top10DirtyDict['Top 10 Trigrams'].append(top10trigrams)

    top10DirtyDf = mergedDirtyDf
    top10DirtyDf['Top 10 Words'] = top10DirtyDict['Top 10 Words']
    top10DirtyDf['Top 10 Bigrams'] = top10DirtyDict['Top 10 Bigrams']
    top10DirtyDf['Top 10 Trigrams'] = top10DirtyDict['Top 10 Trigrams']
    
    return top10Df, top10DirtyDf

################################################################################################################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################################################################################################################################################

def expertiseFinderTwitter(token, directorypath, rawFile, start, count):
    '''
    This function's purpose is to process data using ADS data to determine a name's astronomical expertise. To achieve this goal, the function first must be given an ADS API token ('token'), a .csv file with the data to be processed ('fileName'), the starting row index of that data where the function will begin processing (start), and the amount of rows following that start point to continue processing (count). The reason these last two arguments are included is to limit the number of queries this function processes; ADS API has a limit of 5000 queries per token per day, which if exceeded, will result in a loss of data from this function. 
    
    The steps followed throughout this function will be explained as they come along.
    
    NOTE: This version of the expertiseFinder function queries ADS for TWITTER DATA. 
    '''
    ads.config.token = token
    
    # STEP 1 & STEP 2:
    rawNames = step12(start, count, rawFile)
    
    # STEP 3: 
    searchQueries = step3(rawNames)
    
    # STEP 4: 
    Bibcodes, Names = step4(searchQueries)
            
    # STEP 5: 
    paperSearchDf = step5(Bibcodes, Names)

    # STEP 6: 
    cleanDataDf, dirtyDataDf = step6_Twitter(paperSearchDf)

    # STEP 7: 
    mergedDataDf = step7_cleanDf(cleanDataDf)
    mergedDirtyDf = step7_dirtyDf(dirtyDataDf)

    # STEP 8: 
    top10Df, top10DirtyDf = step8(mergedDataDf, mergedDirtyDf, directorypath)
    
    # STEP 9: 
    return top10Df, top10DirtyDf

###################################################################################################################################################################################################################################################################################################################################################################################################

def cleanTwitterData(rawData):
    '''
    This function takes in raw twitter data and picks out the names (in column 'Name') from a twitter data frame and keeps only the entries most likely to represent a full name.
    '''
    punc = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
    num = '''1234567890'''

    for i in range(len(rawData['Name'])):

        name = rawData['Name'][i]

        # Remove emojis and make lowercase
        name = clean(name, no_emoji=True)

        # Remove punctuation and numbers
        for letter in name:
            if letter in punc:
                name = name.replace(letter, "")
            if letter in num:
                name = name.replace(letter, "")

        tokenized = word_tokenize(name)
        if 'dr' in tokenized:
            # Remove dr
            tokenized.remove('dr')
        if 'phd' in tokenized:
            # Remove phd
            tokenized.remove('phd')
        if 'prof' in tokenized:
            # Remove prof
            tokenized.remove('prof')

        name = ' '.join(tokenized)
        rawData.at[i, 'Name'] = name
        
    # Determine which cells have a first and last name
    rawData = rawData.reset_index(drop = True)
    rawNames = rawData['Name']
    rawData['LastName, FirstName'] = ""

    for i in range(len(rawData['Name'])):
        name = rawData['Name'][i]
        tokenized = word_tokenize(name)
        if len(tokenized) > 1:
            namelist = name.split()
            lastnamefirstname = namelist[-1] + ', ' + namelist[0]
            rawData.at[i, 'LastName, FirstName'] = lastnamefirstname
    
    rawData = rawData.reset_index(drop = True)
    for i in range(len(rawData['Name'])):
        name = rawData['Name'][i]
        tokenized = word_tokenize(name)
        if len(tokenized) <= 1:
            rawData.at[i, 'LastName, FirstName'] = 'NaN'
        elif 'nasa' in tokenized:
            rawData.at[i, 'LastName, FirstName'] = 'NaN'
        elif 'aas' in tokenized:
            rawData.at[i, 'LastName, FirstName'] = 'NaN'
            
    # Add new column to data frame
    rawData = rawData[['IDnum', 'Name', 'LastName, FirstName', 'ScreenName', 'location', 'profile_loc', 'description', 'URL']]
    
    return rawData

###################################################################################################################################################################################################################################################################################################################################################################################################

def twitterNGrams(rawData, directorypath):
    '''
    This function determines the top words, bigrams, and trigrams for twitter bios.
    '''
    rawData['Twitter Top Words'] = ""
    rawData['Twitter Top Bigrams'] = ""
    rawData['Twitter Top Trigrams'] = ""
    for i in range(len(rawData['Name'])):
        desc = str(rawData['description'][i])
        topword = topwords(desc, directorypath)
        topbi = topbigrams(desc, directorypath)
        toptri = toptrigrams(desc, directorypath)
        
        rawData.at[i, 'Twitter Top Words'] = topword
        rawData.at[i, 'Twitter Top Bigrams'] = topbi
        rawData.at[i, 'Twitter Top Trigrams'] = toptri
        
    return rawData

################################################################################################################################################################################################################################################################################################################################################################################################

def dirtyCleaner_moreStrict_Twitter(dirtyDf, cleanDf, ogDf):
    '''
    This function takes in a dirty data frame outputted from expertiseFinder and removes any names in the dirty spreadsheet that are already present in the clean spreadsheet. Thus, it leaves only data on people who are missing from the clean spreadsheet, and need more investigating. 
    It also returns a spreadsheet of names without any hits on ADS. The names in missingNames are those that are not present in either cleanDf or dirtyDf.
    '''
    ogDf = ogDf.reset_index(drop = True)
    ogNames = ogDf['LastName, FirstName']   
    ogID = ogDf['IDnum']    
    
            
    for row in dirtyDf.values:
        trueauthorDirty = row[0]
        for i in range(len(cleanDf['True Author'])):
            if trueauthorDirty == cleanDf['True Author'][i]:
                dirtyDf = dirtyDf[dirtyDf['True Author'] != trueauthorDirty]
                
    dirtyDf = dirtyDf.reset_index(drop = True)
    
    
    
    missingNames = ogNames
    missingID = ogID
    missingNames = pd.DataFrame({'LastName, FirstName': missingNames, 'IDnum':missingID})
    
    for row1 in missingNames.values:
        name = row1[0]
        ids = row1[1]
        for row2 in cleanDf.values:
            cleanname = row2[0]
            if name == cleanname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
        for row3 in dirtyDf.values:
            dirtyname = row3[0]
            if name == dirtyname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
                
    missingNames = missingNames.reset_index(drop = True)
    
    
    
    return dirtyDf, cleanDf, missingNames

################################################################################################################################
################################################################################################################################################################################################################################################################

def dirtyCleaner_lessStrict_Twitter(dirtyDf, cleanDf, ogDf):
    '''
    This function takes in a dirty data frame outputted from expertiseFinder and removes any names in the dirty spreadsheet that are already present in the clean spreadsheet. Thus, it leaves only data on people who are missing from the clean spreadsheet, and need more investigating. 
    It also returns a spreadsheet of names without any CLEAN hits on ADS. So, the missingNames return includes names that are not present in cleanDf, but ARE present in dirtyDf.
    '''
    ogDf = ogDf.reset_index(drop = True)
    ogNames = ogDf['LastName, FirstName']   
    ogID = ogDf['IDnum']
    
    
            
    for row in dirtyDf.values:
        trueauthorDirty = row[0]
        for i in range(len(cleanDf['True Author'])):
            if trueauthorDirty == cleanDf['True Author'][i]:
                dirtyDf = dirtyDf[dirtyDf['True Author'] != trueauthorDirty]
                
    dirtyDf = dirtyDf.reset_index(drop = True)
    
    
    
    missingNames = ogNames
    missingID = ogID
    missingNames = pd.DataFrame({'LastName, FirstName': missingNames, 'IDnum':missingID})
    
    for row1 in missingNames.values:
        name = row1[0]
        ids = row1[1]
        for row2 in cleanDf.values:
            cleanname = row2[0]
            if name == cleanname:
                missingNames = missingNames[missingNames['LastName, FirstName'] != name]
                
    missingNames = missingNames.reset_index(drop = True)
    
    
    
    return dirtyDf, cleanDf, missingNames

################################################################################################################################################################################################################################################################################################################################################################################################

def spreadsheetMaker_Twitter(cleanDf, dirtyDf, missingDf, ogDf):
    '''
    This function combines the data from three separate spreadsheets: cleanDf, dirtyDf, and missingDf, to create a single spreadsheet of Twitter data. This final spreadsheet, finalDf, combines data from cleanDf, dirtyDf, and missingDf to make all analysis from the previous functions more digestable. 
    
    The final spreadsheet should contain Twitter data (user names, descriptions, top words, etc.) and ADS data (bibcodes, abstracts, top words, etc.). There will also be a column labelling whether that row contains clean ADS data (matched our critera from expertiseFinder), dirty ADS data (produced results in ADS, but nothing that met our criteria from expertiseFinder), and missing ADS data (names that produced no hits on ADS).
    '''
    
    # STEP 1: Make empty columns to fill.
    ogDf['First Author'] = ""
    ogDf['Bibcode'] = ""
    ogDf['Title'] = ""
    ogDf['Year'] = ""
    ogDf['Keywords'] = ""
    ogDf['Affiliations'] = ""
    ogDf['Abstract'] = ""
    ogDf['ADS Top Words'] = ""
    ogDf['ADS Top Bigrams'] = ""
    ogDf['ADS Top Trigrams'] = ""
    ogDf['Data Type'] = ""
    
    # STEP 2: Fill those empty columns with clean, dirty, and missing data.
    for i in range(len(rawCleanDf_ADSCleanDf['LastName, FirstName'])):
        name1 = rawCleanDf_ADSCleanDf['LastName, FirstName'][i]

        for j in range(len(twitterData_cleanFINAL['True Author'])):
            name2 = twitterData_cleanFINAL['True Author'][j]
            firstauth2 = twitterData_cleanFINAL['First Author'][j]
            bib2 = twitterData_cleanFINAL['Bibcode'][j]
            tit2 = twitterData_cleanFINAL['Title'][j]
            year2 = twitterData_cleanFINAL['Year'][j]
            keyw2 = twitterData_cleanFINAL['Keywords'][j]
            aff2 = twitterData_cleanFINAL['Affiliations'][j]
            abs2 = twitterData_cleanFINAL['Abstract'][j]
            topw2 = twitterData_cleanFINAL['Top 10 Words'][j]
            topb2 = twitterData_cleanFINAL['Top 10 Bigrams'][j]
            topt2 = twitterData_cleanFINAL['Top 10 Trigrams'][j]

            if name1 == name2:
                rawCleanDf_ADSCleanDf.at[i, 'First Author'] = firstauth2
                rawCleanDf_ADSCleanDf.at[i, 'Bibcode'] = bib2
                rawCleanDf_ADSCleanDf.at[i, 'Title'] = tit2
                rawCleanDf_ADSCleanDf.at[i, 'Year']  = year2
                rawCleanDf_ADSCleanDf.at[i, 'Keywords'] = keyw2
                rawCleanDf_ADSCleanDf.at[i, 'Affiliations']  = aff2
                rawCleanDf_ADSCleanDf.at[i, 'Abstract'] = abs2
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Words'] = topw2
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Bigrams'] = topb2
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Trigrams'] = topt2
                rawCleanDf_ADSCleanDf.at[i, 'Data Type'] = 'CLEAN'

        for j in range(len(twitterData_dirtyFINAL['True Author'])):
            name3 = twitterData_dirtyFINAL['True Author'][j]
            firstauth3 = twitterData_dirtyFINAL['First Author'][j]
            bib3 = twitterData_dirtyFINAL['Bibcode'][j]
            tit3 = twitterData_dirtyFINAL['Title'][j]
            year3 = twitterData_dirtyFINAL['Year'][j]
            keyw3 = twitterData_dirtyFINAL['Keywords'][j]
            aff3 = twitterData_dirtyFINAL['Affiliations'][j]
            abs3 = twitterData_dirtyFINAL['Abstract'][j]
            topw3 = twitterData_dirtyFINAL['Top 10 Words'][j]
            topb3 = twitterData_dirtyFINAL['Top 10 Bigrams'][j]
            topt3 = twitterData_dirtyFINAL['Top 10 Trigrams'][j]

            if name1 == name3:
                rawCleanDf_ADSCleanDf.at[i, 'First Author'] = firstauth3
                rawCleanDf_ADSCleanDf.at[i, 'Bibcode'] = bib3
                rawCleanDf_ADSCleanDf.at[i, 'Title'] = tit3
                rawCleanDf_ADSCleanDf.at[i, 'Year']  = year3
                rawCleanDf_ADSCleanDf.at[i, 'Keywords'] = keyw3
                rawCleanDf_ADSCleanDf.at[i, 'Affiliations']  = aff3
                rawCleanDf_ADSCleanDf.at[i, 'Abstract'] = abs3
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Words'] = topw3
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Bigrams'] = topb3
                rawCleanDf_ADSCleanDf.at[i, 'ADS Top Trigrams'] = topt3
                rawCleanDf_ADSCleanDf.at[i, 'Data Type'] = 'DIRTY'

        for j in range(len(twitterData_missingFINAL['LastName, FirstName'])):
            name4 = twitterData_missingFINAL['LastName, FirstName'][j]

            if name1 == name4:
                rawCleanDf_ADSCleanDf.at[i, 'Data Type'] = 'MISSING'
                
    # STEP 3: Reorder the columns.
    ogDf = ogDf[['Name',
                 'LastName, FirstName',
                 'IDnum',
                 'ScreenName',
                 'location',
                 'profile_loc',
                 'URL',
                 'description',
                 'Top Words',
                 'Top Bigrams',
                 'Top Trigrams',
                 'First Author',
                 'Bibcode',
                 'Title',
                 'Year',
                 'Keywords',
                 'Affiliations',
                 'Abstract',
                 'ADS Top Words', 
                 'ADS Top Bigrams', 
                 'ADS Top Trigrams', 
                 'Data Type']]
    
    # STEP 4: Rename the columns.
    ogDf.rename(columns = {'IDnum':'ID Number',
                           'ScreenName':'Screen Name', 
                           'location':'Location', 
                           'profile_loc':'Profile Loc', 
                           'description':'Description', 
                           'Top Words':'Twitter Top Words', 
                           'Top Bigrams':'Twitter Top Bigrams', 
                           'Top Trigrams':'Twitter Top Trigrams'}, inplace = True)
    
    return ogDf

################################################################################################################################################################################################################################################################################################################################################################################################