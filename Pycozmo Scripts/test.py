import vlc
import time
# Path to your audio file
audio_file = 'auto.mp3'
# Creating a VLC instance
player = vlc.Instance()
# Creating a media player
media_player = player.media_player_new()
# Creating a new media
media = player.media_new(audio_file)
# Setting media to the media player
media_player.set_media(media)
# Playing the media
media_player.play()
# Wait for the audio to play
time.sleep(10)  # Adjust this to the length of your audio file or find a more dynamic way to determine the length
# Note: The sleep here is just to prevent the script from terminating
# immediately after starting to play the audio. In a real application,
# you would use events or a more sophisticated method to determine when
# the audio has finished playing.