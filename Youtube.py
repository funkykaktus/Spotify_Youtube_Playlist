import os 
import pickle
import Spotify
import Keys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build 


def credentialsYoutube():
    credentials= None 

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)


    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',
                #Select the correct scoope for your use, the list can be found on youtubes api website. 
                scopes=[
                    "https://www.googleapis.com/auth/youtube.force-ssl"
                ]
            )

            #Opens up website to log in as user. Make correct settup for the api credentials on youtube api website.
            flow.run_local_server(port=8080, prompt='consent',
                                authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    return build('youtube','v3', credentials = credentials)


def initialize(textFilename):
    getYoutubeVideoID(textFilename)

def getYoutubeVideoID(textFilename):
    
    youtube = credentialsYoutube()
    resultsSpotify= Spotify.getSpotifyPlaylist()

    #Checks if there is a text file. If you want to export a new spotify playlist remove or rename the YoutubeVideoID text file.
    if(not os.path.exists(textFilename)):
        print("Creating a new text file")
        videoIDTextFile = open(textFilename, "w")

        #Loops through spotify playlist
        for item in resultsSpotify['tracks']['items']:
            print(item['track']['name'] + " "+ item['track']['artists'][0]['name'])

            #Gets the youtube playlist videoID for the song.
            request= youtube.search().list(q=item['track']['name'] + " "+ item['track']['artists'][0]['name'],part='snippet',type='video', maxResults=1)
            res = request.execute()
            
            #Adds the videoID to a text file since quota cost for a search is 100 points per request. You need to wait one day to reset the quoata. 
            print("Adding songs to text file")
            for item in res['items']:
                videoIDTextFile.write(item['id']['videoId']+"\n")

        videoIDTextFile.close()
    addSongsToYoutubePlaylist(youtube,textFilename)

def addSongsToYoutubePlaylist(youtube,textFilename): 
    
    #Adds song to youtube playlist. Quota for inserting to playlist is 50 points per request
    print("Adding songs to youtube playlist")
    
    with open(textFilename) as videoIDTextFile:
        for line in videoIDTextFile:
            print(line.strip())
            
            add_video_request=youtube.playlistItems().insert(
            part="snippet",
                body={
                    'snippet': {
                    'playlistId': Keys.youtubeplaylist, 
                    'resourceId': {
                            'kind': 'youtube#video',
                        'videoId': line.strip()
                        }
                    }
            }
            )
            response =add_video_request.execute()
    videoIDTextFile.close()