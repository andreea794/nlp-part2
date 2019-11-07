import os

options = {
    "useStemming": False,
    "useBigrams": False,
    "useUnigramsAndBigrams": False,
    "usePresence": False,
    "useCutoffs": False,
}


def get_features(file_path):
    with open(file_path) as f:
        content = f.read()
        features = content.split("\n")

    filtered_features = list(filter(lambda x: x != '', features))

    if options["useBigrams"] or options["useUnigramsAndBigrams"]:
        bigrams = []

        for i in range(0, len(filtered_features) - 1):
            bigrams.append(filtered_features[i] + ":" + filtered_features[i + 1])

        if options["useUnigramsAndBigrams"]:
            filtered_features.extend(bigrams)
            return filtered_features
        return bigrams

    return filtered_features


def get_features_from_reviews():
    pos_path = "./POS_STEMMED" if options["useStemming"] else "./POS"
    neg_path = "./NEG_STEMMED" if options["useStemming"] else "./NEG"

    if options["useBigrams"]:
        print "[Using bigrams]"
    elif options["useUnigramsAndBigrams"]:
        print "[Using unigrams and bigrams]"
    else:
        print "[Using unigrams]"

    if options["useStemming"]:
        print "[Stemming on]"
    else:
        print "[Stemming off]"

    if options["usePresence"]:
        print "[Using presence]"
    else:
        print "[Using frequency]"

    if options["useCutoffs"]:
        print "[Using cutoff 3]"
    else:
        print "[No cutoff]"

    print "----------------------"

    pos_files = sorted(list(filter(lambda x: x.endswith(".tag"), os.listdir(pos_path))))
    neg_files = sorted(list(filter(lambda x: x.endswith(".tag"), os.listdir(neg_path))))

    features = []

    for f in pos_files:
        features.append(("POS", f, get_features(pos_path + "/" + f)))

    for f in neg_files:
        features.append(("NEG", f, get_features(neg_path + "/" + f)))

    return features
