'''
Program that reads the text data from Temple dataset files and then pulls out:
1. Demographics - done "on the fly" in a per file manner
2. Keywords - will be done across whole dataset in a computer intensive manner
'''

import os
import pickle
from difflib import SequenceMatcher

import fuzzysearch as fs
import pandas as pd
import winsound
from fuzzysearch.common import consolidate_overlapping_matches
from nltk.stem.porter import *
from tqdm import trange

# stopwords = set(stopwords.words("english"))

# Global lists which contain key words for identifying demogs - please add any you can think of
MaleWords = [" male", " man", " boy"]
FemaleWords = [" female", " woman", " girl"]
AgeWords = ["-year-old", " year old", " y.o.", "yr ", "yo ", "YO ", "Y/O ", "y.o ", "year man", "year woman"]
HzGloss = ["Hz", "Hertz", "hz", "hertz", "c/s", "cycles per second"]

# mainPath = "TUE/" #Our Directory
mainPath = r"H:\EEGData"  # A folder containing all the tuh_eeg reports,
# available from https://www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg/v1.2.0/reports.tar.gz
mainPathNormal = r"H:\ClassifiedEEGs\AbnormalVsNormal\v2.0.0\edf\eval\normal"  # Normal EEGs
mainPathAbnormal = r"H:\ClassifiedEEGs\AbnormalVsNormal\v2.0.0\edf\train\abnormal"  # Abnormal EEGs

glossary_file = r"C:\Users\Rohan\PycharmProjects\Temple-Data-Management\EEG Glossary V4.xlsx"

pklFN = "MatchPickle"
destination_folder = r"C:/Users/Rohan/PycharmProjects/Temple-Data-Management/"

MSDict = {"ms" : "multiple sclerosis", "multiple sclerosis" : "multiple sclerosis", "rrms" : "multiple sclerosis", "ppms" : "multiple sclerosis"}

def GetDir(dir):
    TxtFiles = []
    EdfFiles = []
    Directory = os.scandir(dir)
    # where TUE is the folder containing EEG data (txt and edf files) - with more data this will have to be more 
    # structured 
    for file in Directory:
        # here we separate out the files into txt and edf - NB this function is just returning their
        # locations as dir objects so that other functions can open the files stepwise
        if file.is_dir():
            # Go deeper
            (subdTxtFiles, subdEdfFiles) = GetDir(file.path)
            # Append results from subdirectory(s)
            TxtFiles += subdTxtFiles
            EdfFiles += subdEdfFiles
        if os.path.splitext(file.name)[1] == ".txt":
            TxtFiles.append(file)
        elif os.path.splitext(file.name)[1] == ".edf":
            EdfFiles.append(file)
    return (TxtFiles, EdfFiles)


def GetSex(string):  # uses keywords to spot sex from a string
    Sex = 0
    lstring = string.lower()
    # We now search for Male words and increase sex by 1 per word
    for word in MaleWords:
        if lstring.find(word.lower()) >= 0:
            Sex += 1
    # We now search for Female words and decrease sex by 1 per word
    for word in FemaleWords:
        if lstring.find(word.lower()) >= 0:
            Sex -= 1
    # Now we determine sex by whether Sex is pos/neg
    if Sex > 0:
        return ("Male")
    elif Sex < 0:
        return ("Female")
    else:
        return ("Undetermined")


def GetAge(string):  # uses keywords to spot age from a string
    Age = "Not Determined"
    lstring = string.lower()
    for word in AgeWords:
        WordLocation = lstring.find(word.lower())
        if WordLocation > -1:
            Age = string[(WordLocation - 5):WordLocation]  # last 5 chars before the Age keyword are selected
            # note I imposed a theoretical maximum age of 999 by doing this. Can be updated post-singularity.
            Age = re.sub("[^0-9]", "", Age)  # Non numerical characters are stripped from Age string
    return (Age)


def GetDemographics(file):  # takes a file as provided as a dir object by os and gets the text content (for text files)
    # first we open the file
    if isinstance(file, str):
        path = file
    else:
        path = file.path
    f = open(path, "r")
    try:
        TextFileContent = f.read()
    except UnicodeDecodeError:
        print("UnicodeDecodeError on " + path + ".")
        TextFileContent = ""
    except FileNotFoundError:
        print("File not found: " + path)
    # TextFileContent is a string
    # We then run functions to extract Age and Sex
    Sex = GetSex(TextFileContent)
    Age = GetAge(TextFileContent)

    return (Age, Sex)


def GetDemographicsAndText(file):
    '''
    takes a file as provided as a dir object by os and gets the text content (for text files)
    '''
    # first we open the file
    if isinstance(file, str):
        path = file
    else:
        path = file.path
    f = open(path, "r")
    try:
        TextFileContent = f.read()
    except UnicodeDecodeError:
        print("UnicodeDecodeError on " + file.path + ".")
        TextFileContent = ""
    # TextFileContent is a string
    # We then run functions to extract Age and Sex
    Sex = GetSex(TextFileContent)
    Age = GetAge(TextFileContent)

    return (Age, Sex, TextFileContent)


def CompileDemographics(Path):
    '''
    returns a dataframe of all the demographics from text files in the directory selected
    '''

    TxtFiles, EdfFiles = GetDir(Path)
    column_names = ["Patient", "Age", "Sex"]
    Demographics = pd.DataFrame(columns=column_names)  # sets up a blank dataframe with some columns
    n_undet = 0
    for file in TxtFiles:
        Age, Sex = GetDemographics(file)
        if Age != "Not Determined" and Sex != "Not Determined" and len(Age) == 2:
            Demographics = Demographics.append(pd.Series([file.name[:-4], Age, Sex], index=column_names),
                                               ignore_index=True)
        else:
            n_undet += 1
        # each line is the filename (without extension), then demographics
        # Note: I am using the txt filenames as the labels for the patients because they appear to be
        # unique identifiers that serve as prefixes for the patient's EEG files
    Demographics['Age'] = pd.to_numeric(Demographics['Age'])
    print("number of undetermined age or sex: ", n_undet)
    return (Demographics)


def CompileDemographicsAndText(Path):
    # returns a dataframe of all the demographics from text files in the directory selected
    TxtFiles, EdfFiles = GetDir(Path)
    column_names = ["Patient", "Age", "Sex", "text"]
    Demographics = pd.DataFrame(columns=column_names)  # sets up a blank dataframe with some columns
    n_undet = 0
    for file in TxtFiles:
        Age, Sex, text = GetDemographicsAndText(file)
        if Age != "Not Determined" and Sex != "Not Determined":
            Demographics = Demographics.append(pd.Series([file.name[:-4], Age, Sex, text], index=column_names),
                                               ignore_index=True)
        else:
            n_undet += 1
        # each line is the filename (without extension), then demographics
        # Note: I am using the txt filenames as the labels for the patients because they appear to be
        # unique identifiers that serve as prefixes for the patient's EEG files
    Demographics['Age'] = pd.to_numeric(Demographics['Age'])
    print(Demographics)
    print("number of undertermined age or sex: ", n_undet)
    return (Demographics)


def CheckUndeterminedResults():
    '''
    pulls concerning demographics results
    '''
    TxtFiles, EdfFiles = GetDir(mainPath)
    column_names = ["Patient", "Age", "Sex", "text"]
    Details = pd.DataFrame(columns=column_names)
    for file in TxtFiles:
        Age, Sex, text = GetDemographicsAndText(file)
        if Age == "Not Determined" or Sex == "Not Determined":
            Details = Details.append(pd.Series([file.name[:-4], Age, Sex, text[:200]], index=column_names),
                                     ignore_index=True)
    print(Details)  # a dataframe of data including both demographics and the first 200 characters of the text file.
    Details.to_excel(r"Data\UndeterminedDemographics.xlsx", sheet_name="Data", index=False)

    return (Details)


def concatenate_list_data(list):
    result = ''
    for element in list:
        result += (str(element) + " ")
    return result


def strip_interpretation(text):
    word_list = ['DESCRIPTION OF THE RECORD']
    lines_with_colons = []
    line_number = 0
    for i, char in enumerate(text):
        if char == '\n':
            line_number += 1
        if char == ':':
            lines_with_colons.append(line_number)

    stop_line = None
    lines = text.splitlines()
    print(lines)
    for i in lines_with_colons:
        suspect_line = lines[i]
        line_header = suspect_line[:suspect_line.find(':')]
        word_out, match = roughStringMatch(line_header, word_list, False)
        if match:
            stop_line = i

    print(stop_line)
    out_text = ""
    if stop_line is not None:
        for i in range(stop_line):
            out_text += f"{lines[i]}\n"
        return out_text
    else:
        return None

    
def strip_interpretations(report_file, text, word_list):
    lines_with_colons = []
    with open(report_file, 'r') as f:
        txt = f.read()
        line_number = 0
        for i, char in enumerate(txt):
            if char == '\n':
                line_number += 1
            if char == ':':
                lines_with_colons.append(line_number)

    stop_line = None
    with open(report_file, 'r') as f:
        lines = f.readlines()
        for i in lines_with_colons:
            suspect_line = lines[i]
            line_header = suspect_line[:suspect_line.find(':')]
            word_out, match = roughStringMatch(line_header, word_list, False)
            if match:
                stop_line = i

    out_text = ""
    if stop_line is not None:
        with open(report_file, 'r') as f:
            lines = f.readlines()
            for i in range(stop_line):
                out_text += lines[i]
    
    return out_text


def roughStringMatch(wordIn, wordList, userConfirm=True, thresh=0.8, stopAtOne=True, failSafe=False,
                     pklFN="confirmedWordMatches.pkl"):
    """ Standardise a provided string (e.g. with spelling errors, shortened versions)
        according to a list of standard words (wordList).

        Parameters:
        wordIn (str): string to be standardised
        wordList (list of str): List of standard strings
        manualConfirm (boolean): Whether user confirmation is required for close but imperfect matches.
        thresh (float): Threshold for similarity ratio.  When manualConfirm is False
                        and thresh < matchRatio, the match will be accepted. When userConfirm is
                        True and thresh < matchRatio < 1, user confirmation will be sought.
        stopAtOne (boolean): Whether to stop as soon as one acceptable match is found.
        failSafe (boolean): If False (default), in cases where no match was found, the original
                        word will be returned. If failSafe is True, such cases will cause a runTimeError.
        pklFN (str): File name or full path for pickle file to use as reference list of confirmed matches
                        and non-matches, to prevent repetitive user confirmation.
                        default = "confirmedWordMatches.pkl.

        Returns:
        wordOut ((list of) str): The string (or strings, if stopAtOne==False) accepted as match for wordIn
        success (boolean): True if an acceptable match was found, otherwise False.

        """

    confirmedMatches = {}
    confirmedDiff = {}
    matches = []

    for word in wordList:

        ratio = SequenceMatcher(None, wordIn.lower(), word.lower()).ratio()
        if ratio == 1:
            # Perfect match
            if stopAtOne:
                return word, True
            else:
                matches.append(word)
                continue
        elif ratio > thresh:
            # Near match. Check if we've already compared these two previously.
            # First load any confirmed matches/differences from file:
            if os.path.isfile(pklFN) and os.path.getsize(pklFN) > 0:
                with open(pklFN, 'rb') as f:  # Python 3: open(..., 'wb')
                    confirmedMatches, confirmedDiff = pickle.load(f)
            # Match already confirmed for this pair?
            if (word in confirmedMatches) and (wordIn in confirmedMatches[word]):
                if stopAtOne:
                    return word, True
                else:
                    matches.append(word)
                    continue
            # Difference already confirmed for this pair?
            if (word in confirmedDiff) and (wordIn in confirmedDiff[word]):
                continue

            # Unseen pair. Prompt for manual check?
            if userConfirm:
                winsound.Beep(2000, 100)
                print("Are these words interchangeable (i.e. is '" + wordIn + "' intended to be '" + word + "')?")
                print(wordIn)
                print(word)
                ansAccepted = False
                ans = input("y/n")
                while not ansAccepted:
                    if ans.lower() in ["y", "yes"]:
                        if not word in confirmedMatches:
                            confirmedMatches[word] = {wordIn}
                        else:
                            confirmedMatches[word].add(wordIn)
                        with open(pklFN, 'wb') as f:  # Python 3: open(..., 'wb')
                            pickle.dump([confirmedMatches, confirmedDiff], f)
                        ansAccepted = True
                        if stopAtOne:
                            return word, True
                        else:
                            matches.append(word)
                        break
                    elif ans.lower() in ["n", "no"]:
                        ansAccepted = True
                        if not word in confirmedDiff:
                            confirmedDiff[word] = {wordIn}
                        else:
                            confirmedDiff[word].add(wordIn)
                        with open(pklFN, 'wb') as f:  # Python 3: open(..., 'wb')
                            pickle.dump([confirmedMatches, confirmedDiff], f)
                        continue
                    ans = input("y/n")
            else:
                # userConfirm==False. Just accept it.
                if stopAtOne:
                    return word, True
                else:
                    matches.append(word)

    if matches:
        return matches, True
    else:
        if failSafe:
            # raise RuntimeError("name " + wordIn + " not found in wordList.")
            pass
        else:
            return wordIn, False


def NormalVsAbnormal(Data):
    '''
    Takes a dataframe
    Can use Output of GetDemographics()
    Returns a dataframe with extra column "normality" containing a value which is abnormal if <0, normal if >0
    '''

    NormalSeries = []
    for row in Data["text"]:
        Normality = DetermineNormal(row)
        NormalSeries.append(Normality)
    Data["normality"] = NormalSeries

    return Data


def PDtoNP(Data):
    if isinstance(Data, pd.DataFrame):
        DataArray = Data.to_numpy
    elif isinstance(Data, np.array):
        pass
    else:
        raise ValueError("PDtoNP requires numpy array or Pandas Dataframe")
    return (DataArray)


def DetermineNormal(text):
    '''

    text is a string
    input whole report or substring
    returns a value which is abnormal if <0, normal if >0

    '''

    text = text.lower()
    Normality = 0
    NormPlace = text.find("normal")
    while NormPlace > -1:
        if text[NormPlace - 2:NormPlace] == "ab":
            if text[NormPlace - 6:NormPlace - 3] == "not":
                Normality += 1
            else:
                Normality -= 1
        elif text[NormPlace + 7:NormPlace + 13] == "limits":
            if text[NormPlace - 7:NormPlace - 1] == "within":
                if text[NormPlace - 11:NormPlace - 8] == "not":
                    Normality -= 1
                elif text[NormPlace - 10:NormPlace - 8] == "is":
                    Normality += 1
            if text[NormPlace - 8:NormPlace - 1] == "outside":
                Normality -= 1
        else:
            Normality += 1
        text = text[:NormPlace] + text[NormPlace + 6:]
        NormPlace = text.find("normal")

    return Normality


def ProcessNormalVsAbnormal():
    '''
    When working with two folders of reports, one with normal reports and one with abnormal reports, this allows one to
    analyse normality of the reports and summarize with some stats.

    useful for testing the normal/abnormal delineation
    '''

    AbnormalReports = CompileDemographicsAndText(mainPathAbnormal)
    AbnormalReports["DatasetNormal"] = "FALSE"
    NormalityDataframe = NormalVsAbnormal(AbnormalReports)
    Abnormals = NormalityDataframe

    NormalReports = CompileDemographicsAndText(mainPathNormal)
    NormalReports["DatasetNormal"] = "TRUE"
    Normals = NormalVsAbnormal(NormalReports)
    NormalityDataframe = NormalityDataframe.append(Normals, ignore_index=True)
    print(NormalityDataframe)

    NormalityDataframe.to_excel('Data/NormalVsAbnormal.xlsx', sheet_name="NormalVsAbnormal")
    for i in range(-5, 5):
        TP = Abnormals[Abnormals.normality < i].normality.count()
        TN = Normals[Normals.normality > i].normality.count()
        FP = Normals[Normals.normality < i].normality.count()
        FN = Abnormals[Abnormals.normality > i].normality.count()

        Sens = TP / (TP + FN)
        Spec = TN / (TN + FP)
        NPV = TN / (TN + FN)

        print("With a threshold at ", i)
        print("Sens = ", Sens, "\nSpec = ", Spec, "\nNPV = ", NPV)

        print("Done")
    import matplotlib.pyplot as plt

    PlotDF = pd.DataFrame({"Normal": Normals.normality,
                           "Abnormal": Abnormals.normality})
    plt.close('all')

    ax = PlotDF.plot.hist(alpha=0.5)

    plt.show()

    return ()


def WordSearch(ReportDict, glossary, Multithreaded=False):
    '''
    Function to iterate GetMatches over the text "column" of ReportDict

    Takes a dict of dicts that includes a 2nd order dict key "text"

    Returns dict of dicts with added Key "matches" full of dicts {word:Match}
    '''
    if Multithreaded:
        pass
        # needs work
    else:
        for i in trange(len(ReportDict),
                        desc="Getting fuzzy matches using Glossary terms"):
            Matches = GetMatches(ReportDict[i]["text"].lower(), glossary)
            ReportDict[i]["matches"] = Matches
    return (ReportDict)


def GetMatches(text, glossary):
    '''
    searches text (string) for every word in glossary and returns a dict of the word
    searched (and matched) and the Match object returned

    Match object has attributes:
    Match.start - location of substring start in text
    Match.end - location of substring end in text
    Match.dist - levenstein distance (word to matched substring)
    Match.matched - substring match to searched term
    '''
    text = text.replace('\n', ' ').replace('\r', '')
    text = "  " + text + "  "  # To stop error caused by substrings being at end of text

    Matches = {}
    for i in range(len(glossary)):
        word = glossary[i]["word"].lower()
        FuzzyOut = fs.find_near_matches(word, text, max_l_dist=1,
                                        max_deletions=1, max_insertions=1)
        consolidate_overlapping_matches(FuzzyOut)
        for Match in FuzzyOut:

            StartText = Match.start
            EndText = Match.end
            CharBefore = text[StartText - 1]
            CharAfter = text[EndText + 1]

            if (CharBefore.isalnum() and CharAfter.isalnum()):
                # Removes the match if it is in the middle of a word
                # (to stop REM etc. being found everywhere)
                FuzzyOut.remove(Match)

            if len(word) < 4 and (CharBefore.isalnum() or CharAfter.isalnum()):
                #Short words are often found embedded in other words, annoyingly
                FuzzyOut.remove(Match)


            elif (CharBefore.isalnum() or CharAfter.isalnum()) and Match.dist > 0:
                # If matched substring is part of a word, it is not allowed to also have a typo.
                FuzzyOut.remove(Match)
                break

            else:
                Matches[word] = Match

                # Check if the same text has been matched by two words and delete the one less like it
                for Match2 in FuzzyOut:
                    # checks by seeing if they overlap by more than half the length of Match
                    if max(Match.start, Match2.start) - min(Match.end, Match2.end) > len(Match.matched) / 2:
                        if Match.dist > Match2.dist:
                            FuzzyOut.remove(Match)
                            Matches[word] = Match2  # as Match2 is closer
                            break

    return (Matches)


def CheckMatches(ReportDict, column = "matches"):
    '''
    Function that takes a dict-table with a "column" of dicts. These dicts show
    the matched words and the paired match objects as output by GetMatches.

    Iterates through the column by patient, then by word within patient's listed
    matches.

    Requires human input to confirm Fuzzy matches, so cannot be parallelised.
    '''

    confirmedMatches = {}
    confirmedDiff = {}

    if os.path.isfile(pklFN) and os.path.getsize(pklFN) > 0:
        with open(pklFN, 'rb') as f:  # Python 3: open(..., 'wb')
            confirmedMatches, confirmedDiff = pickle.load(f)
            print("Pickle file of previous confirmed matches loaded.\n", len(confirmedMatches), " confirmed matches\n",
                  len(confirmedDiff), " confirmed differences")

    for i in range(len(ReportDict)):

        MatchesFinal = []
        Matches = ReportDict[i][column]
        for word in Matches.keys():
            '''
            Iterate through the matches in the matches "column"
            '''
            wordIn = Matches[word].matched
            StartText = Matches[word].start
            EndText = Matches[word].end
            Context = ReportDict[i]["text"][StartText - 10:EndText + 10]

            if Matches[word].dist == 0 or wordIn + "s" == word or wordIn == word + "s":
                # exact match +/- plurals
                MatchesFinal.append(wordIn)
            else:
                # Near match. Check if we've already compared these two before.
                # Match already confirmed for this pair?
                if (word in confirmedMatches) and \
                        (wordIn in confirmedMatches[word]):
                    MatchesFinal.append(word)
                    continue
                # Difference already confirmed for this pair?
                if (word in confirmedDiff) and (wordIn in confirmedDiff[word]):
                    continue
                # Unseen pair. Prompt for manual check
                print("is \n'" + wordIn + "' in \n'" + Context + "' intended to be \n'" \
                      + word + "?")
                ansAccepted = False
                ans = input("y/n")
                while not ansAccepted:
                    if ans.lower() in ["y", "yes"]:
                        if not word in confirmedMatches:
                            confirmedMatches[word] = {wordIn}
                        else:
                            confirmedMatches[word].add(wordIn)
                        with open(pklFN, 'wb') as f:
                            pickle.dump([confirmedMatches, confirmedDiff], f)
                        ansAccepted = True
                        NoList1 = ["no", "not", "NO", "NOT", "No", "Not", \
                                   "Absent", "absent", "ABSENT", "?"]
                        NoList2 = ["None", "none", "NONE", "Absent", "absent", \
                                   "ABSENT", "not"]
                        if any((" " + x) in \
                               ReportDict[i]["text"][StartText - 10:StartText] \
                               for x in NoList1):
                            print("Negative use of word")
                        elif any((" " + x) in \
                                 ReportDict[i]["text"][EndText:EndText + 10] \
                                 for x in NoList2):
                            print("Negative use of word")
                        else:
                            MatchesFinal.append(word)
                        break
                    elif ans.lower() in ["n", "no"]:
                        ansAccepted = True
                        if not word in confirmedDiff:
                            confirmedDiff[word] = {wordIn}
                        else:
                            confirmedDiff[word].add(wordIn)
                        with open(pklFN, 'wb') as f:
                            pickle.dump([confirmedMatches, confirmedDiff], f)
                        continue
                    elif ans.lower() == "preview_results":
                        print(ReportDict[column])
                    ans = input("y/n")
        confirmedcolumn = column + "final"
        ReportDict[i][confirmedcolumn] = MatchesFinal
    return (ReportDict)


def DataFrameToDict(df):
    '''
    Converts dataframe to dict of dicts for the benefit of speeding up with parallelisation
    '''
    dict = df.T.to_dict('dict')
    return (dict)


def ReportSearch(InputFile="RawReports.xlsx", OverWrite=False, Save=True, GetKeywords = True):
    '''
    Loads a dataframe from excel, converts to dict
    needs column named: "text"

    This dict then has fuzzysearch applied, row-wise, on text column
    Adds columns called "matches" and "confirmedmatches"

    Parses text with ParseReport() - columns "impression", "correlation"
    Assesses Normality using GetNormality() - column "normality"

    Assess consciousness with GetConsciousness() - column "gcs"
    '''

    from pathlib import Path

    df_glossary = pd.read_excel(glossary_file, sheet_name="words")
    GlossaryDict = DataFrameToDict(df_glossary)

    os.chdir(destination_folder)

    if Path(InputFile).exists() and OverWrite == False:
        ReportDataframe = pd.read_excel(InputFile)
        ReportDict = DataFrameToDict(ReportDataframe)

        print("Loaded and working from previous reports file: ", InputFile)
    else:

        ReportDataframe = CompileDemographicsAndText(mainPath)
        ReportDataframe = ReportDataframe.replace(r'\\n', ' ', regex=True)
        ReportDict = DataFrameToDict(ReportDataframe)
        ReportDataframe.to_excel(InputFile, sheet_name="Data", index=False)

    if GetKeywords:
        ReportDict = WordSearch(ReportDict, GlossaryDict)
        ReportDict = CheckMatches(ReportDict)

    for i in trange(len(ReportDict), desc="Parsing reports into sections    "):
        ReportDict[i]["impression"], ReportDict[i]["correlation"] = ParseReport(ReportDict[i]["text"])

    for i in trange(len(ReportDict), desc="Assessing normality              "):
        if ReportDict[i]["impression"] == False:
            ReportDict[i]["normality"] = DetermineNormal(ReportDict[i]["text"])
        else:
            ReportDict[i]["normality"] = DetermineNormal(ReportDict[i]["impression"])

    for i in trange(len(ReportDict), desc="Assessing Consciousness          "):
        ReportDict[i]["gcs"] = GetConsciousness(ReportDict[i]["text"])

    if Save:
        ReportDataframe = pd.DataFrame.from_dict(ReportDict)
        ReportDataframe = ReportDataframe.transpose()
        ReportDataframe.to_excel("KeywordSaveFile.xlsx", sheet_name="Data", index=False)

    return (ReportDict)


def ParseReport(string):
    '''
    Divides text into substrings split at "Impression" and "Clinical correlation" if present.
    '''
    text = string.lower()
    if "impression" in text:
        Impression = text.split("impression")[1]
        if "clinical correlation" in text:
            Impression = Impression.split("clinical correlation")[0]
            Correlation = text.split("clinical correlation")[1]
        else:
            Correlation = False
    else:
        Impression = False
        if "clinical correlation" in text:
            Correlation = text.split("clinical correlation")[1]
        else:
            Correlation = False

    return (Impression, Correlation)


def GetConsciousness(text):
    import re
    text = text.lower()

    GCSMatch = fs.find_near_matches("gcs", text, max_l_dist=0,
                                    max_deletions=0, max_insertions=0)
    GCSMatch.extend(fs.find_near_matches("glasgow coma scale", text, max_l_dist=2,
                                    max_deletions=1, max_insertions=1))
    GCSMatch.extend(fs.find_near_matches("glasgow coma score", text, max_l_dist=2,
                                         max_deletions=1, max_insertions=1))
    if len(GCSMatch) > 0:
        for Match in GCSMatch:
            return re.sub("[^0-9]", "",text[Match.end : Match.end + 4])
    else:
        return "NaN"

def GetNCSE(text):
    raise NotImplementedError

def GetEncephalopathy(text):
    raise NotImplementedError

def GetDisease(text, DiseaseGlossary):
    '''
    Function that searches text for disease keywords using fuzzy searching
    diseaseGlossary as dict of disease synonym: preferred name
    e.g.
    "MS"                    :   "Multiple Sclerosis"
    "Multiple Sclerosis"    :   "Multiple Sclerosis"

    returns a list of match objects for a text string
    '''
    text = text.lower()
    Matches = {}

    for Disease in DiseaseGlossary.keys():
        if len(Disease) > 3:
            #for full names we allow spellign errors
            FuzzyOut = fs.find_near_matches(Disease, text, max_l_dist=1, max_deletions=1, max_insertions=1)
        else:
            #not for acronyms <3 characters long
            FuzzyOut = fs.find_near_matches(Disease, text, max_l_dist=0, max_deletions=0, max_insertions=0)
        for Match in FuzzyOut:

            StartText = Match.start
            EndText = Match.end
            CharBefore = text[StartText - 1]
            CharAfter = text[EndText + 1]

            if (CharBefore.isalnum() and CharAfter.isalnum()):
                # Removes the match if it is in the middle of a word
                # (to stop REM etc. being found everywhere)
                FuzzyOut.remove(Match)

            elif len(Disease) < 4 and (CharBefore.isalnum() or CharAfter.isalnum()):
                #Short words are often found embedded in other words, annoyingly
                FuzzyOut.remove(Match)

            elif (CharBefore.isalnum() or CharAfter.isalnum()) and Match.dist > 0:
                # If matched substring is part of a word, it is not allowed to also have a typo.
                FuzzyOut.remove(Match)
                break

            else:
                Matches[Disease] = Match

                # Check if the same text has been matched by two words and delete the one less like it
                for Match2 in FuzzyOut:
                    # checks by seeing if they overlap by more than half the length of Match
                    if max(Match.start, Match2.start) - min(Match.end, Match2.end) > len(Match.matched) / 2:
                        if Match.dist > Match2.dist:
                            FuzzyOut.remove(Match)
                            Matches[Disease] = Match2  # as Match2 is closer
                            break

    return Matches

def RearrangeGlossary(Glossary):
    '''
    Takes glossary as dict like:
    {MainTerm1 : [List of synonyms1]
    Mainterm2 : [List of synonyms2]}

    OR

    Array like:
    (( MainTerm1, [List of synonyms1])
    (Mainterm2, [List of synonyms2]))

    and turns it into a good format for our program:
    {Synonym1a : Mainterm1
    Synonym1b : Mainterm1
    Synonym2a : Mainterm2
    Synonym2b : Mainterm2}
    '''

    GlossaryDict = {}
    if type(Glossary) is dict:
        for key in Glossary.keys():
            for synonym in Glossary[key]:
                GlossaryDict[synonym] = key

    elif type(Glossary) is np.array:
        raise NotImplementedError

    return(GlossaryDict)

def DiseaseSearch(ReportDict, DiseaseGlossary):
    '''
    Function to iterate GetDisease over the text "column" of ReportDict

    Takes a dict of dicts that includes a 2nd order dict key "text"

    Returns dict of dicts with added Key "diseasematches" full of dicts {word:Match}
    '''

    for i in trange(len(ReportDict),
                    desc="Getting fuzzy diseaseGlossary matches         "):
        Matches = GetDisease(ReportDict[i]["text"], DiseaseGlossary)
        ReportDict[i]["diseasematches"] = Matches

    return (ReportDict)


def ProcessNormality():
    '''
    helper function to compile and analyse results of keywords search as applied to TUAB dataset
    '''

    AbnormalReports = CompileDemographicsAndText(mainPathAbnormal)
    AbnormalReports["DatasetNormal"] = "FALSE"
    NormalityDataframe = AbnormalReports

    NormalReports = CompileDemographicsAndText(mainPathNormal)
    NormalReports["DatasetNormal"] = "TRUE"
    NormalityDataframe = NormalityDataframe.append(NormalReports, ignore_index=True)

    NormalityDataframe.to_excel("NormalVsAbnormal.xlsx", sheet_name="Data", index=False)

    NormalityDict = KeyWordSearch(InputFile="NormalVsAbnormal.xlsx")

    NormalityDataframe = pd.DataFrame.from_dict(NormalityDict)
    NormalityDataframe = NormalityDataframe.transpose()

    i = 0

    TP = NormalityDataframe[NormalityDataframe.normality < i][
        NormalityDataframe.DatasetNormal == False].normality.count()
    TN = NormalityDataframe[NormalityDataframe.normality > i][
        NormalityDataframe.DatasetNormal == True].normality.count()
    FP = NormalityDataframe[NormalityDataframe.normality < i][
        NormalityDataframe.DatasetNormal == True].normality.count()
    FN = NormalityDataframe[NormalityDataframe.normality > i][
        NormalityDataframe.DatasetNormal == False].normality.count()

    Sens = TP / (TP + FN)
    Spec = TN / (TN + FP)
    NPV = TN / (TN + FN)

    print("With a threshold at ", i)
    print("Sens = ", Sens, "\nSpec = ", Spec, "\nNPV = ", NPV)

    import matplotlib.pyplot as plt

    PlotDF = pd.DataFrame({"Normal": NormalityDataframe[NormalityDataframe.DatasetNormal == True].normality,
                           "Abnormal": NormalityDataframe[NormalityDataframe.DatasetNormal == False].normality})
    plt.close('all')

    ax = PlotDF.plot.hist(alpha=0.5)

    plt.show()

    return ()


if __name__ == "__main__":
    print("Run parser")
    ReportDict = ReportSearch(GetKeywords = False)
    ReportDict = DiseaseSearch(ReportDict, MSDict)
    ReportDict = CheckMatches(ReportDict, column = "diseasematches")
    ReportDataframe = pd.DataFrame.from_dict(ReportDict)
    ReportDataframe = ReportDataframe.transpose()
    ReportDataframe.to_excel("MSSearchedDataframe.xlsx", sheet_name="Data", index=False)

