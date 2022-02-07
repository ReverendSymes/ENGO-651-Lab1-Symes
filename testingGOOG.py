import requests
import json

res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "rothfuss", "maxResults": 40,"projection": "lite"})
bookinfo = res.json()
print(bookinfo["items"][4]["volumeInfo"]["title"])
print(len(bookinfo["items"]))
results = []
for i in range(0,len(bookinfo["items"])-1):
    tempbook = bookinfo["items"][i]["volumeInfo"]["authors"][0]#,bookinfo["items"][i]["volumeInfo"]["authors"]]
    print(tempbook)
    results.append(tempbook)

print(results)

# bookinfo = (bookinfo["items"][0])
# title = (bookinfo["volumeInfo"]["title"])
# authors = (bookinfo["volumeInfo"]["authors"])
# publishedDate = (bookinfo["volumeInfo"]["publishedDate"])
# ISBN_10 = (bookinfo["volumeInfo"]["industryIdentifiers"][0]["identifier"])
# ISBN_13 = (bookinfo["volumeInfo"]["industryIdentifiers"][1]["identifier"])
# reviewCount = (bookinfo["volumeInfo"]["ratingsCount"])
# averageRating = (bookinfo["volumeInfo"]["averageRating"])
#
# infor = {"title": title, "authors": authors, "publishedDate": publishedDate, "ISBN_10": ISBN_10, "ISBN_13": ISBN_13,"reviewCount": reviewCount,"averageRating": averageRating}
#
# print(json.dumps(infor))
