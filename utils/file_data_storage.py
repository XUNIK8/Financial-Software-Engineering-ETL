import pandas as pd
import fall2022py.utils.misc_util as miscu
import logging
import os
from fall2022py.utils.data_storage import DataStorage


class FileDataStorage(DataStorage):
    """
    Concrete class to read and write csv or excel files, inherited from DataStorage.
    Override read and write functions.
    """
    def __init__(self, description):
        super(FileDataStorage, self).__init__(description)


    @staticmethod
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


    def read(self, config):
        """
        Read file, along with validating provided path.
        :param config: dict; Configuaration dictionary
        :return: pd.DataFrame; Resulted dataframe
        """
        description = miscu.eval_elem_mapping(config, 'description')
        path = miscu.eval_elem_mapping(config, 'path')
        file_type = miscu.eval_elem_mapping(config, 'file_type', default_value='excel')
        separator = miscu.eval_elem_mapping(config, 'separator', default_value=',')
        skip_rows = miscu.eval_elem_mapping(config, 'skip_rows', default_value=0)
        use_cols = miscu.eval_elem_mapping(config, 'use_cols')
        sheet_name = miscu.eval_elem_mapping(config, 'sheet_name', default_value=0)

        df_target = None
        if self.validate_path(path, True):
            if file_type.lower() == 'csv':
                # Read csv based file.
                df_target = pd.read_csv(path, sep=separator, skiprows=skip_rows, usecols=use_cols)
            elif file_type.lower() == 'excel':
                # Read Excel based file.
                if len((pd.ExcelFile(path)).sheet_names) > 1:
                    df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols, sheet_name=sheet_name)
                else:
                    df_target = pd.read_excel(path, skiprows=skip_rows, usecols=use_cols)

        logging.info(f'{description} records <{len(df_target.index)}> were read from <{path}>')
        return df_target


    def write(self, df, config):
        """
        Write an Excel/Csv file, based on given dataframe
        :param df: pd.DataFrame; Target dataframe to save
        :param config: dict; Configuration dictionary
        :return: None
        """
        path = miscu.eval_elem_mapping(config, 'path')
        file_type = miscu.eval_elem_mapping(config, 'file_type')
        separator = miscu.eval_elem_mapping(config, 'separator')
        mode = miscu.eval_elem_mapping(config, 'mode')

        # Write file helper
        def write_file(file_type, path):

            if file_type == 'csv':
                df.to_csv(path, sep=separator, index = False)

            elif file_type == 'excel':
                df.to_excel(path, index = False)
            
            else:
                raise KeyError("File type can only be 'csv' or 'excel'")

        # Get file name and directory name
        file_full_name = os.path.basename(path)
        dir_name = os.path.dirname(path)
        
        if self.validate_path(dir_name, False):
            
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
