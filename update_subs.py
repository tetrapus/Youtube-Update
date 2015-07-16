"""
Download youtube subscriptions.

Usage:
    ./update_subs.py [options] [<folder>...]

Options:
    -a URL      Add subscription to folder(s)
    -n NUM      Only check the first NUM videos [default: 5]
    -r          Perform action on all subfolders recursively
"""

import json
import datetime
import time
import docopt
import collections
from pathlib import Path

import youtube_dl

args = docopt.docopt(__doc__)

folders = collections.deque([Path(i).resolve() for i in args["<folder>"]])
if not folders:
    folders.append(Path(".").resolve())

visited = set()

while folders:
    folder = folders.popleft()
    if folder in visited:
        continue
    else:
        visited.add(folder)
    settings_path = folder/"settings.json"
    downloaded = folder/"downloaded.ydl"

    try:
        with settings_path.open() as f:
            settings = json.load(f)
    except (FileNotFoundError, ValueError):
        if args["-a"] is not None:
            settings_path.open("w").close()
            settings = []
        else:
            if args["-r"]:
                folders.extend({Path(d).resolve() for d in folder.iterdir() if d.is_dir() and d not in folders and d not in visited})
            continue

    if args["-a"] is not None:
        settings.append({"url": args["-a"], "updated": time.time()-7*3600})
    else:
        for subscription in settings:
            date = youtube_dl.utils.DateRange()
            date.start = datetime.datetime.utcfromtimestamp(subscription["updated"]).date() 
            options = {"daterange": date, "download_archive": downloaded.as_posix(), "playlistend": int(args["-n"])}
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([subscription["url"]])
            subscription["updated"] = time.time() - 7*3600

    with settings_path.open("w") as f:
        json.dump(settings, f)

    if args["-r"]:
        folders.extend({Path(d).resolve() for d in folder.iterdir() if d.is_dir() and d not in folders and d not in visited})