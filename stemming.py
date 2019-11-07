import os
import porter_stemmer

stemmer = porter_stemmer.PorterStemmer()

posFiles = sorted(list(filter(lambda x: x.endswith(".tag"), os.listdir("./POS"))))
negFiles = sorted(list(filter(lambda x: x.endswith(".tag"), os.listdir("./NEG"))))


def perform_stemming(file_list, in_directory, out_directory):
    for f in file_list:
        i = open(in_directory + f, 'r')
        stems = ''

        while True:
            stemmedLine = ''
            word = ''
            line = i.readline()
            if line == '':
                break
            for char in line:
                if char.isalpha():
                    word += char.lower()
                else:
                    if word:
                        stemmedLine += stemmer.stem(word, 0, len(word) - 1)
                        word = ''
                    stemmedLine += char.lower()
            stems += stemmedLine

        o = open(out_directory + f, 'w')
        o.write(stems)

        i.close()


perform_stemming(posFiles, "./POS/", "./POS_STEMMED/")
perform_stemming(negFiles, "./NEG/", "./NEG_STEMMED/")
