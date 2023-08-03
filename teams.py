import pandas as pd
import csv


class Team:

  def __init__(self, name):
    # Team name
    self.name = name

    # Home, away, and overall stats
    self.home_games = 0
    self.away_games = 0
    self.total_games = 0

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

    self.wins = 0
    self.draws = 0
    self.loses = 0
    self.goals_scored = 0
    self.goals_conceded = 0

    # Average stats
    self.home_avg_goals_scored = 0
    self.away_avg_goals_scored = 0
    self.overall_avg_goals_scored = 0

    self.home_avg_goals_conceded = 0
    self.away_avg_goals_conceded = 0
    self.overall_avg_goals_conceded = 0

    # Elo scores
    self.home_attack_elo = 1000
    self.home_defence_elo = 1000
    self.away_attack_elo = 1000
    self.away_defence_elo = 1000

    self.attack_elo = 1000
    self.defence_elo = 1000

    self.home_elo = 1000
    self.away_elo = 1000
    self.elo = 1000

  def calculate_averages(self):
    if self.home_games != 0:
      self.home_avg_goals_scored = self.home_goals_scored / self.home_games
      self.home_avg_goals_conceded = self.home_goals_conceded / self.home_games
    if self.away_games != 0:
      self.away_avg_goals_scored = self.away_goals_scored / self.away_games
      self.away_avg_goals_conceded = self.away_goals_conceded / self.away_games
    if self.total_games != 0:
      self.overall_avg_goals_scored = self.goals_scored / self.total_games
      self.overall_avg_goals_conceded = self.goals_conceded / self.total_games


# Attack/Defence ELO
def calculate_elo(home_team, away_team, home_goals, away_goals,
                  average_conceded_goals_home, average_conceded_goals_away):
  K = 20  # This is a constant that should be fine-tuned
  L = 20  # This is a constant for the case when actual_goals < average_conceded_goals

  # Calculate the goal difference for home and away teams
  goal_difference_home = home_goals - average_conceded_goals_home
  goal_difference_away = away_goals - average_conceded_goals_away

  # Update the home team's attack and away team's defence based on home team's goals
  update_elo_attack_defence(home_team, away_team, goal_difference_home, K, L,
                            'home')

  # Update the away team's attack and home team's defence based on away team's goals
  update_elo_attack_defence(away_team, home_team, goal_difference_away, K, L,
                            'away')

  # Update overall attack and defence ELO
  home_team.attack_elo = (home_team.home_attack_elo +
                          home_team.away_attack_elo) / 2
  home_team.defence_elo = (home_team.home_defence_elo +
                           home_team.away_defence_elo) / 2
  away_team.attack_elo = (away_team.home_attack_elo +
                          away_team.away_attack_elo) / 2
  away_team.defence_elo = (away_team.home_defence_elo +
                           away_team.away_defence_elo) / 2


def update_elo_attack_defence(attack_team, defence_team, goal_difference, K, L,
                              venue):
  if goal_difference > 0:
    # Attacking team was better than expected
    setattr(attack_team, f"{venue}_attack_elo",
            getattr(attack_team, f"{venue}_attack_elo") + K * goal_difference)
    setattr(
        defence_team, f"{venue}_defence_elo",
        getattr(defence_team, f"{venue}_defence_elo") - K * goal_difference)
  elif goal_difference < 0:
    # Attacking team was worse than expected
    setattr(
        attack_team, f"{venue}_attack_elo",
        getattr(attack_team, f"{venue}_attack_elo") - L * abs(goal_difference))
    setattr(
        defence_team, f"{venue}_defence_elo",
        getattr(defence_team, f"{venue}_defence_elo") +
        L * abs(goal_difference))

  # Make sure Elo ratings do not fall below a minimum (e.g., 100)
  setattr(attack_team, f"{venue}_attack_elo",
          max(getattr(attack_team, f"{venue}_attack_elo"), 100))
  setattr(defence_team, f"{venue}_defence_elo",
          max(getattr(defence_team, f"{venue}_defence_elo"), 100))


# Home/Away/overall result ELO
def update_elo(home_team, away_team, result, k_factor=20):
  # Calculate expected outcome
  expected_home = 1 / (1 + 10**(
      (home_team.away_elo - home_team.home_elo) / 400))
  expected_away = 1 - expected_home

  # Define the actual outcome
  # win = 1, draw = 0.5, loss = 0
  actual_home, actual_away = get_actual_scores(result, home_team.home_elo,
                                               away_team.away_elo)

  # Update Elo Ratings
  home_team.home_elo, away_team.away_elo = update_individual_elo(
      home_team.home_elo, away_team.away_elo, actual_home, expected_home,
      actual_away, expected_away, k_factor)

  # Update overall ELO
  home_team.elo = (home_team.home_elo + home_team.away_elo) / 2
  away_team.elo = (away_team.home_elo + away_team.away_elo) / 2


def update_individual_elo(home_elo, away_elo, actual_home, expected_home,
                          actual_away, expected_away, k_factor):
  new_home_elo = home_elo + k_factor * (actual_home - expected_home)
  new_away_elo = away_elo + k_factor * (actual_away - expected_away)
  return new_home_elo, new_away_elo


def get_actual_scores(result, home_elo, away_elo):
  if result == 'H':  # Home Win
    actual_home = 1
    actual_away = 0
  elif result == 'A':  # Away Win
    actual_home = 0
    actual_away = 1
  else:  # Draw
    if home_elo > away_elo:
      actual_home = 0.5
      actual_away = 0.75
    elif home_elo < away_elo:
      actual_home = 0.75
      actual_away = 0.5
    else:
      actual_home = 0.5
      actual_away = 0.5
  return actual_home, actual_away


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

    # Update game counts
    home_team.home_games += 1
    away_team.away_games += 1
    home_team.total_games += 1
    away_team.total_games += 1

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

    # Calculate averages
    home_team.calculate_averages()
    away_team.calculate_averages()

    # Update ELO scores
    calculate_elo(home_team, away_team, row['Home Goals'], row['Away Goals'],
                  home_team.home_avg_goals_conceded,
                  away_team.away_avg_goals_conceded)

    if row['Home Goals'] > row['Away Goals']:  # home team wins
      result = 'H'
    elif row['Home Goals'] < row['Away Goals']:  # away team wins
      result = 'A'
    else:  # draw
      result = 'D'
    update_elo(home_team, away_team, result)


def print_first_team_data(teams):
  # Get the first team in the dictionary
  first_team = next(iter(teams.values()))

  # Print the attributes of the first team
  print(f"Team Name: {first_team.name}")
  print(f"Home Games: {first_team.home_games}")
  print(f"Away Games: {first_team.away_games}")
  print(f"Total Games: {first_team.total_games}")
  print(f"Home Wins: {first_team.home_wins}")
  print(f"Away Wins: {first_team.away_wins}")
  print(f"Home Draws: {first_team.home_draws}")
  print(f"Away Draws: {first_team.away_draws}")
  print(f"Home Loses: {first_team.home_loses}")
  print(f"Away Loses: {first_team.away_loses}")
  print(f"Wins: {first_team.wins}")
  print(f"Draws: {first_team.draws}")
  print(f"Loses: {first_team.loses}")
  print(f"Goals Scored: {first_team.goals_scored}")
  print(f"Goals Conceded: {first_team.goals_conceded}")
  print(f"Home Goals Scored: {first_team.home_goals_scored}")
  print(f"Away Goals Scored: {first_team.away_goals_scored}")
  print(f"Home Goals Conceded: {first_team.home_goals_conceded}")
  print(f"Away Goals Conceded: {first_team.away_goals_conceded}")
  print(f"Home Average Goals Scored: {first_team.home_avg_goals_scored}")
  print(f"Away Average Goals Scored: {first_team.away_avg_goals_scored}")
  print(f"Overall Average Goals Scored: {first_team.overall_avg_goals_scored}")
  print(f"Home Average Goals Conceded: {first_team.home_avg_goals_conceded}")
  print(f"Away Average Goals Conceded: {first_team.away_avg_goals_conceded}")
  print(
      f"Overall Average Goals Conceded: {first_team.overall_avg_goals_conceded}"
  )

  # Elo Scores
  print(f"Home Attack Elo: {first_team.home_attack_elo}")
  print(f"Home Defence Elo: {first_team.home_defence_elo}")
  print(f"Away Attack Elo: {first_team.away_attack_elo}")
  print(f"Away Defence Elo: {first_team.away_defence_elo}")
  print(f"Attack Elo: {first_team.attack_elo}")
  print(f"Defence Elo: {first_team.defence_elo}")
  print(f"Home Elo: {first_team.home_elo}")
  print(f"Away Elo: {first_team.away_elo}")
  print(f"Elo: {first_team.elo}")
