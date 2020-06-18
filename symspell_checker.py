from config_loader import ConfigLoader
from parser import Parser
from symspellpy import SymSpell, Verbosity
from nltk.corpus import words


class SymSpellChecker:

    def __init__(self, config_loader: ConfigLoader, parser: Parser):
        self.__high_frequency_threshold = config_loader.get_high_frequency_threshold()
        self.__parser = parser
        self.__sym_spell_filtered_file_path = config_loader.get_sym_spell_filtered_file_path()
        self.__sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        self.__english_dictionary = set(words.words())

    def __get_best_suggestion_term(self, suggestions, split_term):
        res = suggestions[0]

        for suggestion in suggestions:
            if suggestion._count > res._count:
                res = suggestion

        if suggestions[0]._term == split_term and suggestions[0]._count >= res._count * self.__high_frequency_threshold:
            return split_term

        return res._term

    def __load_sym_spell_dictionary(self, dictionary_file):
        self.__sym_spell.load_dictionary(dictionary_file, term_index=0, count_index=1, separator=',')

    def __sym_spell_lookup(self, input_term):
        return self.__sym_spell.lookup(input_term, Verbosity.ALL, max_edit_distance=1, include_unknown=True)

    def __sym_spell_step(self, input_file, output_file, filter_file):
        updated_dictionary = {}
        file = open(filter_file, "w")
        queries_file = open(input_file, "r")
        for line in queries_file:
            (input_term, frequency) = line.split(",")
            split_terms = input_term.split(" ")
            best_suggested_query = ""
            for split_term in split_terms:
                if len(split_term) > 2 and split_term.isalpha() \
                        and split_term not in self.__english_dictionary:
                    suggestions = self.__sym_spell_lookup(split_term)
                    suggestion = self.__get_best_suggestion_term(suggestions, split_term)
                else:
                    suggestion = split_term

                if len(best_suggested_query) > 0:
                    best_suggested_query += " "
                best_suggested_query += suggestion

            updated_dictionary[best_suggested_query] = updated_dictionary.get(best_suggested_query, 0) + int(frequency)
            if input_term != best_suggested_query:
                file.write(input_term + "," + best_suggested_query + "," + frequency)

        file.close()
        queries_file.close()

        self.__parser.write_dictionary_to_file(updated_dictionary, output_file)

    def run_sym_spell(self, iterations, input_file, output_file, sym_spell_dictionary_file):
        self.__load_sym_spell_dictionary(sym_spell_dictionary_file)
        file_name = self.__sym_spell_filtered_file_path
        self.__sym_spell_step(input_file, output_file, file_name + "1.csv")
        for i in range(iterations):
            self.__sym_spell_step(output_file, output_file, file_name + str(i + 2) + ".csv")
