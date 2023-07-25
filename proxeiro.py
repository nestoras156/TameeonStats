################################################################
def update_elo(R_A, R_B, Sa, K):
    """
    Function to update the Elo rating for a team.

    Args:
    R_A: Elo rating for team A
    R_B: Elo rating for team B
    Sa: actual result of the game for team A (1 for win, 0.5 for draw, 0 for loss)
    K: K-factor, which determines the maximum change in rating (larger K = more change)

    Returns:
    Updated Elo rating for team A
    """

    # Calculate the expected result for team A based on their current ratings
    E_A = 1 / (1 + 10 ** ((R_B - R_A) / 400))

    # Update the Elo rating for team A based on the actual result and the expected result
    Rn_A = R_A + K * (Sa - E_A)

    return Rn_A
#################################################################

#################################################################

def update_attack_defense_elo(RA_A, RD_B, actual_goals_A, K):
    """
    Function to update the attack Elo rating for team A.

    Args:
    RA_A: Attack Elo rating for team A
    RD_B: Defense Elo rating for team B
    actual_goals_A: Actual goals scored by team A
    K: K-factor, which determines the maximum change in rating (larger K = more change)

    Returns:
    Updated Attack Elo rating for team A
    """

    # Calculate the expected goals for team A based on their current ratings
    expected_goals_A = 1 / (1 + 10 ** ((RD_B - RA_A) / 400))

    # Update the Elo rating for team A based on the actual goals and the expected goals
    Rn_A = RA_A + K * (actual_goals_A - expected_goals_A)

    return Rn_A

#################################################################