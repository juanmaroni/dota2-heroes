from  os import makedirs, path, rename


CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
TMP_HEROES_INFO_FILENAME = "dota2_heroes_info_tmp.csv"
TMP_HEROES_TALENTS_FILENAME = "dota2_heroes_talents_tmp.csv"
OUTPUT_DIR_PATH = "../output/"

def change_filepath(filename, new_filename, new_dir_path=OUTPUT_DIR_PATH):
    new_path = path.join(new_dir_path, new_filename)
    makedirs(new_dir_path, exist_ok=True)
    rename(filename, new_path)
