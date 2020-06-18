from config_loader import ConfigLoader
from parser import Parser


class ProfanityFilter:

    def __init__(self, config_loader: ConfigLoader, parser: Parser):
        self.__profane_words = set()
        self.__parser = parser
        self.__load_profane_words(config_loader.get_profane_words_file_path())

    def __load_profane_words(self, profane_words_file):
        file = open(profane_words_file, "r")
        for line in file:
            self.__profane_words.add(line.rstrip())

        file.close()

    def __is_profane(self, query):
        keywords = query.split(" ")
        for keyword in keywords:
            if keyword in self.__profane_words:
                return True

        return False

    def remove_profane_queries(self, input_file, output_file, output_profane_file):
        file = open(input_file, "r")
        profane_queries_file = open(output_profane_file, "w")
        dictionary = {}
        for line in file:
            (query, count) = line.rstrip().split(",")
            if not self.__is_profane(query):
                dictionary[query] = count
            else:
                profane_queries_file.write(line)

        file.close()
        profane_queries_file.close()

        self.__parser.write_dictionary_to_file(dictionary, output_file)
