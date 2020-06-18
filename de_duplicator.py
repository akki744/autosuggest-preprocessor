from parser import Parser
from nltk import PorterStemmer


class DeDuplicator:

    def __init__(self, parser: Parser):
        self.__stop_words = parser.get_stop_words()
        self.__synonyms = parser.get_synonyms()
        self.__parser = parser
        self.__stemmer = PorterStemmer()

    def __replace_with_synonyms(self, query):
        updated_query = ""
        for term in query.split(" "):
            if len(updated_query) > 0:
                updated_query += " "
            updated_query += self.__synonyms.get(term, term)
        return updated_query

    def __get_query_hash(self, query):
        terms = query.split(" ")
        updated_terms = []
        for term in terms:
            if term not in self.__stop_words:
                stemmed_term = self.__stemmer.stem(term) if len(term) > 1 and term.isalpha() else term
                updated_terms.append(stemmed_term)

        updated_terms.sort()

        return ":".join(list(dict.fromkeys(updated_terms)))

    def __remove_keyword_ordered_duplicates(self, input_file, output_file, deduplicated_queries_file):
        hashed_query_counts = {}
        dictionary_file = open(input_file, "r")
        for line in dictionary_file:
            (query, count) = line.split(",")
            hashed_query = self.__get_query_hash(query)
            prev = hashed_query_counts.get(hashed_query, ["", 0])
            if prev[1] < int(count):
                hashed_query_counts[hashed_query] = [query, int(count)]

        dictionary_file.close()

        dictionary_file = open(input_file, "r")
        filtered_queries_file = open(deduplicated_queries_file, "w")
        updated_dictionary = {}
        for line in dictionary_file:
            (query, count) = line.split(",")
            hashed_query = self.__get_query_hash(query)
            hashed_query_count = hashed_query_counts[hashed_query]
            updated_dictionary[hashed_query_count[0]] = updated_dictionary.get(hashed_query_count[0], 0) + int(count)
            if hashed_query_count[0] != query:
                filtered_queries_file.write(query + "," + hashed_query_count[0] + "\n")

        dictionary_file.close()
        filtered_queries_file.close()

        self.__parser.write_dictionary_to_file(updated_dictionary, output_file)

    def __remove_space(self, query):
        return "".join(query.split(" "))

    def __remove_missing_space_duplicates(self, input_file, output_file, deduplicated_queries_file):
        hashed_query_counts = {}
        dictionary_file = open(input_file, "r")
        for line in dictionary_file:
            (query, count) = line.split(",")
            hashed_query = self.__remove_space(query)
            prev = hashed_query_counts.get(hashed_query, ["", 0])
            if prev[1] < int(count):
                hashed_query_counts[hashed_query] = [query, int(count)]

        dictionary_file.close()

        dictionary_file = open(input_file, "r")
        filtered_queries_file = open(deduplicated_queries_file, "w")
        updated_dictionary = {}
        for line in dictionary_file:
            (query, count) = line.split(",")
            hashed_query = self.__remove_space(query)
            hashed_query_count = hashed_query_counts[hashed_query]
            updated_dictionary[hashed_query_count[0]] = updated_dictionary.get(hashed_query_count[0], 0) + int(count)
            if hashed_query_count[0] != query:
                filtered_queries_file.write(query + "," + hashed_query_count[0] + "\n")

        dictionary_file.close()
        filtered_queries_file.close()

        self.__parser.write_dictionary_to_file(updated_dictionary, output_file)

    def __remove_synonymous_duplicates(self, input_file, output_file, synonymous_duplicates_file):
        file = open(input_file, "r")
        filtered_queries_file = open(synonymous_duplicates_file, "w")
        dictionary = {}
        for line in file:
            (query, count) = line.split(",")
            original_query = query
            query = self.__replace_with_synonyms(query)
            if original_query != query:
                filtered_queries_file.write(original_query + "," + query + "\n")
            dictionary[query] = dictionary.get(query, 0) + int(count)
        file.close()
        filtered_queries_file.close()

        file = open(output_file, "w")
        for query in dictionary.keys():
            file.write(query + "," + str(dictionary[query]) + "\n")
        file.close()

    def remove_duplicates(self, input_file, output_file, keyword_ordered_duplicates_file, missing_space_duplicates_file,
                          synonymous_duplicates_file):
        self.__remove_keyword_ordered_duplicates(input_file, output_file, keyword_ordered_duplicates_file)
        self.__remove_missing_space_duplicates(output_file, output_file, missing_space_duplicates_file)
        self.__remove_synonymous_duplicates(output_file, output_file, synonymous_duplicates_file)
