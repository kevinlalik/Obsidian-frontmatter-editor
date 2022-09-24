import frontmatter
import os
from io import BytesIO
import datetime

notes = []
keys = ["date_created", "aliases", "tags"]
vaultPath = "/Users/kevin/Documents/Obsidian notes/Notes copy/"
newMetadata = {}


# yields each full filename of every .md file in the vaultPath
def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith("md"):
                yield os.path.abspath(os.path.join(dirpath, f))


# this function attempts to import the values of the frontmatter key
# if it doesn't exist it creates a new key value for a given key
def importKeyValue(note, key):
    try:
        print(key)
        # store value of note's aliases metadata
        newMetadata[key] = note[key]
        # if no values, initialize the value of the key as empty,
        # instead of insterting an empty string
        if note[key] is None:
            newMetadata[key] = []
    # if the key is non-existent, initialize the key-value pair
    except KeyError:
        newMetadata[key] = []


def creationDate(filename):
    stat = os.stat(filename)  # gets info of file
    c_timestamp = stat.st_birthtime  # stores timestamp of creation time
    # coverts timestamp into time
    c_time = datetime.datetime.fromtimestamp(c_timestamp)
    return c_time.strftime("%Y-%m-%d %H:%m")  # formats time


# function reads, edits and outputs new metadata to markdown files
def formatFrontmatter(filepaths):
    dateInput = input("Put created date as first frontmatter value? (y/n): ")
    if dateInput == "y":
        dateSelection = True
        date = True
    else:
        dateSelection = False
        date = False
    for i in filepaths:
        note = frontmatter.load(i)  # loading note using frontmatter import
        for k in keys:
            if date is True:
                newMetadata["date_created"] = creationDate(i)
                date = False
            else:
                importKeyValue(note, k)
        # create new post from scratch using new metadata
        date = dateSelection
        if date is True:
            newNote = frontmatter.Post(
                content=note.content,
                date_created=newMetadata["date_created"],
                aliases=newMetadata[keys[1]],
                tags=newMetadata[keys[2]],
            )
        else:
            newNote = frontmatter.Post(
                content=note.content,
                aliases=newMetadata[keys[1]],
                tags=newMetadata[keys[2]],
            )
        # saves current file.
        f = BytesIO()
        with open(i, "wb") as f:
            frontmatter.dump(newNote, f, sort_keys=False)


if __name__ == "__main__":
    # accumulating all filepaths to an array
    allPaths = absoluteFilePaths(vaultPath)
    # imports, edits, cleans and initializes all desired frontmatter keys
    formatFrontmatter(allPaths)
