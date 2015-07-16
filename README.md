# Youtube-Update
Download youtube subscriptions.

Usage:
    ./update_subs.py [options] [<folder>...]

Options:
    -a URL      Add subscription to folder(s)
    -n NUM      Only check the first NUM videos [default: 5]
    -r          Perform action on all subfolders recursively
    
## Installation
Make sure you have python3.4+ installed. Run `pip3 install -r requirements.txt`.

## Adding subscription folders
Find the URL of the youtube subscription or other URL supported by youtube_dl. For youtube subscriptions, go to the channel page and provide the URL of the "Videos" tab.
Run `./update_subs.py -a <URL> <FOLDER>`. If FOLDER does not exist, it will be created for you. You may add multiple subscriptions to the same folder if you wish.

You may try running `./update_subs.py <FOLDER>` to initialise the download archive, but this will also download any videos uploaded on the current date.

## Downloading your subscriptions
Run `./update_subs.py <FOLDER>` to update a folder. By default, the script only downloads the latest 5: you can change this with the -n flag based on download frequency, but this also means the number of webpages youtube-dl must download may increase.

You can supply multiple folders or use the -r flag to update all subfolders.
