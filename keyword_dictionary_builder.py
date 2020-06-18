from parser import Parser


class KeywordDictionaryBuilder:

    def __init__(self, parser: Parser):
        self.__parser = parser

    def build_dictionary_file_from_frequency_file(self, input_file, output_file, min_length=3):
        updated_dictionary = {}
        file = open(input_file, "r")
        for line in file:
            (query, count) = line.split(",")
            terms = query.split(" ")
            for term in terms:
                if len(term) >= min_length and not term.isnumeric():
                    updated_dictionary[term] = updated_dictionary.get(term, 0) + int(count)

        file.close()

        self.__parser.write_dictionary_to_file(updated_dictionary, output_file)
