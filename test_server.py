import requests

print(
    requests.post('http://127.0.0.1:8000/',
                  json= {
                      "content" : """ 
{
  "type": "links",
  "text": "$1Step RT PCR Kit",
  "image": "https://resource.amerigoscientific.com/p-img/1-product-image.jpeg",
  "links": [
    {
      "url": "https://www.amerigoscientific.org/1step-rt-pcr-kit-item-237886.html",
      "text": "Click here to buy",
      //"icon": "http://zylker.com/help/home.png"
    }
  ]
}
"""        }
    ).json()
)