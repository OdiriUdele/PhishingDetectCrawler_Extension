def model_inference(features):
  """
  This function takes in a data and returns a predictions.
  """

  # Import libraries
  import pandas as pd
  import numpy as np
  import pickle
  import xgboost
  from joblib import dump , load


  # features = pd.DataFrame(data, index=[0])

  # Load the model
  model = load(filename="model/tuned_xgb_model.joblib")

  # Transform the data
  input_data_as_array = np.asarray(features)
  print("array")
  print(input_data_as_array)
  input_data_reshape = input_data_as_array.reshape(1, -1)
  prediction = model.predict(input_data_reshape)

  status = np.array( ['legitimate', 'phishing'])
  

  return status[prediction]

