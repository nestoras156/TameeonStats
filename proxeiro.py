#Attack/Defence ELO
def calculate_elo(home_team, away_team, actual_goals, average_conceded_goals):
    K = 20  # This is a constant that should be fine-tuned
    L = 20  # This is a constant for the case when actual_goals < average_conceded_goals

    # Calculate the goal difference
    goal_difference = actual_goals - average_conceded_goals

    if goal_difference > 0:
        # Home team's attack was better than expected
        home_team.home_attack_elo += K * goal_difference
        away_team.away_defence_elo -= K * goal_difference
    elif goal_difference < 0:
        # Home team's attack was worse than expected
        home_team.home_attack_elo -= L * abs(goal_difference)
        away_team.away_defence_elo += L * abs(goal_difference)

    # Make sure Elo ratings do not fall below a minimum (e.g., 100)
    home_team.home_attack_elo = max(home_team.home_attack_elo, 100)
    away_team.away_defence_elo = max(away_team.away_defence_elo, 100)

# An example call to the function might look like this:
# calculate_elo(home_team, away_team, home_team_goals, away_team_avg_conceded)


#Home/Away/overall result ELO
def update_elo(home_elo, away_elo, result, k_factor=20):
    # Calculate expected outcome
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    
    # Define the actual outcome
    # win = 1, draw = 0.5, loss = 0
    if result == 'H': # Home Win
        actual_home = 1
        actual_away = 0
    elif result == 'A': # Away Win
        actual_home = 0
        actual_away = 1
    else: # Draw
        if home_elo > away_elo:
            actual_home = 0.5
            actual_away = 0.75
        elif home_elo < away_elo:
            actual_home = 0.75
            actual_away = 0.5
        else:
            actual_home = 0.5
            actual_away = 0.5
    
    # Update Elo Ratings
    new_home_elo = home_elo + k_factor * (actual_home - expected_home)
    new_away_elo = away_elo + k_factor * (actual_away - expected_away)
    
    return new_home_elo, new_away_elo
