import pandas as pd
import numpy as np

def format_value(x, max_len=20):
    if pd.isna(x):
        return '<NaN>'
    if isinstance(x, str) and len(x) > max_len:
        return x[:max_len-3] + '...'
    elif isinstance(x, float):
        return f'{x:.3f}'.rstrip('0').rstrip('.')
    else:
        return str(x)

def get_df_info(df, trh=0.1):
    """
    Generates a summary DataFrame with detailed information about each column
    of the input DataFrame.

    This function analyzes data types, calculates uniqueness, finds value
    proportions (nulls, zeros, empty strings), and computes a `trash_score`
    to quickly identify potentially problematic or low-information columns.

    Args:
        df (pd.DataFrame): The input DataFrame to analyze.
        trh (float, optional): A threshold for the proportion of the most
            common value, used in the `trash_score` calculation.
            Defaults to 0.1.

    Returns:
        pd.DataFrame:
            A DataFrame containing summary statistics for each column of the
            input `df`. The index of the returned DataFrame consists of the
            column names from the input `df`. The result is sorted by
            `trash_score` in descending order.

            The columns of the returned DataFrame are:
            - `dtype`: Data type of the column.
            - `nunique`: Number of unique values, including NaN (`dropna=False`).
            - `example_1`: The first unique non-null value.
            - `example_2`: The second unique non-null value.
            - `zero`: Proportion of numeric zeros. Formatted as 'z:0.XXX' or -1 if none.
            - `nan`: Proportion of NaN/null values. Formatted as 'n:0.XXX' or -1 if none.
            - `empty_str`: Proportion of empty strings (''). Formatted as 'e:0.XXX' or -1 if none.
            - `vc_max`: The most frequent value and its proportion, formatted as '(value, 0.XXX)'.
            - `trash_score`: A metric to estimate data quality. It is the maximum of:
                1. The sum of `nan`, `zero`, and `empty_str` proportions.
                2. The proportion of the most frequent value, if it exceeds `trh`.
    """
    df_info = pd.DataFrame(index=df.columns)
    df_info['dtype'] = df.dtypes
    # -0.5 nunique без dropna=False
    df_info['nunique'] = df.nunique(dropna=False)

    nan_shape = df.isna().mean()

    numeric_cols = df.select_dtypes(include=np.number).columns
    zero_shape = pd.Series(0.0, index=df.columns)
    if not numeric_cols.empty:
        zero_shape[numeric_cols] = (df[numeric_cols] == 0).mean()

    object_cols = df.select_dtypes(include=['object']).columns
    empty_str_shape = pd.Series(0.0, index=df.columns)
    if not object_cols.empty:
        empty_str_shape[object_cols] = (df[object_cols] == '').mean()

    examples_1 = []
    examples_2 = []
    vc_max_vals = []
    vc_max_shapes = []

    for col in df.columns:
        series = df[col]
        
        unique_vals = series.dropna().unique()
        examples_1.append(unique_vals[0] if len(unique_vals) > 0 else np.nan)
        examples_2.append(unique_vals[1] if len(unique_vals) > 1 else np.nan)

        value_counts = series.value_counts()
        if not value_counts.empty:
            vc_max_vals.append(value_counts.index[0])
            vc_max_shapes.append(value_counts.iloc[0] / len(series))
        else:
            vc_max_vals.append(np.nan)
            vc_max_shapes.append(0.0)
            
    df_info['example_1'] = examples_1
    df_info['example_2'] = examples_2

    pos1 = nan_shape + zero_shape + empty_str_shape
    vc_max_shapes = pd.Series(vc_max_shapes, index=df.columns)
    pos2 = vc_max_shapes.where(vc_max_shapes > trh, 0)
    
    df_info['trash_score'] = np.maximum(pos1, pos2)

    df_info['nan'] = nan_shape.apply(lambda x: f'n:{x:.3f}' if x > 0 else -1)
    df_info['zero'] = zero_shape.apply(lambda x: f'z:{x:.3f}' if x > 0 else -1)
    df_info['empty_str'] = empty_str_shape.apply(lambda x: f'e:{x:.3f}' if x > 0 else -1)
    
    vc_max_formatted = []
    for val, shape in zip(vc_max_vals, vc_max_shapes):
        if shape > 0:
            formatted_val = format_value(val)
            vc_max_formatted.append(f'({formatted_val}, {shape:.3f})')
        else:
            vc_max_formatted.append(-1)
    df_info['vc_max'] = vc_max_formatted
    
    df_info['example_1'] = df_info['example_1'].apply(format_value)
    df_info['example_2'] = df_info['example_2'].apply(format_value)
    
    final_columns = [
        'dtype', 'nunique', 'example_1', 'example_2', 
        'zero', 'nan', 'empty_str', 'vc_max', 'trash_score'
    ]

    return df_info[final_columns].sort_values(by='trash_score', ascending=False)
