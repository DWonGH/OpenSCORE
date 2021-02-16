'''
Program that reads the text data from Temple dataset files and then pulls out:
1. Demographics - done "on the fly" in a per file manner
2. Keywords - will be done across whole dataset in a computer intensive manner
'''

import os
import pickle
from difflib import SequenceMatcher

import winsound


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

