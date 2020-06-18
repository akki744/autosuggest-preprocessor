from config_loader import ConfigLoader


class Parser:

    def __init__(self, config_loader: ConfigLoader):
        self.__alphanumeric_list = {
            'a': 1, 'b': 1, 'c': 1, 'd': 1,
            'e': 1, 'f': 1, 'g': 1, 'h': 1,
            'i': 1, 'j': 1, 'k': 1, 'l': 1,
            'm': 1, 'n': 1, 'o': 1, 'p': 1,
            'q': 1, 'r': 1, 's': 1, 't': 1,
            'u': 1, 'v': 1, 'w': 1, 'x': 1,
            'y': 1, 'z': 1,
            'A': 1, 'B': 1, 'C': 1, 'D': 1,
            'E': 1, 'F': 1, 'G': 1, 'H': 1,
            'I': 1, 'J': 1, 'K': 1, 'L': 1,
            'M': 1, 'N': 1, 'O': 1, 'P': 1,
            'Q': 1, 'R': 1, 'S': 1, 'T': 1,
            'U': 1, 'V': 1, 'W': 1, 'X': 1,
            'Y': 1, 'Z': 1,
            '0': 1, '1': 1, '2': 1, '3': 1,
            '4': 1, '5': 1, '6': 1, '7': 1,
            '8': 1, '9': 1
        }
        self.__stop_words = self.__load_stop_words(config_loader.get_stop_words_file_path())
        self.__synonyms = self.__load_synonyms(config_loader.get_synonyms_file_path())
        self.__query_count_threshold = config_loader.get_query_count_threshold()

    def __filter_queries_less_than_threshold(self, dictionary, threshold):
        filtered_dictionary = {}
        for x in dictionary.keys():
            if dictionary[x] >= threshold:
                filtered_dictionary[x] = dictionary[x]

        return filtered_dictionary

    def __get_normalised_query(self, line):
        query = line.split(",")[0].replace("\"", "").lower()
        query = self.__remove_special_characters(query)
        query = self.__convert_multiple_spaces_to_one(query)
        return query

    def parse(self, input_file, output_file, total_queries):
        file = open(input_file, "r")
        curr_query_cnt = 0
        dictionary = {}
        for line in file:
            query = self.__get_normalised_query(line)
            if len(query) > 0:
                dictionary[query] = dictionary.get(query, 0) + 1

            curr_query_cnt += 1
            if curr_query_cnt > total_queries:
                break
        file.close()

        dictionary = self.__filter_queries_less_than_threshold(dictionary, self.__query_count_threshold)

        self.write_dictionary_to_file(dictionary, output_file)

    def write_dictionary_to_file(self, dictionary, output_file):
        file = open(output_file, "w")
        for term in sorted(dictionary.items(), key=lambda item: item[1], reverse=True):
            if len(term[0]) > 1 and term[0] not in self.__stop_words:
                file.write(term[0] + "," + str(term[1]) + "\n")

        file.close()

    def __load_stop_words(self, stopwords_file_path: str):
        stop_words = set()
        stop_words_file = open(stopwords_file_path, "r")
        for stop_word in stop_words_file:
            stop_word = stop_word.lower().strip()
            stop_words.add(stop_word)
        stop_words_file.close()

        return stop_words

    def __load_synonyms(self, synonyms_file_path: str):
        synonyms = {}
        synonyms_file = open(synonyms_file_path, "r")
        for line in synonyms_file:
            (incorrect_term, correct_term) = line.strip().split(",")
            synonyms[incorrect_term] = correct_term
        synonyms_file.close()

        return synonyms

    def __is_alnum(self, ch):
        return self.__alphanumeric_list.get(ch, 0) == 1

    def __convert_multiple_spaces_to_one(self, query):
        size = len(query)
        i = 0
        curr = ""
        ans = ""
        for i in range(size):
            if query[i] == " ":
                if len(curr) > 0:
                    if len(ans) > 0:
                        ans += " "
                    ans += curr
                    curr = ""
            else:
                curr += query[i]

        if len(curr) > 0:
            if len(ans) > 0:
                ans += " "
            ans += curr

        return ans

    def __remove_special_characters(self, query):
        res = ""
        for x in query:
            if self.__is_alnum(x):
                res += x
            else:
                res += " "

        return res

    def filter_query(self, query):
        query = self.__remove_special_characters(query.lower())
        query = self.__convert_multiple_spaces_to_one(query)
        return query

    def get_stop_words(self):
        return self.__stop_words

    def get_synonyms(self):
        return self.__synonyms
