#!/usr/bin/python

# We only need to import this module
import os
import eyed3
import hashlib
import shutil

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

### List out the files in the directory, write a temp file with the PATH, MD5 and MP3 info

# The top argument for walk. The
# Python27/Lib/site-packages folder in my case
#topdir = '/Users/donalddanielson/Music/iTunes/iTunes Media/Music'
topdir = '/Volumes/theseahasno/Music_Collection'
target_dir = "/Users/donalddanielson/New_Music"

# The arg argument for walk, and subsequently ext for step
exten ='.mp3'
seen_this_file = dict()



### Begin walk of the source directory
for directory, dirnames, files in os.walk(topdir, topdown=True):

    for name in files:
        working_file = os.path.join(directory, name)
        working_path_parts = working_file.split(os.sep)
        source_name = working_path_parts.pop()
        source_album = working_path_parts.pop()
        source_artist = working_path_parts.pop()

        print "Source artist and album", source_artist , source_album

        if name.lower().endswith(exten):

            working_file_hash = hashfile(open(working_file, 'rb'), hashlib.sha256() )

            if working_file_hash in seen_this_file:
                print "Found duplicate" , working_file
                seen_this_file[working_file_hash] += 1
            else:
                print "Found a new file" , working_file
                seen_this_file[working_file_hash] = 1
                # Check the MP3 metadata to see if its complete, then use that to
                ## copy the file to the target location
                working_tag = eyed3.load(working_file)
                available_settings = (dir(working_tag.tag))

                if 'artist' in available_settings:
                    working_artist =  working_tag.tag.artist
                else:
                    print "Missing Artist Info", working_file

                if 'album' in available_settings:
                    working_album =  working_tag.tag.album
                else:
                    print "Missing Album Info", working_file

                if 'title' in available_settings:
                    working_title =  working_tag.tag.title
                else:
                    print "Missing Title Info" , working_file


                mp3_check = eyed3.mp3.isMp3File(working_file)

                mp3_data = eyed3.mp3.Mp3AudioFile(working_file)

                bit_rate = mp3_data.info.bit_rate_str

                target_file = target_dir + "/" + source_artist +  "/" + source_album + "/" + name
                target_artist_album_path = target_dir + "/" + source_artist +  "/" + source_album

                print working_album, working_artist, working_title, mp3_check, (mp3_data.info.sample_freq), (bit_rate.split(' ',0))
                print "   Target file location: " , target_dir + "/" + source_artist +  "/" + source_album + "/" + name

                if  os.path.isfile(target_file):
                    print "There is a file with that name and location already"
                else:
                    print "Location is clear, copying file"
                    ### Check to see if directory path exists, if not, create
                    if os.path.isdir(target_artist_album_path):
                        print "Target location exists", target_artist_album_path
                    else:
                        print "Target location missing, need to create first"
                        mkdir_p(target_artist_album_path)

                    shutil.copyfile(working_file , target_file )

        #print working_file, working_file_hash

