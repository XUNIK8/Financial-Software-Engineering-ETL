import logging
import pandas as pd
import os
from fall2022py.utils.misc_util import log_trace


@ log_trace
def read(description, path, file_type='excel', separator=',', skip_rows=0, use_cols=None, sheet_name=0, fill_nan=False):
    """
    Read file, along with validating provided path.
    :param description: str; File description
    :param path: str; Fully qualified file name to read
    :param file_type: str, default='Excel'; Read type with possible values of 'csv' or 'excel'
    :param separator: str, default=','; Values separator
    :param skip_rows: int, default=0; Number of rows to skip
    :param use_cols: int, default=None; A list of columns to read (all others are discarded)
    :param sheet_name: int or str; default=0; A sheet name or index to read
    :return: pd.DataFrame; Resulted dataframe
    """
    df_target = None
    if validate_path(path, True):
        if file_type.lower() == 'csv':
            # Read csv based file.
            df_target = pd.read_csv(path, sep=separator, skiprows=skip_rows, usecols=use_cols)
        elif file_type.lower() == 'excel':
            # Read Excel based file.
            if len((pd.ExcelFile(path)).sheet_names) > 1:
                df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols, sheet_name=sheet_name)
            else:
                df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols)

    # Fill nan as 0 if the fill_nan setting in configuration file is True
    if fill_nan:
        df_target.fillna(value=0.0, axis=1, inplace=True)

    logging.info(f'{description} records <{len(df_target.index)}> were read from <{path}>')
    return df_target


@ log_trace
def validate_path(path, is_path):
    """
    Validate provided path.
    :param path: Fully qualified file path
    :param path: bool; True if it is path, False if it is directory
    :return: bool; Resulted validation; either true or raise an exception
    """
    if is_path:
        if not os.path.isfile(path):
            logging.error(f'Provided file path is invalid: <{path}>')
            raise FileNotFoundError(f'Provided file path is invalid: <{path}>')
    else:
        if not os.path.isdir(path):
            logging.error(f'Provided directory path is invalid: <{path}>')
            raise FileNotFoundError(f'Provided directory path is invalid: <{path}>')
    return True


@ log_trace
def write(df, path, file_type, separator, mode):
    """
    Write an Excel/Csv file, based on given dataframe
    :param df: pd.DataFrame; Target dataframe
    :param path: str; Fully qualified file name to write
    :param file_type: str; str, default='Excel'; Read type with possible values of 'csv' or 'excel'
    :param separator: str; default=','; Values separator
    :param mode: str; 'overwrite' or 'new'
    :return: None
    """
    def write_file(file_type, path):

        if file_type == 'csv':
            df.to_csv(path, sep=separator, index = False)

        elif file_type == 'excel':
            df.to_excel(path, index = False)
        
        else:
            raise KeyError("File type can only be 'csv' or 'excel'")

    file_full_name = os.path.basename(path)
    dir_name = os.path.dirname(path)
    
    if validate_path(dir_name, False):
        
        if mode == 'overwrite':
            write_file(file_type, path)

        elif mode == 'new':
            suffix_num = 1
            file_name, suffix = file_full_name.split('.')
            
            while os.path.isfile(path):
                file_name += "_" + str(suffix_num)
                file_full_name_new = file_name + '.' + suffix
                suffix_num += 1
            
            path_new = os.path.join(dir_name,'/',file_full_name_new)
            write_file(file_type, path_new)

        else:
            raise KeyError("Mode can only be 'new' or 'overwrite'")
            