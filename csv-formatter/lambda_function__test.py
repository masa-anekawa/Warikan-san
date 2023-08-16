import pandas as pd
from lambda_function import transform_df

def test_transform():
    # load df from csv files
    input_df = pd.read_csv('./input_format.csv')
    output_df = pd.read_csv('./output_format.csv')

    transformed_df = transform_df(input_df)

    # assert columns, row count, data types are equal between transform_df(input_df) and output_df
    assert list(transformed_df.columns) == list(output_df.columns)
    assert len(transformed_df) == len(output_df)
    assert transformed_df.dtypes.equals(output_df.dtypes)

