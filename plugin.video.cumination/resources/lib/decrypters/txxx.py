# -*- coding: utf-8 -*-

import re
import base64
from resources.lib import utils


def Tdecode(vidurl):
    replacemap = {'M': r'\u041c', 'A': r'\u0410', 'B': r'\u0412', 'C': r'\u0421', 'E': r'\u0415', '=': '~', '+': '.', '/': ','}

    for key in replacemap:
        vidurl = vidurl.replace(replacemap[key], key)
    vidurl = base64.b64decode(vidurl)
    return vidurl.decode('utf-8')


def GetTxxxVideo(vidpage):
    vidpagecontent = utils.getHtml(vidpage)
    posturl = f"https://{vidpage.split('/')[2]}/sn4diyux.php"

    pC3 = re.search('''pC3:'([^']+)''', vidpagecontent)[1]
    vidid = re.search(r'''video_id["|']?:\s*(\d+)''', vidpagecontent)[1]
    data = f'{vidid},{pC3}'
    vidcontent = utils.getHtml(posturl, referer=vidpage, data={'param': data})
    vidurl = re.search('video_url":"([^"]+)', vidcontent)[1]
    vidurl = Tdecode(vidurl)

    return f"{vidurl}|Referer={vidpage}"
