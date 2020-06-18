import os


class ConfigLoader:

    def __init__(self):
        self.__sym_spell_iterations = 2
        self.__query_count_threshold = 5
        self.__high_frequency_threshold = 0.75
        self.__max_total_queries = 500000000
        self.__output_directory_name = "/output"
        self.__input_directory_name = "/input"
        self.__base_path = os.getcwd()
        self.__synonyms_file_path = self.__base_path + self.__input_directory_name + "/synonyms.txt"
        self.__profane_words_file_path = self.__base_path + self.__input_directory_name + "/bad_words.txt"
        self.__stop_words_file_path = self.__base_path + self.__input_directory_name + "/stopwords.txt"
        self.__query_logs_file_path = self.__base_path + self.__input_directory_name + "/query_logs.txt"
        self.__frequency_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_original_queries.csv"
        self.__dictionary_file_path = \
            self.__base_path + self.__output_directory_name + "/processed_queries.csv"
        self.__sym_spell_filtered_file_path = \
            self.__base_path + self.__output_directory_name + "/sym_spell_corrected_queries"
        self.__filtered_profane_queries_file_path = \
            self.__base_path + self.__output_directory_name + "/filtered_profane_queries.csv"
        self.__de_duplicated_keyword_ordered_1_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_keyword_ordered_1.csv"
        self.__de_duplicated_keyword_ordered_2_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_keyword_ordered_2.csv"
        self.__de_duplicated_missing_space_1_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_missing_space_1.csv"
        self.__de_duplicated_missing_space_2_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_missing_space_2.csv"
        self.__de_duplicated_synonyms_1_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_synonyms_1.csv"
        self.__de_duplicated_synonyms_2_file_path = \
            self.__base_path + self.__output_directory_name + "/de_duplicated_synonyms_2.csv"

    def get_profane_words_file_path(self):
        return self.__profane_words_file_path

    def get_filtered_profane_queries_file_path(self):
        return self.__filtered_profane_queries_file_path

    def get_stop_words_file_path(self):
        return self.__stop_words_file_path

    def get_query_count_threshold(self):
        return self.__query_count_threshold

    def get_query_logs_file_path(self):
        return self.__query_logs_file_path

    def get_high_frequency_threshold(self):
        return self.__high_frequency_threshold

    def get_frequency_file_path(self):
        return self.__frequency_file_path

    def get_max_total_queries(self):
        return self.__max_total_queries

    def get_de_duplicated_keyword_ordered_1_file_path(self):
        return self.__de_duplicated_keyword_ordered_1_file_path

    def get_de_duplicated_keyword_ordered_2_file_path(self):
        return self.__de_duplicated_keyword_ordered_2_file_path

    def get_de_duplicated_missing_space_1_file_path(self):
        return self.__de_duplicated_missing_space_1_file_path

    def get_de_duplicated_missing_space_2_file_path(self):
        return self.__de_duplicated_missing_space_2_file_path

    def get_de_duplicated_synonyms_1_file_path(self):
        return self.__de_duplicated_synonyms_1_file_path

    def get_de_duplicated_synonyms_2_file_path(self):
        return self.__de_duplicated_synonyms_2_file_path

    def get_dictionary_file_path(self):
        return self.__dictionary_file_path

    def get_sym_spell_filtered_file_path(self):
        return self.__sym_spell_filtered_file_path

    def get_sym_spell_iterations(self):
        return self.__sym_spell_iterations

    def get_output_directory_name(self):
        return self.__output_directory_name

    def get_input_directory_name(self):
        return self.__input_directory_name

    def get_base_path(self):
        return self.__base_path

    def get_synonyms_file_path(self):
        return self.__synonyms_file_path
