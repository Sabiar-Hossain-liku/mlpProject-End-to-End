import sys
from dataclasses import dataclass
import os
# library's
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging 

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path =os.path.join('artificats',"preprocessor.pkl")

class DataTransformation:

    '''
    This class is responsible for Data Transformation 
    '''


    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        try:
            numerical_feature = ["writing_score","reading_score"]
            categorical_feature = [
                'gender', 
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch', 'test_preparation_course'
                ]
            
            num_pipeline = Pipeline(
                steps=[
            ("imputer",SimpleImputer(strategy='median')), # its handling the missing value with a strategy "median"
            ("scaler",StandardScaler()) # Scaling the numarical Features
                ]
            )

            cat_pipeline = Pipeline(

                steps = [
            ("imputer",SimpleImputer(strategy="most_frequent")),
            ("one_hot_encoder",OneHotEncoder()),
            ("scaler",StandardScaler())
                ]
            )
            logging.info("Numerical  columns scalling Completed")
            logging.info("Categorical columns encoding Completed")

            # Connecting the pipeline with the columns
            preproccessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_feature),
                    ("cat_pipeline",cat_pipeline,categorical_feature)
                ]
            )
            

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation (self,train_path,test_path):

        try:
            # Reading Datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtainning preprocessing object")

            #initializing the transformer object / preprocessor object
            preprocessing_obj = self.get_data_transformer_object()
            
            # getting numerical feature and target feature column names
            target_column_name ="math_score" 
            numerical_feature_column_name = ["writing_score","reading_score"]
           
           # getting input features from train_df and droping the target features
            input_feature_train_df = train_df.drop(columns=target_column_name, axis=1)
           # getting the target feature from train_df
            target_feature_train_df = train_df[target_column_name]
           
           # getting input features for test from test_df and droping the target features
            input_feature_test_df = test_df.drop(columns=target_column_name, axis=1)
           # getting target features for test from test_df
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Apply preproccessing  object on trainning dataframe and test dataframe")

            # transforming the train and test input data using preprocessor object
            input_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_test_array = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c[
                input_train_array, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_test_array, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        