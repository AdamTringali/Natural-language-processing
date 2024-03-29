#!/usr/bin/python3

# !/usr/bin/python3
# CSE354 Sp20; Assignment 1 Template v02
##################################################################
_version_ = 0.2

import sys

##################################################################
# 1. Tokenizer

import re  # python's regular expression package


def tokenize(sent):
    # input: a single sentence as a string.
    # output: a list of each "word" in the text
    # must use regular expressions

    tokens = []
    # <FILL IN>

#    _=)($%^*  <--- handle?
#   ascii ! - @
    tokens = re.findall(r'(?:[A-Za-z0-9\'!-@#-]+[^. ?!]+)|(?:[A-Z\.])+|(?:[!|?|\.])|(?:[a-z0-9]+)', sent)

    return tokens


##################################################################
# 2. Pig Latinizer

def pigLatinizer(tokens):
    # input: tokens: a list of tokens,
    # output: plTokens: tokens after transforming to pig latin

    plTokens = []
    # <FILL IN>

    for token in tokens:
        if(token[0] == 'a' or token[0] == 'e' or token[0] == 'i' or token[0] == 'o' or token[0] == 'u' or token[0] == 'A'
                or token[0] == 'E' or token[0] == 'I' or token[0] == 'O' or token[0] == 'U'):
            plTokens.append(token + 'way')
        else:
            if token[0].isalpha():
                x = 0
                for ch in token:
                    if (ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u'
                            or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
                        plTokens.append(token[x:] + token[0:x] + 'ay')
                        break
                    else:
                        if x == len(token)-1:
                            plTokens.append(token + "ay")
                    x = x+1
            else:
                plTokens.append(token)

    return plTokens


##################################################################
# 3. Feature Extractor

import numpy as np
np.set_printoptions(threshold=sys.maxsize)


def getFeaturesForTokens(tokens, wordToIndex):
    # input: tokens: a list of tokens,
    # wordToIndex: dict mapping 'word' to an index in the feature list.
    # output: list of lists (or np.array) of k feature values for the given target

    num_words = len(tokens)

    previousVector = []
    currentVector = []
    nextVector = []

    for y in range(len(wordToIndex)):
        previousVector.append(0)
        currentVector.append(0)
        nextVector.append(0)

    featuresPerTarget = list()
    for targetI in range(num_words):
        # <FILL IN>

        if targetI > 0:
            previousVector[wordToIndex[tokens[targetI-1].lower()]] = 1

        currentVector[wordToIndex[tokens[targetI].lower()]] = 1

        if targetI+1 < num_words:
            nextVector[wordToIndex[tokens[targetI+1].lower()]] = 1


        vowels = 0
        constants = 0
        for ch in tokens[targetI]:
            if (ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u'
                    or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U' or ch == 'y' or ch == 'Y'):
                vowels = vowels + 1
            elif ch.isalpha():
                constants = constants + 1

        fullVector = [vowels] + [constants] + previousVector + currentVector + nextVector

        featuresPerTarget.append(fullVector)

    return featuresPerTarget  # a (num_words x k) matrix


##################################################################
# 4. Adjective Classifier

from sklearn.linear_model import LogisticRegression


def trainAdjectiveClassifier(features, adjs):
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

    # inputs: features: feature vectors (i.e. X)
    #        adjs: whether adjective or not: [0, 1] (i.e. y)
    # output: model -- a trained sklearn.linear_model.LogisticRegression object
   # print(features)

    Cs = [.001, .01, .1, 1, 10, 100, 1000, 10000, 100000]
    # X_train, X_test, y_train, y_test
    train_x, dev_x, train_y, dev_y = train_test_split(features, adjs, test_size=0.10, random_state=42)
    bestAccuracy = 0.0
    bestModel = None
    for c in Cs:  # c values:
        model = LogisticRegression(penalty='l1', solver='liblinear', C=c)
        model.fit(train_x, train_y)
        pred_y = model.predict(dev_x)

        # compute accuracy:
        length = len(dev_y)

        # print("test n: ", leny)
        # acc = np.sum([1 if (y_pred[i] == y_test[i]) else 0 for i in range(leny)]) / leny
        accuracy = np.sum([1 if (pred_y[i] == dev_y[i]) else 0 for i in range(length)]) / length
        print("Accuracy: %.4f" % accuracy)

        if accuracy > bestAccuracy:
            bestModel = model
            bestAccuracy = accuracy

    return bestModel
    # <FILL IN>


##################################################################
##################################################################
## Main and provided complete methods
## Do not edit.
## If necessary, write your own main, but then make sure to replace
## and test with this before you submit.
##
## Note: Tests below will be a subset of those used to test your
##       code for grading.

def getConllTags(filename):
    # input: filename for a conll style parts of speech tagged file
    # output: a list of list of tuples
    #        representing [[[word1, tag1], [word2, tag2]]]
    wordTagsPerSent = [[]]
    sentNum = 0
    with open(filename, encoding='utf8') as f:
        for wordtag in f:
            wordtag = wordtag.strip()
            if wordtag:  # still reading current sentence
                (word, tag) = wordtag.split("\t")
                wordTagsPerSent[sentNum].append((word, tag))
            else:  # new sentence
                wordTagsPerSent.append([])
                sentNum += 1
    return wordTagsPerSent


# Main
if __name__ == '__main__':
    print("Initiating test. Version ", _version_)
    # Data for 1 and 2
    testSents = [ 'I am attending NLP class 2 days a week at ##S.B.U. this Spring.',
               # "stony brook NLP",
               #  "Daaammmmn. Florida got too many tolls.. Coach comin outta pocket every 5 mins -_-",
                 "I don't think data-driven computational linguistics is very tough.",
                 '@mybuddy and the drill begins again. #SemStart']

    # 1. Test Tokenizer:
    print("\n[ Tokenizer Test ]\n")
    tokenizedSents = []
    for s in testSents:
        tokenizedS = tokenize(s)
        print(s, tokenizedS, "\n")
        tokenizedSents.append(tokenizedS)

    # 2. Test Pig Latinizer:
    print("\n[ Pig Latin Test ]\n")
    for ts in tokenizedSents:
        print(ts, pigLatinizer(ts), "\n")

    # load data for 3 and 4 the adjective classifier data:
    taggedSents = getConllTags('daily547.conll')

    # 3. Test Feature Extraction:
    print("\n[ Feature Extraction Test ]\n")
    # first make word to index mapping:
    wordToIndex = set()  # maps words to an index
    for sent in taggedSents:
        if sent:
            words, tags = zip(*sent)  # splits [(w, t), (w, t)] into [w, w], [t, t]
            wordToIndex |= set([w.lower() for w in words])  # union of the words into the set
    print("  [Read ", len(taggedSents), " Sentences]")
    # turn set into dictionary: word: index
    wordToIndex = {w: i for i, w in enumerate(wordToIndex)}

    # Next, call Feature extraction per sentence
    sentXs = []
    sentYs = []
    print("  [Extracting Features]")
    for sent in taggedSents:
        if sent:
            words, tags = zip(*sent)
            sentXs.append(getFeaturesForTokens(words, wordToIndex))
            sentYs.append([1 if t == 'A' else 0 for t in tags])
    # test sentences
    print("\n", taggedSents[5], "\n", sentXs[5], "\n")
    print(taggedSents[192], "\n", sentXs[192], "\n")

    # 4. Test Classifier Model Building
    print("\n[ Classifier Test ]\n")
    # setup train/test:
    from sklearn.model_selection import train_test_split

    # flatten by word rather than sent:
    X = [j for i in sentXs for j in i]
    y = [j for i in sentYs for j in i]
    try:
        X_train, X_test, y_train, y_test = train_test_split(np.array(X),
                                                            np.array(y),
                                                            test_size=0.20,
                                                            random_state=42)
    except ValueError:
        print("\nLooks like you haven't implemented feature extraction yet.")
        print("[Ending test early]")
        sys.exit(1)
    print("  [Broke into training/test. X_train is ", X_train.shape, "]")
    # Train the model.
    print("  [Training the model]")
    tagger = trainAdjectiveClassifier(X_train, y_train)
    print("  [Done]")

    # Test the tagger.
    from sklearn.metrics import classification_report

    # get predictions:
    y_pred = tagger.predict(X_test)
    # compute accuracy:
    leny = len(y_test)
    print("test n: ", leny)
    acc = np.sum([1 if (y_pred[i] == y_test[i]) else 0 for i in range(leny)]) / leny
    print("Accuracy: %.4f" % acc)
#    print(classification_report(y_test, y_pred, ['not_adj', 'adjective']))


