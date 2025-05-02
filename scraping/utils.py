from  os import makedirs, path, rename


CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
TMP_FILENAME = "dota2_heroes_tmp.csv"
OUTPUT_DIR_PATH = "../output/"

def change_filepath(
        filename=TMP_FILENAME,
        new_dir_path=OUTPUT_DIR_PATH,
        new_filename=TMP_FILENAME
    ):
    new_path = path.join(new_dir_path, new_filename)
    makedirs(new_dir_path, exist_ok=True)
    rename(filename, new_path)
