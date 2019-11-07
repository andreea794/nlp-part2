import svmlight
from loader import options


def get_feature_indices(data_set):
    feature_indices = {}
    index = 1
    for (sentiment, file_name, features) in data_set:
        for w in features:
            if w not in feature_indices:
                feature_indices[w] = index
                index += 1
    print 'Word count: ' + str(len(feature_indices))
    return feature_indices


def svm(training_set, test_set):
    feature_indices = get_feature_indices(training_set + test_set)

    formatted_training_set = []
    formatted_test_set = []

    for (sentiment, file_name, features) in training_set:
        feature_vec = []
        feature_freqs = {}

        for w in features:
            if options["usePresence"] or w not in feature_freqs:
                feature_freqs[w] = 1
            else:
                feature_freqs[w] += 1

        for word, count in feature_freqs.items():
            feature_vec.append((feature_indices[word], count))

        list.sort(feature_vec, key=lambda x: x[0])

        sent_val = 1 if sentiment == "POS" else -1
        formatted_training_set.append((sent_val, feature_vec))

    model = svmlight.learn(formatted_training_set)

    for (sentiment, file_name, features) in test_set:
        feature_vec = []
        feature_freqs = {}

        for w in features:
            if w not in feature_freqs:
                feature_freqs[w] = 1
            else:
                feature_freqs[w] += 1

        for word, count in feature_freqs.items():
            feature_vec.append((feature_indices[word], count))

        list.sort(feature_vec, key=lambda x: x[0])
        formatted_test_set.append((0, feature_vec))

    predictions = svmlight.classify(model, formatted_test_set)

    formatted_predictions = []
    idx = 0
    for (sentiment, file_name, features) in test_set:
        formatted_predictions.append(("POS" if predictions[idx] > 0 else "NEG", sentiment, file_name))
        idx += 1
    return formatted_predictions
