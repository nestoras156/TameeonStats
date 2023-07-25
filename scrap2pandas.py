import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta


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

  # Convert the 'Date' column to datetime
  cleaned_dataframe['Date'] = pd.to_datetime(cleaned_dataframe['Date'])

  return cleaned_dataframe


def played_games_filter(cleaned_dataframe):
  # Only perform the operations on rows where 'Score' is not null
  score_condition = cleaned_dataframe['Score'].notna()

  # Perform the split operation, store results in new columns and convert them to integers
  cleaned_dataframe.loc[score_condition, 'Home Goals'] = cleaned_dataframe.loc[
      score_condition, 'Score'].str.split('–').str[0].astype(int)
  cleaned_dataframe.loc[score_condition, 'Away Goals'] = cleaned_dataframe.loc[
      score_condition, 'Score'].str.split('–').str[1].astype(int)

  # Remove the 'Score' column as it's no longer needed
  cleaned_dataframe = cleaned_dataframe.drop(columns=['Score'])

  # Only keep the games that have been played
  played_games = cleaned_dataframe[score_condition]

  return played_games


def upcoming_games_filter(cleaned_dataframe):
  # Only perform the operations on rows where 'Score' is null
  upcoming_condition = cleaned_dataframe['Score'].isna()

  # Only keep the upcoming games
  upcoming_games = cleaned_dataframe[upcoming_condition]

  # Find the date of the last played game
  last_played_date = cleaned_dataframe[cleaned_dataframe['Score'].notna()]['Date'].max()

  # Only keep the games that are within 7 days of the last played game
  upcoming_games = upcoming_games[upcoming_games['Date'] <= last_played_date + timedelta(days=7)]

  return upcoming_games


def dataStorer(played_games, upcoming_games, played_games_file_name, upcoming_games_file_name):
  played_games.to_csv(played_games_file_name, index=False)
  upcoming_games.to_csv(upcoming_games_file_name, index=False)
