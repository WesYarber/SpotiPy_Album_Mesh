#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import spotipy
import json
import requests
import glob
import re, shutil
import os, random
from os.path import exists
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import PIL
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Spotipy Album Mesh:  Create an album artwork mesh from a given Spotify playlist.')
parser.add_argument('-q', choices=['low', 'medium', 'high'], default='medium',
    help='define the resolution of the downloaded albums. (default is medium)')
parser.add_argument('-o', metavar='\'output_file\'', default='album_mesh.jpg',
    help='file path and name of output file (should end in .jpg). (default is \'album_mesh.jpg\'')
parser.add_argument('-p', metavar='\'playlist_name\'',
    help='name of public playlist to download album art from (enclose in single-quotes ex: \'Gruvy Toons\')')
# parser.add_argument('-max', default='-1', type=int,
#     help='maximum number of albums to download. (default is no limit)')
# parser.add_argument('-height', type=int, required=True,
#     help='height of album artwork mesh in albums (\'-h 2\' creates a mesh that is 2 albums high)')
# parser.add_argument('-width', type=int, required=True,
#     help='width of album artwork mesh in albums (\'-w 2\' creates a mesh that is 2 albums wide)')

args = parser.parse_args()
playlist_name = args.p
output_file = args.o

if args.q == 'high':
    album_resolution = 0
    size = 640
elif args.q == 'medium':
    album_resolution = 1
    size = 300
elif args.q == 'low':
    album_resolution = 2
    size = 64

if exists(output_file):
    print('File already exists at \'%s\'... Exiting' % output_file)
    exit()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

playlists = sp.current_user_playlists()
mesh_playlist_uri = ''

if playlist_name == None: #If no playlist specified, print options and get playlist name as input
    print('\nNo playlist specified. Please specify a playlist from the following list:\n')
    print('----Current User\'s Playlists----')
    for i, playlist in enumerate(playlists['items']):
        print('  %s' % playlist['name'])
    print('--------------------------------')
    playlist_name = str(input('\nInput playlist name: '))
    print()

while playlists: #Check if specified playlist exists for the current user.
    for i, playlist in enumerate(playlists['items']):
        if playlist['name'] == playlist_name: #If playlist exists, get the playlist uri and exit
            print('Playlist found!')
            mesh_playlist_uri = playlist['uri']
            break
    if playlists['next']: #If not all playlists were received in the first message, fetch more until complete
        playlists = sp.next(playlists)
    else: #Once all playlists have been checked and none match, exit
        playlists = None

if mesh_playlist_uri == '':
    print('Playlist not found... Exiting')
    exit()

if os.path.exists('album_art_temp/'):
    for f in glob.glob('album_art_temp/*.png'):
        os.remove(f)
else:
    os.mkdir('album_art_temp')

# sp.user_playlist_tracks("username", "playlist_id")
mesh_playlist = sp.playlist_items(mesh_playlist_uri, limit=100, offset=0, market='US', additional_types=('track', ))
# print(json.dumps(mesh_playlist['items'], sort_keys=True, indent=2))

print('Downloading album artwork...')

total_tracks = 0
total_albums = 0
album_list = []
album_nums = []

items = mesh_playlist['items']
while mesh_playlist['next']:
    mesh_playlist = sp.next(mesh_playlist)
    items.extend(mesh_playlist['items'])

for i in items:
    total_tracks += 1
    album_name = re.sub(r'["\n]', '',json.dumps(i['track']['album']['name'], sort_keys=True, indent=2))
    album_name = album_name.replace("\u2019", "\'")
    if album_name not in album_list:
        total_albums += 1
        album_list.append(album_name)
        album_nums.append(total_albums)
        print('  %d: %s' % (total_albums, album_name))

        album_url = re.sub(r'["\n]', '', json.dumps(i['track']['album']['images'][album_resolution]['url']))

        r = requests.get(album_url, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open('album_art_temp/%d.png' % total_albums,'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print('Image Couldn\'t be retreived')

print('Complete!')


print('Total unique albums: %d' % total_albums)
print('Total duplicates: %d' % (total_tracks - total_albums))

num_rows = int(input("How many rows? (how tall?): "))
num_columns = int(input("How many columns? (how long?): "))
used_albums = num_rows * num_columns
img_list = []

print('%d albums will be used' % used_albums)

if exists('album_art_temp/.DS_Store'):
    os.remove('album_art_temp/.DS_Store')
if exists('album_art_temp/.cache'):
    os.remove('album_art_temp/.cache')

for x in range(0,num_columns*num_rows):
    v_list = []
    file = random.choice(album_nums)
    album_nums.remove(file)
    img_list.append('album_art_temp/%s.png' % file)

imgs = [PIL.Image.open(i) for i in img_list]
assert len(imgs) == num_rows*num_columns

w, h = imgs[0].size
grid = Image.new('RGB', size=(num_columns*w, num_rows*h))
grid_w, grid_h = grid.size

for i, img in enumerate(imgs):
    grid.paste(img, box=(i%num_columns*w, i//num_columns*h))
    
grid.save(output_file)
shutil.rmtree('album_art_temp/')
print('Complete! Output image saved as \'output.jpg\'')