from django.shortcuts import render
from django.http import HttpResponse
import json, io, requests, ssl
from PIL import Image
from collections import Counter 
from base64 import b16encode
from colorthief import ColorThief


def index(request):
    response = json.dumps({})
    return HttpResponse(response, content_type = 'text/json')    

def get_image_url(requset, image_url):
    # ssl certification
    ssl._create_default_https_context = ssl._create_unverified_context
    if requset.method == 'GET':
        try:
            res = requests.get(image_url)
            image_obj = io.BytesIO(res.content)
            image_org = Image.open(image_obj)

            # for borders
            border_pixel_rgb = [] 
            width, height = image_org.size

            # read the all pixels color
            for x in range(0, width):
                for y in range(0, height):
                    if x in [0, width] or y in [0, height]:
                        # check that pixel of border
                        r, g, b = image_org.getpixel((x, y))[:3]
                        border_pixel_rgb.append((r, g, b))
            
            # for dominant color
            dominant_color = ColorThief(image_obj)
            dominant_color = dominant_color.get_color(quality=1)
            logo_border_color = Counter(border_pixel_rgb).most_common(1)[0][0]
           
            # RGB to hex
            logo_border_color = (b'#'+b16encode(bytes(logo_border_color))).decode('utf-8')
            dominant_color = (b'#'+b16encode(bytes(dominant_color))).decode('utf-8')
            
            response = json.dumps(
                {
                    'logo_border': logo_border_color,
                    'dominant_color': dominant_color
                }
            )

        except:
            response = json.dumps({ 'Error' : 'invalid image url!' })
    else:
        response = json.dumps({ 'Error' : 'Try again(only GET request)!' })

    return HttpResponse(response, content_type = 'text/json') 

