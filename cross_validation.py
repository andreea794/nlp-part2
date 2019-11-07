from loader import *
import naive_bayes
import sign_test
import statistics
import svm

fold_count = 10


def round_robin_split(features):
    splits = []
    for i in range(0, fold_count):
        splits.append([])

    pos_features = features[0:1000]
    neg_features = features[1000:2000]

    for i in range(0, 1000):
        splits[i % fold_count].append(pos_features[i])
        splits[i % fold_count].append(neg_features[i])

    return splits


def predictions_for_index(splits, index, function):
    training_set = []
    test_set = []

    for i in range(0, len(splits)):
        if i == index:
            test_set = splits[i]
        else:
            training_set.extend(splits[i])

    if options["useCutoffs"]:
        feature_freqs = {}
        for (sentiment, file_name, features) in training_set:
            for w in features:
                if w not in feature_freqs:
                    feature_freqs[w] = 1
                else:
                    feature_freqs[w] += 1

        for i in range(0, len(training_set)):
            features_to_keep = []
            for w in training_set[i][2]:
                if feature_freqs[w] >= 3:
                    features_to_keep.append(w)

            # Rewrite each entry in the training set by cutting the feature set
            training_set[i] = (training_set[i][0], training_set[i][1], features_to_keep)

    return function(training_set, test_set)


def cross_validation_for_index(splits, index, function):
    predictions = predictions_for_index(splits, index, function)

    right_predictions = 0
    for i in range(0, len(predictions)):
        if predictions[i][0] == predictions[i][1]:
            right_predictions += 1

    return float(right_predictions) / float(len(predictions))


def cross_validation(splits, function):
    accuracies = []
    for i in range(0, len(splits)):
        accuracies.append(cross_validation_for_index(splits, i, function))
    return accuracies


def cross_validation_nb():
    features = get_features_from_reviews()
    splits = round_robin_split(features)
    accuracies = cross_validation(splits, naive_bayes.naive_bayes)
    print "Naive Bayes mean accuracy: " + str(statistics.mean(accuracies))


def cross_validation_svm():
    features = get_features_from_reviews()
    splits = round_robin_split(features)
    accuracies = cross_validation(splits, svm.svm)
    print "SVM mean accuracy: " + str(statistics.mean(accuracies))


def predictions_for_all_splits(splits, function):
    results = []
    for i in range(0, len(splits)):
        results.extend(predictions_for_index(splits, i, function))
    return results


def predictions_for_system(function):
    features = get_features_from_reviews()
    splits = round_robin_split(features)
    return predictions_for_all_splits(splits, function)


def compare(function1, function2):
    print "Comparing systems..."
    print "System 1:"
    # Set options for system 1 here
    # options["useUnigramsAndBigrams"] = True
    # options["usePresence"] = True
    # options["useStemming"] = True
    options["useCutoffs"] = True
    predictions1 = predictions_for_system(function1)

    print "System 2:"
    # Set options for system 2 here
    # options["useUnigramsAndBigrams"] = True
    # options["usePresence"] = True
    # options["useStemming"] = True
    options["useCutoffs"] = True
    predictions2 = predictions_for_system(function2)

    p_val = sign_test.sign_test(predictions1, predictions2)

    print "p-value: " + str(p_val)

print "Options: "
print options
print ""
# compare(naive_bayes.naive_bayes, naive_bayes.naive_bayes)
compare(naive_bayes.naive_bayes, svm.svm)
