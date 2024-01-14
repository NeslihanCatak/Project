from nba_api.stats.static import teams
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playergamelog

# Function to get NBA team data
def get_nba_team_data():
    nba_teams = teams.get_teams()
    teams_data = []
    for team in nba_teams:
        team_data = {
            'TeamID': team['id'],
            'Abbreviation': team['abbreviation'],
            'City': team['city'],
            'Full_Name': team['full_name'],
            'Name': team['abbreviation'],
        }
        teams_data.append(team_data)

    # Convert to Pandas DataFrame
    df = pd.DataFrame(teams_data)

    # Save team data to CSV file
    df.to_csv('nba_team_data.csv', index=False)

    return df  # Return the DataFrame instead of printing

# Function to get NBA player data
def get_nba_player_data(player_name, season):
    # Get player information
    player_info = players.find_players_by_full_name(player_name)
    
    if player_info:
        player_id = player_info[0]['id']

        # Get player's general information
        player_general_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        general_info_data = player_general_info.get_normalized_dict()

        # Get player's game log for a specific season
        player_game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        game_log_data = player_game_log.get_normalized_dict()

        # Combine player data
        player_data = {
            'Player Name': general_info_data['CommonPlayerInfo'][0]['DISPLAY_FIRST_LAST'],
            'Team': general_info_data['CommonPlayerInfo'][0]['TEAM_ABBREVIATION'],
            'Birth Date': general_info_data['CommonPlayerInfo'][0]['BIRTHDATE'],
            'Height': general_info_data['CommonPlayerInfo'][0]['HEIGHT'],
            'Weight': general_info_data['CommonPlayerInfo'][0]['WEIGHT'],
            'Game Log': [
                {
                    'Date': game['GAME_DATE'],
                    'Points': game['PTS'],
                    'Rebounds': game['REB'],
                    'Assists': game['AST']
                }
                for game in game_log_data['PlayerGameLog']
            ]
        }

        # Convert to Pandas DataFrame
        df = pd.DataFrame(player_data['Game Log'])
    
        # Save player data to CSV file
        df.to_csv(f'{player_name}_data.csv', index=False)

        return df  # Return the DataFrame instead of printing
    else:
        print(f"Player {player_name} not found.")

if __name__ == "__main__":
    # Get and save team data to CSV, print to screen
    get_nba_team_data()

    # Example: Get LeBron James' data for the 2022 season, save to CSV, print to screen
    get_nba_player_data("LeBron James", "2022")