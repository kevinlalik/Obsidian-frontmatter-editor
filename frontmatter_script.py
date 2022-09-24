import frontmatter
import os
from io import BytesIO
import datetime

notes = []

# get all .md file paths
def absoluteFilePaths(directory):
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			if f.endswith('md'):
				yield os.path.abspath(os.path.join(dirpath, f))

allPaths = absoluteFilePaths("/Users/kevin/Documents/Obsidian notes/Notes/")





def getKeyValuePairs(filepaths):
	for i in filepaths:
		note = frontmatter.load(i)
		stat = os.stat(i)
		c_timestamp = stat.st_birthtime
		c_time = datetime.datetime.fromtimestamp(c_timestamp)
		obsidian_time = c_time.strftime("%Y-%m-%d %H:%m")
		newMetadata = {}
		newMetadata["date_created"] = obsidian_time
		try:
			try:
				newMetadata["aliases"] = note["aliases"]
				if note["aliases"] is None:
					newMetadata["aliases"] = []
			except KeyError: 
				newMetadata["aliases"] = note["alias"]
				if note["aliases"] is None:
					newMetadata["aliases"] = []
		except:
			newMetadata["aliases"] = []
		try:
			newMetadata["tags"] = note["tags"]
			if note["tags"] is None:
					newMetadata["tags"] = []
		except: 
			newMetadata["tags"] = []


		newNote = frontmatter.Post(content=note.content, date_created=newMetadata["date_created"], aliases=newMetadata["aliases"], tags=newMetadata["tags"])

		f = BytesIO()
		with open(i, 'wb') as f:
			frontmatter.dump(newNote, f, sort_keys=False)
	# note.metadata = newMetadata
	# print(note.metadata)
	# print(f)
	# print(note)
	# with open(filepath, "wb"):
	# 	frontmatter.dump(newNote, f)

# load each note to posts

newNotes = getKeyValuePairs(allPaths)

# for i in newNotes:
# 	print(i)
# 	print(i.metadata)
# 	with open






