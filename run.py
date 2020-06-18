from time import time
from parser import Parser
from config_loader import ConfigLoader
from profanity_filter import ProfanityFilter
from de_duplicator import DeDuplicator
from keyword_dictionary_builder import KeywordDictionaryBuilder
from symspell_checker import SymSpellChecker
import os


def main():
    start_time = time()

    print("Running Basic Setup Steps....")
    config_loader = ConfigLoader()
    output_directory_path = config_loader.get_base_path() + config_loader.get_output_directory_name()
    if not os.path.exists(output_directory_path):
        os.makedirs(output_directory_path)
    parser = Parser(config_loader)
    profanity_filter = ProfanityFilter(config_loader, parser)
    de_duplicator = DeDuplicator(parser)
    keyword_dictionary_builder = KeywordDictionaryBuilder(parser)
    sym_spell_checker = SymSpellChecker(config_loader, parser)

    print("Running Parser....")
    parser.parse(config_loader.get_query_logs_file_path(), config_loader.get_frequency_file_path(),
                 config_loader.get_max_total_queries())

    print("Running De-duplicator....")
    de_duplicator.remove_duplicates(config_loader.get_frequency_file_path(), config_loader.get_frequency_file_path(),
                                    config_loader.get_de_duplicated_keyword_ordered_1_file_path(),
                                    config_loader.get_de_duplicated_missing_space_1_file_path(),
                                    config_loader.get_de_duplicated_synonyms_1_file_path())

    print("Running Profanity Filter....")
    profanity_filter.remove_profane_queries(config_loader.get_frequency_file_path(),
                                            config_loader.get_frequency_file_path(),
                                            config_loader.get_filtered_profane_queries_file_path())

    print("Running Keyword Dictionary Builder....")
    keyword_dictionary_builder.build_dictionary_file_from_frequency_file(config_loader.get_frequency_file_path(),
                                                                         config_loader.get_dictionary_file_path())

    print("Running SymSpell Checker....")
    sym_spell_checker.run_sym_spell(config_loader.get_sym_spell_iterations(), config_loader.get_frequency_file_path(),
                                    config_loader.get_dictionary_file_path(), config_loader.get_dictionary_file_path())

    print("Running De-duplicator....")
    de_duplicator.remove_duplicates(config_loader.get_dictionary_file_path(), config_loader.get_dictionary_file_path(),
                                    config_loader.get_de_duplicated_keyword_ordered_2_file_path(),
                                    config_loader.get_de_duplicated_missing_space_2_file_path(),
                                    config_loader.get_de_duplicated_synonyms_2_file_path())

    print("Completed!!!")

    print("Total time taken: ", (time() - start_time) / 60, " minutes")


if __name__ == "__main__":
    main()
