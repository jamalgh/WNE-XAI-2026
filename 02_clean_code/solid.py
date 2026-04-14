# ----------------------------------------------------
#                 XAI 2026
#         CLASS 07: SOLID principles
# ----------------------------------------------------

# Article source:
#  https://towardsdatascience.com/scale-your-machine-learning-projects-with-solid-principles-824230fa8ba1/

# Imports
# ----------------------------------------------------
import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO)
# ----------------------------------------------------


def process(path: str, output_path: str) -> pd.DataFrame:
    """"""
    df = pd.read_parquet(path)
    logging.info(f"Data: {df}")

    # Normalization
    std = np.std(df["feature_a"])
    mean = np.mean(df["feature_a"])
    standardized_feature = (df["feature_a"] - mean) / std

    # Categorical value
    encoder = LabelEncoder()
    encoded_feature = encoder.fit_transform(df["feature_b"])

    # Nan
    filled_feature = df["feature_c"].fillna(-1)

    processed_df = pd.concat(
        [standardized_feature, encoded_feature, filled_feature], axis=1
    )
    logging.info(f"Processed data: {processed_df}")
    processed_df.to_parquet(output_path)


def main():
    path = "data/data.parquet"
    output_path = "data/preprocessed_data.parquet"
    process(path, output_path)


if __name__ == "__main__":
    main()


# 1. Single Responsibility Principle
# -------------------------------
# A class should have only one reason to change.


def process(self, path: str, output_path: str) -> None:
    df = load_data(path)
    logging.info(f"Raw data: {df}")
    normalized_df = normalize(df["feature_a"])
    encoded_df = encode(df["feature_b"])
    filled_df = fill_na(df["feature_c"], value=-1)
    processed_df = pd.concat([normalized_df, encoded_df, filled_df], axis=1)
    logging.info(f"Processed df: {processed_df}")
    save_data(df=processed_df, path=output_path)


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    std = np.std(df)
    mean = np.mean(df)
    return (features - mean) / std


def encode(df: pd.DataFrame) -> pd.DataFrame:
    encoder = LabelEncoder()
    encoder.fit_transform(features)
    array = np.atleast_2d(array)  # Transform array into 2D from 1D or 2D arrays
    processed_df = pd.DataFrame({name: data for name, data in zip(df.columns, array)})
    return processed_df


def fill_na(df: pd.DataFrame, value: int = -1) -> pd.DataFrame:
    return df.fillna(value=self.value)


def load_data(self, path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def save_data(self, df: pd.DataFrame, path: str) -> None:
    df.to_parquet(path)


# 2. Open/Closed Principle
# -------------------------------
# Software entities (classes, modules, functions, etc.) should be
# open for extension, but closed for modification.


# So, now we add a functionality to load data also from csv.

# NO 
def load_data(self, path: Path) -> pd.DataFrame:
    splitted_path = os.path.splitext(path)
    if splitted_path[-1] == ".csv":
        return pd.read_csv(path)
    if splitted_path[-1] == ".parquet"
        return pd.read_parquet(path)
    else:
        raise ValueError(f"File type {splitted_path[-1]} not handled.")
    
# YES
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_parquet(path: str) -> pd;DataFrame:
    return pd.read_parquet(path)



# 3. Liskov Substitution Principle
# -------------------------------
# A module may be replaced by its base without breaking the program.


# Now we go into OOP 
# ------------------------------------------------------------
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod   
    def load_data(self, path: str) -> pd.DataFrame:
        pass

class ParquetDataLoader(DataLoader):
    def load_data(self, df: pd.DataFrame, path: str) -> None:
        return pd.read_parquet(path)

class CSVDataLoader(DataLoader):
    def load_data(self, df: pd.DataFrame, path: str) -> None:
        return pd.read_csv(path)


# And if then you need also to add a JSON loading functionality,
# you just inherit from DataLoader and don't break anything
class JSONDataLoader(DataLoader):
    def load_data(path: str) -> pd.Dataframe:
        return pd.read_json(path)
    
# ------------------------------------------------------------


# And we can also implement same logic for feature preprocessing 
class FeatureProcessor(ABC):
    def __init__(self, feature_names: List[str]) -> None:
        # Features to process are directly implemented into the base module
        self.feature_names = feature_names

    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class Standardizer(FeatureProcessor):   
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df[self.feature_names]
        std = np.std(features)
        mean = np.mean(features)
        return (features - mean) / std

class Encoder(FeatureProcessor):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df[self.feature_names]
        encoder = LabelEncoder()
        array = encoder.fit_transform(features)
        array = np.atleast_2d(array) # Transform array into 2D from 1D or 2D arrays
        processed_df = pd.DataFrame({name: data for name, data in zip(features.columns, array)})
        return processed_df

class NaFiller(FeatureProcessor):
    def __init__(self, feature_names: List[str], value: int = -1) -> None:
        self.value = value
        super().__init__(feature_names)

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df[self.feature_names]
        return features.fillna(value=self.value)

# Adding new functionality - normalisation
class Normalizer(FeatureProcessor):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df[self.feature_names]
        minimum = features.min()
        maximum = features.max()
        return (features - minimum) / (maximum - minimum)
    

# So now, the former process() function would look like this:
class DataProcessor:
    # __init__ respect the Liskov Substitution Principle
    def __init__(
        self,
        feature_processors: List[FeatureProcessor],
        data_loader: DataLoader,
        data_saver: DataSaver
    ) -> None:
        self.feature_processors = feature_processors
        self.data_loader = data_loader
        self.data_saver = data_saver     

    def process(self, path: str, output_path: str) -> None:
        df = self.data_loader.load_data(path)
        logging.info(f"Raw data: {df}")
        processed_df = pd.concat(
            [feature_processor.process(df) for feature_processor in self.feature_processors],
            axis=1
        )
        self.data_saver.save_data(df=processed_df, path=output_path)
        logging.info(f"Processed df: {processed_df}")


# Initialisation: 
processor = DataProcessor(
        feature_processors=[
            Normalizer(feature_names=["feature_a"]),
            # Standardizer(...),
            Encoder(feature_names=["feature_b"]),
            NaFiller(feature_names=["feature_c"], value=-1)
        ],
        data_loader=CSVDataLoader(),
        data_saver=ParquetDataSaver()
    )
    processor.process(
        path="data/data.csv", 
        output_path="data/preprocessed_data.parquet"
    )


# Homework: 
# Check how the code would further be changed to meet principles 4 and 5. 
# https://towardsdatascience.com/scale-your-machine-learning-projects-with-solid-principles-824230fa8ba1/

# 4. Interface Segregation Principle
# -------------------------------
# Clients should not be forced to depend upon methods that they do not use. 
# Interfaces belong to clients, not to hierarchies.

# In other words, a class shouldn’t inherit methods (or attributes) that are not used. 
# Those methods should be associated with appropriate classes instead.


# 5. Dependency Aversion Principle
# -------------------------------
# Abstractions should not depend upon details. Details should depend upon abstractions.