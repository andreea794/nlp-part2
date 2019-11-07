import math
from scipy.stats import binom


def sign_test(predictions1, predictions2):
    # Sort by file name, so the files match
    list.sort(predictions1, key=lambda x: x[2])
    list.sort(predictions2, key=lambda x: x[2])

    plus = 0
    minus = 0
    null = 0

    correct_count1 = 0
    correct_count2 = 0

    for i in range(0, len(predictions1)):
        (predicted1, actual1, file_name1) = predictions1[i]
        (predicted2, actual2, file_name2) = predictions2[i]

        if file_name1 != file_name2:
            print file_name1 + " and " + file_name2 + " don't match!"
            return

        if predicted1 == actual1 and predicted2 != actual2:
            # System 1 predicted correctly, but not system 2
            correct_count1 += 1
            plus += 1
        elif predicted1 != actual1 and predicted2 == actual2:
            # System 2 predicted correctly, but not system 1
            correct_count2 += 1
            minus += 1
        else:
            if (predicted1 == actual1):
                # Both systems predicted correctly
                correct_count1 += 1
                correct_count2 += 1
            null += 1

    print "System 1 accuracy: "
    print float(correct_count1) / float(len(predictions1))
    print "----------------------"

    print "System 2 accuracy: "
    print float(correct_count2) / float(len(predictions2))
    print "----------------------"

    print "Plus: " + str(plus)
    print "Minus: " + str(minus)
    print "Null: " + str(null)

    q = 0.5
    n = int(2 * (math.ceil(float(null) / 2.0)) + plus + minus)
    k = int(math.ceil(float(null) / 2.0) + min(plus, minus))
    return 2 * binom.cdf(k, n, 0.5)
