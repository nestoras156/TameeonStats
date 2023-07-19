from scrap2pandas import scrape_data, data_cleaner, dataStorer


def main():
  url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
  table_id = "sched_2022-2023_9_1"

  firstdata = scrape_data(url, table_id)

  if firstdata is not None:
    cleaned_dataframe = data_cleaner(firstdata)
    dataStorer(cleaned_dataframe, 'data.csv')
    print("Program completed successfully")
  else:
    print("Could not scrape data")


if __name__ == "__main__":
  main()
