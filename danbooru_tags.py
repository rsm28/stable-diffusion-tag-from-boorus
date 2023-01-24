# fetch tags from a post using danbooru API
import requests
import re, os
import pyperclip
from pybooru import Danbooru

BLACKLIST = [
    "censored",
    "bar censor",
    "mosaic censoring",
    "blank censor",
    "blur censor",
    "glitch censor",
    "heart censor",
    "light censor",
    "mosaic censor",
    "novelty censor",
    "character censor",
    "text censor",
    "flower censor",
    "interface censor",
    "flower censor",
    "identity censor",
    "fake censor",
    "censored text",
    "censored gesture",
    "monochrome",
    "greyscale",
    "comic",
    "greyscale with colored background",
]

# url = input("Enter the URL of the post: ")
#

# id = match[0]

# print(id)


def getTags(post_link, username_, api_key_):
    match = re.findall(r"\d+", post_link)
    post_id = match[0]

    client = Danbooru("danbooru", username=username_, api_key=api_key_)
    print(f"post_id: {post_id}, username: {username_}, api_key: {api_key_}")
    post = client.post_show(post_id)

    # print response in console

    general_tags = post["tag_string_general"]
    character_tags = post["tag_string_character"]

    # find parantheses in character tags, and add backslash to escape them
    character_tags = re.sub(r"[()]", r"\\\g<0>", character_tags)
    general_tags = re.sub(r"[()]", r"\\\g<0>", general_tags)

    # set character tag to first entry in character tag list
    character_tags = character_tags.split(" ")[0]
    # surround character tags with parentheses, with ":1.3" at the end
    character_tags = "(" + character_tags + ":1.3)"
    if character_tags == "(:1.3)":
        character_tags = ""
    character_tags = character_tags.replace("_", " ")

    general_tags = general_tags.replace(" ", ", ")
    general_tags = general_tags.replace("_", " ")

    for tag in BLACKLIST:
        if tag in general_tags:
            general_tags = general_tags.replace(tag, "")
        else:
            pass

    output_tags = character_tags + " " + general_tags

    return output_tags


# def format():
#     arr = full_tags.split(" ")
#     #replace underscores with spaces
#     for i in range(len(arr)):
#         arr[i] = arr[i].replace("_", " ")
#     #create new file called danbooru_tags.txt
#     if os.path.exists("danbooru_tags.txt"):
#         os.remove("danbooru_tags.txt")
#     else:
#         pass
#     with open("danbooru_tags.txt", "a+") as f:
#         for i in arr:
#         #if tag is in blacklist, don't write to file
#             if i in BLACKLIST:
#                 pass
#             else:
#                 f.write(i + ", ")
#     return []

# get the tags
# full_tags = getTags(id)
# format()

# fo = open("danbooru_tags.txt", 'r').read()
# pyperclip.copy(fo)
