import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def scrape_data(url, table_id):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  table = soup.find('table', {'id': table_id})

  if table is None:
    print(f"No table found with id {table_id}")
    return None

  try:
    firstdata = pd.read_html(str(table))[0]
    return firstdata
  except Exception as e:
    print(f"Error reading table into DataFrame: {e}")
    return None


def data_cleaner(firstdata):
  # Define the columns we want to keep
  columns_to_keep = [
      "Wk", "Day", "Date", "Time", "Home", "Score", "Away", "Referee"
  ]

  # Filter the dataframe to only include these columns
  cleaned_dataframe = firstdata[columns_to_keep]

  # Remove rows where all elements are missing
  cleaned_dataframe = cleaned_dataframe.dropna(how='all')

  # Only perform the operations on rows where 'Score' is not null
  score_condition = cleaned_dataframe['Score'].notna()

  # Perform the split operation, store results in new columns and convert them to integers
  cleaned_dataframe.loc[score_condition, 'Home Goals'] = cleaned_dataframe.loc[
      score_condition, 'Score'].str.split('–').str[0].astype(int)
  cleaned_dataframe.loc[score_condition, 'Away Goals'] = cleaned_dataframe.loc[
      score_condition, 'Score'].str.split('–').str[1].astype(int)

  # Remove the 'Score' column as it's no longer needed
  cleaned_dataframe = cleaned_dataframe.drop(columns=['Score'])

  # Reorder the columns
  cleaned_dataframe = cleaned_dataframe[[
      'Wk', 'Day', 'Date', 'Time', 'Home', 'Home Goals', 'Away Goals', 'Away',
      'Referee'
  ]]

  return cleaned_dataframe


def dataStorer(cleaned_dataframe, file_name):
  cleaned_dataframe.to_csv(file_name, index=False)
