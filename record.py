import pandas as pd
import os


def new_file(path):
    if not os.path.isfile(path):
        f = open(path, 'x')
        f.close()
    else:
        file = open(path, "r+")
        file.truncate(0)
        file.close()


def append_file(path, result_txt):
    with open(path, "a") as f:
        f.write(result_txt+"\n")


def record(game_result, df, cols):
    result_df = pd.DataFrame([game_result], columns=cols)
    return pd.concat([df, result_df], ignore_index=True)


