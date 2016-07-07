#!/usr/bin/python

# We only need to import this module
import os.path
import eyed3
import hashlib

# Create a hash for what files we found
file_hash = {}

### List out the files in the directory, write a temp file with the PATH, MD5 and MP3 info




# The top argument for walk. The
# Python27/Lib/site-packages folder in my case
topdir = '/Users/donalddanielson/Music/iTunes/iTunes Media/Music'
#topdir = '/Volumes/theseahasno/Music_Collection'

# The arg argument for walk, and subsequently ext for step
exten = '.mp3'


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()



def getEyeD3Tags(full_file_name):
        working_tag = eyed3.load(full_file_name)
        available_settings = (dir(working_tag.tag))

        if 'artist' in available_settings:
            print 'Artist: %s' % working_tag.tag.artist

        if 'album' in available_settings:
            print 'Album: %s' % working_tag.tag.album

        if 'title' in available_settings:
            print 'Title: %s' % working_tag.tag.title

        mp3_check = eyed3.mp3.isMp3File(full_file_name)

        print 'MP3 File check: %s' % mp3_check

        mp3_data = eyed3.mp3.Mp3AudioFile(full_file_name)
        print(mp3_data.info.sample_freq)
        bit_rate = mp3_data.info.bit_rate_str
        print(bit_rate.split(' ',0))




def step(ext, dirname, names):
    ext = ext.lower()

    for name in names:
        if name.lower().endswith(ext):
            full_name = os.path.join(dirname,name)
            getEyeD3Tags(full_name)
            temp_hash = hashfile(open(full_name, 'rb'), hashlib.sha256() )
            print (full_name, hashfile(open(full_name, 'rb'), hashlib.sha256() ) )
            file_hash[temp_hash] = full_name



# Start the walk
os.path.walk(topdir, step, exten)



### So we generate a list of all the files we have, and we have a SH256 digest of them.  So we then
#   copy them to the new target location IFF
#  There is not already a matching file there, checked by target PATH and Digest
#  We mark off the Digests we have seen for that path




