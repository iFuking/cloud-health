# encoding: utf-8
import requests

access_token = 'VJ0IVLFEzWg0MNS3lR_i-ZHL_GAyZD9zniSRRS0HgyKtKJWKIVq_ujZlrYYy6y9o-BAXxMrW3nhLl-eZN2gK43FEtvm5qV9NMCP6wm74WPgOWUjADAUCA'
article_id_api = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token=%s' % access_token
data = """{
    "articles": [
        {
            "thumb_media_id": "E5XTFkAmCO4kN2iRaucSMKk0WJvvnOD942QiIELZPVnELCsrMIuqo0oKDoJgQzlD",
            "author": "chmwang",
            "title": "哈哈",
            "content_source_url": "nba.hupu.com",
            "content": "呵呵",
            "digest": "digest",
            "show_cover_pic": "1"
        }
    ]
}"""

response = requests.post(article_id_api, data)
print response
print response.text