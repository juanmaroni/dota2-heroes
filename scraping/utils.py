from  os import makedirs, path, rename


CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
TMP_HEROES_INFO_FILENAME = "dota2_heroes_info_tmp.csv"
TMP_HEROES_TALENTS_FILENAME = "dota2_heroes_talents_tmp.csv"
TMP_HEROES_INNATE_FILENAME = "dota2_heroes_innate_tmp.csv"
OUTPUT_DIR_PATH = "../output"


def change_filepath(filename, new_filename, patch, base_dir_path=OUTPUT_DIR_PATH):
    new_path = path.join(base_dir_path, patch, new_filename)
    makedirs(f"{base_dir_path}/{patch}", exist_ok=True)
    rename(filename, new_path)
