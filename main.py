from scrap2pandas import scrape_data, data_cleaner, played_games_filter, upcoming_games_filter, dataStorer
from teams import get_teams, populate_team_data, print_first_team_data, update_elo, calculate_elo
import pandas as pd


def main():
  url = "https://fbref.com/en/comps/29/schedule/Allsvenskan-Scores-and-Fixtures"
  table_id = "sched_2023_29_1"
  played_games_file_name = 'data.csv'
  upcoming_games_file_name = 'nextgames.csv'

  firstdata = scrape_data(url, table_id)

  if firstdata is not None:
    cleaned_dataframe = data_cleaner(firstdata)
    played_games = played_games_filter(cleaned_dataframe)
    upcoming_games = upcoming_games_filter(cleaned_dataframe)

    dataStorer(played_games, upcoming_games, played_games_file_name,
               upcoming_games_file_name)
    print("Data scraped and cleaned successfully")

    teams = get_teams(played_games_file_name)
    populate_team_data(played_games_file_name, teams)

    print(f"Teams in the league: {list(teams.keys())}")

    print("\nUpcoming games:")
    print(pd.read_csv(upcoming_games_file_name))

    print("\nFirst team data:")
    print_first_team_data(teams)

  else:
    print("Could not scrape data")


if __name__ == "__main__":
  main()
