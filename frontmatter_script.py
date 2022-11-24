import frontmatter
import os
from io import BytesIO
import datetime

notes = []
keys = ["date_created", "aliases", "tags", "course", "type"]
newMetadata = {}

# This script is meant to be run on obsidian.md vaults
# and will add frontmatter to all notes in the vault
# and add the following keys: date_created, aliases, tags, course, type
# This script is completely has no failsafes and will overwrite
# any and all existing frontmatter. Use at your own risk.


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith("md"):
                yield os.path.abspath(os.path.join(dirpath, f))


def importKeyValue(note, key, filepath):
    if key == "date_created":
        return creationDate(filepath)
    if key == "type":
        return "note"
    if key == "course":
        return ""
    if key == "tags":
        return []
    else:
        try:
            if note[key] is None:
                return []
            return note[key]
        except KeyError:
            return []


def creationDate(filename):
    stat = os.stat(filename)
    c_timestamp = stat.st_birthtime

    c_time = datetime.datetime.fromtimestamp(c_timestamp)
    return c_time.strftime("%Y-%m-%d %H:%m")


def formatFrontmatter(filepaths):
    dateInput = input("Put created date as first frontmatter value? (y/n): ")
    if dateInput == "n":
        dateSelection = False
    else:
        dateSelection = True
    for i in filepaths:
        note = frontmatter.load(i)
        for k in keys:
            newMetadata[k] = importKeyValue(note, k, i)
        if dateSelection is False:
            newMetadata["date_created"] = ""

        newNote = frontmatter.Post(
            content=note.content,
            date_created=newMetadata["date_created"],
            aliases=newMetadata["aliases"],
            tags=newMetadata["tags"],
            course=newMetadata["course"],
            type=newMetadata["type"],
        )
        f = BytesIO()
        with open(i, "wb") as f:
            frontmatter.dump(newNote, f, sort_keys=False)


if __name__ == "__main__":
    vaultPath = input("Enter the vault path: ")
    if vaultPath == "a":
        vaultPath = ""
    allPaths = absoluteFilePaths(vaultPath)
    formatFrontmatter(allPaths)
