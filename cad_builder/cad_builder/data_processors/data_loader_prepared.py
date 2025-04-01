import os
import pandas as pd
from cad_builder.utils import find_project_root


# def get_prepared_data():
# project_root = find_project_root(os.path.dirname(__file__))
project_root = find_project_root(os.path.dirname("./"))
prepared_data_path = os.path.join(project_root, f'cad_builder/data/text2cad_v1.1.csv')
prepared_data = pd.read_csv(prepared_data_path)
prepared_data = prepared_data[(~prepared_data["beginner"].isna()) &
                              (~prepared_data["description"].isna())].copy()
prepared_data.info()
prepared_data.isna().sum()

prepared_data[["keywords"]]


prepared_data[["uid", "description", "all_level_data", "nli_data"]]
prepared_data.sample(10, random_state=42)["uid"].unique()





