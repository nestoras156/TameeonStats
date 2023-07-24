import pandas as pd


class Team:

  def __init__(self, name):
    self.name = name
    self.home_wins = 0
    self.away_wins = 0
    self.home_draws = 0
    self.away_draws = 0
    self.home_loses = 0
    self.away_loses = 0
    self.home_goals_scored = 0
    self.away_goals_scored = 0
    self.home_goals_conceded = 0
    self.away_goals_conceded = 0

    # Add overall stats
    self.wins = 0
    self.draws = 0
    self.loses = 0
    self.goals_scored = 0
    self.goals_conceded = 0


def get_teams(filename):
  data = pd.read_csv(filename)
  home_teams = data['Home'].unique()
  away_teams = data['Away'].unique()
  teams = list(set(home_teams)
               | set(away_teams))  # union of home_teams and away_teams

  teams_objs = {team_name: Team(team_name) for team_name in teams}
  return teams_objs


def populate_team_data(filename, teams):
  data = pd.read_csv(filename)

  for i, row in data.iterrows():
    home_team = teams[row['Home']]
    away_team = teams[row['Away']]

    if row['Home Goals'] > row['Away Goals']:
      home_team.home_wins += 1
      away_team.away_loses += 1
      home_team.wins += 1  # Update overall wins
      away_team.loses += 1  # Update overall loses
    elif row['Home Goals'] < row['Away Goals']:
      home_team.home_loses += 1
      away_team.away_wins += 1
      home_team.loses += 1  # Update overall loses
      away_team.wins += 1  # Update overall wins
    else:  # draw
      home_team.home_draws += 1
      away_team.away_draws += 1
      home_team.draws += 1  # Update overall draws
      away_team.draws += 1  # Update overall draws

    home_team.home_goals_scored += row['Home Goals']
    home_team.home_goals_conceded += row['Away Goals']
    away_team.away_goals_scored += row['Away Goals']
    away_team.away_goals_conceded += row['Home Goals']

    # Update overall goals
    home_team.goals_scored += row['Home Goals']
    home_team.goals_conceded += row['Away Goals']
    away_team.goals_scored += row['Away Goals']
    away_team.goals_conceded += row['Home Goals']


