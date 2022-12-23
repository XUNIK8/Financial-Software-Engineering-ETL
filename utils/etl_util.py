import pandas as pd
import numpy as np
import fall2022py.utils.file_util as fileu
import fall2022py.utils.misc_util as miscu
from fall2022py.utils.misc_util import log_trace
from fall2022py.utils.file_data_storage import FileDataStorage


@ log_trace
def apply_dtype_feature(df, config):
    """
    ETL feature to apply data types to dataframe columns and limit columns to ones specified
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    Sample:
    "apply_dtype": {
        "INSURANCE_CODE": "str",
        "INSURANCE_AMOUNT": "float",
        "CLIENT_TYPE": "int"
    }
    """
    if config and isinstance(config, dict):
        for column_key, type_value in config.items():
            if column_key in df:
                # str type.
                if type_value is str or type_value == 'str':
                    df[column_key] = df[column_key].fillna('')
                    df[column_key] = df[column_key].astype(str)
                # int type.
                elif type_value is int or type_value == 'int':
                    df[column_key] = df[column_key].fillna(0)
                    df[column_key] = df[column_key].astype(int)
                # float type.
                elif type_value is float or type_value == 'float':
                    df[column_key] = df[column_key].fillna(0.0)
                    df[column_key] = df[column_key].astype(float)
                # TODO: Implement datetime.date type
            else:
                raise KeyError(f'Column <{column_key}> is missing from given dataframe')
    return df


@ log_trace
def mapping_feature(df, config):
    """
    ETL feature to merge given dataframe with extracted mapping dataframe
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    df_mapping = read_feature(config['read'])

    df_target = pd.merge(df, df_mapping, how='left', left_index=False,
                         left_on=miscu.eval_elem_mapping(config, 'left_on'),
                         right_on=miscu.eval_elem_mapping(config, 'right_on'))
    df_target.drop(columns=miscu.eval_elem_mapping(config, 'right_on'), inplace=True)

    return df_target


@ log_trace
def read_feature(config):
    """
    ETL feature to read a file, based on provided ETL configuration section
    This is a composite feature, since it can call apply_dtype_feature, if appropriate config section exists
    :param config: dict; Provided configuration mapping
    :return: pd.DataFrame; Resulted dataframe
    """
    df_target = FileDataStorage(None).read(config)

    df_target.columns = df_target.columns.str.strip()

    # Call apply_dtype_feature, if appropriate config section exists
    apply_dtype_config = miscu.eval_elem_mapping(config, 'apply_dtype')
    if apply_dtype_config:
        df_target = apply_dtype_feature(df_target, apply_dtype_config)

    return df_target


@ log_trace
def write_feature(df_target, config):
    """
    ETL feature to write a dataframe, based on provided ETL configuration section
    :param config: dict; Provided configuration output
    """
    df_target = FileDataStorage(None).write(df_target, config)


@ log_trace
def rearrange_feature(df_target, config):
    """
    ETL feature to rename and reorder columns of given dataframe.
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Rearranged dataframe
    """ 
    df_target.rename(columns = miscu.eval_elem_mapping(config, 'col_rename'), inplace = True)
    df_target = df_target.assign(**miscu.eval_elem_mapping(config, 'assign_static'))

    return df_target


@ log_trace
def aggregate_feature(df_target, config):
    """
    ETL feature to aggregate dataframe using groupby or pivot
    :param df: pd.DataFrame; Output dataframe of extraction section
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Aggregated dataframe
    """
    agg_type = miscu.eval_elem_mapping(config, 'type')
    agg_values = miscu.eval_elem_mapping(config, 'values')
    agg_method = miscu.eval_elem_mapping(config, 'aggfunc')

    if agg_type == "groupby":
        agg_groupby_col = miscu.eval_elem_mapping(config, 'groupby_col')
        df_target = df_target.groupby(agg_groupby_col)[agg_values].apply(eval(agg_method))

    else:
        agg_index = miscu.eval_elem_mapping(config, 'index')
        agg_columns = miscu.eval_elem_mapping(config, 'columns')
        df_target = df_target.pivot_table(index=agg_index, columns=agg_columns,
                                        values=agg_values, aggfunc=eval(agg_method))
    
    # Convert index into a column
    df_target.reset_index(inplace=True)

    return df_target
