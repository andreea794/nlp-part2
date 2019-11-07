from math import log
from loader import options


def calculate_class_probs(training_set):
    pos_count = 0
    neg_count = 0

    for (sentiment, file_name, features) in training_set:
        if sentiment == "POS":
            pos_count += 1
        else:
            neg_count += 1

    return float(pos_count) / float(pos_count + neg_count), float(neg_count) / float(pos_count + neg_count)


def calculate_log_probs(training_set):
    freqs = {}
    log_probs = {}
    # Total number of positive and negative words
    pos_words = 0
    neg_words = 0

    for (sentiment, file_name, features) in training_set:
        if options["usePresence"]:
            # Transform the feature vector into a set i.e. one of each word
            feature_set = set(features)
            features = list(feature_set)

        for w in features:
            # Laplace smoothing: Add 1 to both the positive and the negative frequency of each word
            if w not in freqs:
                freqs[w] = (1, 1)

            (pos_freq, neg_freq) = freqs[w]
            if sentiment == "POS":
                freqs[w] = (pos_freq + 1, neg_freq)
                pos_words += 1
            else:
                freqs[w] = (pos_freq, neg_freq + 1)
                neg_words += 1

    # Laplace smoothing
    pos_words += len(freqs)
    neg_words += len(freqs)

    print "Feature count: " + str(len(freqs))

    for w in freqs:
        (pos_freq, neg_freq) = freqs[w]
        pos_prob = float(pos_freq) / float(pos_words)
        neg_prob = float(neg_freq) / float(neg_words)
        log_probs[w] = (log(pos_prob), log(neg_prob))

    return log_probs


def naive_bayes(training_set, test_set):
    class_probs = calculate_class_probs(training_set)
    feature_log_probs = calculate_log_probs(training_set)

    predicted_sentiments = []

    for (sentiment, file_name, features) in test_set:
        pos_prob = log(class_probs[0])
        neg_prob = log(class_probs[1])

        for w in features:
            if w in feature_log_probs:
                pos_prob += feature_log_probs[w][0]
                neg_prob += feature_log_probs[w][1]

        if pos_prob >= neg_prob:
            predicted_sentiments.append(("POS", sentiment, file_name))
        else:
            predicted_sentiments.append(("NEG", sentiment, file_name))

    return predicted_sentiments