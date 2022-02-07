import requests
import json

res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "080213825X", "maxResults": 40,"projection": "lite"})
bookinfo = res.json()
# print(bookinfo["items"][0]["volumeInfo"]["title"])
# print(len(bookinfo["items"]))
# results = []
# results = []
# id = []
# for i in range(0,len(bookinfo["items"])-1):
#     tempbook = bookinfo["items"][i]["volumeInfo"]["title"]#,bookinfo["items"][i]["volumeInfo"]["authors"]]
#     tempid = bookinfo["items"][i]["id"]
#     results.append(tempbook)
#     id.append(tempid)
#
#
# print(id)

bookinfo = (bookinfo["items"][0])
# title = (bookinfo["volumeInfo"]["title"])
# authors = (bookinfo["volumeInfo"]["authors"])
# publishedDate = (bookinfo["volumeInfo"]["publishedDate"])
# ISBN_10 = (bookinfo["volumeInfo"]["industryIdentifiers"][0]["identifier"])
# ISBN_13 = (bookinfo["volumeInfo"]["industryIdentifiers"][1]["identifier"])
# reviewCount = (bookinfo["volumeInfo"]["ratingsCount"])
# averageRating = (bookinfo["volumeInfo"]["averageRating"])
pics = bookinfo["volumeInfo"]["imageLinks"]["thumbnail"]
print(pics)
# infor = {"title": title, "authors": authors, "publishedDate": publishedDate, "ISBN_10": ISBN_10, "ISBN_13": ISBN_13,"reviewCount": reviewCount,"averageRating": averageRating}
#
# print(json.dumps(infor))
