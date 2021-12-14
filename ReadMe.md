# SpotiPy Album Mesh

This is a python project used to generate album artwork meshes from your spotify playlists.
Check the "Example Output" directory for some example output from this program.

# Usage

First, you'll need to install all the dependencies needed.

To run the script, you need to first define environment variables as follows:

    export SPOTIPY_CLIENT_ID='your_client_id_here'
    export SPOTIPY_CLIENT_SECRET='your_client_secret_here'
    export SPOTIPY_REDIRECT_URI='http://www.google.com'

# Input arguments

Spotipy_Album_Artwork_Mesh.py [-h] [-q {low,medium,high}] [-o 'output_file'] [-p 'playlist_name']

optional arguments:
  -h, --help            show this help message and exit
  -q {low,medium,high}  define the resolution of the downloaded albums. (default is medium)
  -o 'output_file'      file path and name of output file (should end in .jpg). (default is 'album_mesh.jpg'
  -p 'playlist_name'    name of public playlist to download album art from (enclose in single-quotes ex: 'Gruvy Toons')

# Future work

This isn't a user-friendly process yet, though I hope to eventually make it to be one.
If you have experience with this, any help is welcomed. I'd love to make this something anyone
can download and run locally with minimal technical expertise. It could possibly even be able to run 
as a web app. 