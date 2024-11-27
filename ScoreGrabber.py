import requests
import json
import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write_json(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Filtered data for 'competition-corner' saved to {filename}")
    except Exception as e:
        logger.error(f"An error occurred while writing to {filename}: {e}")


def getCompetitionCorner(output_file):
    # URL to fetch the JSON data
    url = "https://virtualpinballchat.com:8443/vpc/api/v1/weeksByChannelName"

    try:
        # Fetch data from the URL
        response = requests.get(url)  # Skip SSL verification if necessary
        data = response.json()  # Parse the JSON response

        # Filter for "channelName": "competition-corner" and "isArchived": false
        filtered_data = [
            {
                "channelName": "competition-corner",
                "weeks": [
                    week for week in channel.get("weeks", [])
                    if week.get("isArchived") is False
                ]
            }
            for channel in data
            if channel.get("channelName") == "competition-corner"
        ]
        write_json(filtered_data, output_file)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def get_iScoreGame(roomId, output_file):
    try:
        gameLink = f"https://iscored.info/publicCommands.php?c=getAllGames&roomID={roomId}"
        response = requests.get(gameLink)
        response = json.loads(response.text)
        gameId = response[0]['gameID']
        scoreLink = f"https://iscored.info/publicCommands.php?c=getScores2&roomID={roomId}"
        response = requests.get(scoreLink)
        response = json.loads(response.text)
        filtered_response = [entry for entry in response if entry.get('game') == gameId]
        write_json(filtered_response, output_file)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_iScoreGame("1011", "special-when-lit.json")
    get_iScoreGame("700", "thursday-throwdown.json")
    getCompetitionCorner("competition-corner.json")
