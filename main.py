from scrap2pandas import scrape_data, data_cleaner, dataStorer
from teams import get_teams, populate_team_data


def main():
  url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
  table_id = "sched_2022-2023_9_1"

  firstdata = scrape_data(url, table_id)

  if firstdata is not None:
    cleaned_dataframe = data_cleaner(firstdata)
    filename = 'data.csv'
    dataStorer(cleaned_dataframe, filename)
    print("Data scraped and cleaned successfully")

    teams = get_teams(filename)
    populate_team_data(filename, teams)

    print(f"Teams in the league: {list(teams.keys())}")
    print("\nStats for Arsenal and Manchester United:")
    print(f"Arsenal: {vars(teams['Arsenal'])}")
    print(f"Manchester Utd: {vars(teams['Manchester Utd'])}")

  else:
    print("Could not scrape data")


if __name__ == "__main__":
  main()
