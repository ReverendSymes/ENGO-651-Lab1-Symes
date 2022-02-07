import requests
import json

res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "isbn:080213825X"})
bookinfo = res.json()
bookinfo = (bookinfo["items"][0])
title = (bookinfo["volumeInfo"]["title"])
authors = (bookinfo["volumeInfo"]["authors"])
publishedDate = (bookinfo["volumeInfo"]["publishedDate"])
ISBN_10 = (bookinfo["volumeInfo"]["industryIdentifiers"][0]["identifier"])
ISBN_13 = (bookinfo["volumeInfo"]["industryIdentifiers"][1]["identifier"])
reviewCount = (bookinfo["volumeInfo"]["ratingsCount"])
averageRating = (bookinfo["volumeInfo"]["averageRating"])

infor = {"title": title, "authors": authors, "publishedDate": publishedDate, "ISBN_10": ISBN_10, "ISBN_13": ISBN_13,"reviewCount": reviewCount,"averageRating": averageRating}

print(json.dumps(infor))
