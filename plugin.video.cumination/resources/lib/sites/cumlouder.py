"""
    Cumination
    Copyright (C) 2020 Team Cumination

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re

from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('cumlouder', '[COLOR hotpink]Cum Louder[/COLOR]', 'https://www.cumlouder.com/', 'cumlouder.jpg', 'cumlouder')


@site.register(default_mode=True)
def Main():
    site.add_dir(
        '[COLOR hotpink]Categories[/COLOR]',
        f'{site.url}categories/',
        'Categories',
        site.img_cat,
    )
    site.add_dir(
        '[COLOR hotpink]Channels[/COLOR]',
        f'{site.url}channels/',
        'Channels',
        site.img_cat,
    )
    site.add_dir(
        '[COLOR hotpink]Series[/COLOR]',
        f'{site.url}series/',
        'Series',
        site.img_cat,
    )
    site.add_dir(
        '[COLOR hotpink]Pornstars[/COLOR]',
        f'{site.url}girls/',
        'Girls',
        site.img_cat,
    )
    site.add_dir(
        '[COLOR hotpink]Search[/COLOR]',
        f'{site.url}search/?q=',
        'Search',
        site.img_search,
    )
    List(f'{site.url}porn/')
    utils.eod()


@site.register()
def List(url):
    listhtml = utils.getHtml(url, site.url)
    match = re.compile(r'class="muestra-escena".+?ClickVideo\((\d+).+?data-src="([^"]+)".+?alt="([^"]+)".+?class="ico-minutos sprite"></span>\s*([^<]+)(.*?)/a>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name, duration, hd in match:
        hd = 'HD' if 'hd sprite' in hd else ''
        duration = duration.split(' ')[0] if 'm' in duration else duration.split(' ')[0] + ':00'
        name = utils.cleantext(name)
        videopage = '{0}embed/{1}/'.format(site.url, videopage)
        if img.startswith('//'):
            img = f'https:{img}'
        site.add_download_link(name, videopage, 'Playvid', img, name, duration=duration, quality=hd)

    if nextp := re.compile(
        r'class="btn-pagination"\s*itemprop="name"\s*href="([^"]+)">Next',
        re.DOTALL | re.IGNORECASE,
    ).search(listhtml):
        site.add_dir('Next Page', site.url[:-1] + nextp[1], 'List', site.img_next)

    utils.eod()


@site.register()
def Playvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download=download)
    vp.play_from_link_to_resolve(url)


@site.register()
def Categories(url):
    nextpg = True
    match = []
    while nextpg:
        cathtml = utils.getHtml(url, site.url)
        match += re.compile(r'tag-url.+?href="([^"]+).+?data-src="([^"]+).+?goria">\s*(.*?)\s*<.+?dad">([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
        if np := re.compile(
            r'class="btn-pagination"\s*itemprop="name"\s*href="([^"]+)">Next',
            re.DOTALL | re.IGNORECASE,
        ).search(cathtml):
            url = site.url[:-1] + np[1]
        else:
            nextpg = False
    match = sorted(match, key=lambda x: x[2])
    for catpage, img, name, videos in match:
        if catpage.startswith('/'):
            catpage = site.url[:-1] + catpage
        if img.startswith('//'):
            img = f'https:{img}'
        name = f"{name} [COLOR deeppink]{videos} Videos[/COLOR]"
        site.add_dir(name, catpage, 'List', img)
    utils.eod()


@site.register()
def Channels(url):
    nextpg = True
    match = []
    while nextpg:
        cathtml = utils.getHtml(url, site.url)
        match += re.compile(r'channel-url.+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+).+?videos\s.+?\s([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
        if np := re.compile(
            r'class="btn-pagination"\s*itemprop="name"\s*href="([^"]+)">Next',
            re.DOTALL | re.IGNORECASE,
        ).search(cathtml):
            url = site.url[:-1] + np[1]
        else:
            nextpg = False
    match = sorted(match, key=lambda x: x[2])
    for catpage, img, name, videos in match:
        if catpage.startswith('/'):
            catpage = site.url[:-1] + catpage
        if img.startswith('//'):
            img = f'https:{img}'
        name = f"{name} [COLOR deeppink]{videos}[/COLOR]"
        site.add_dir(name, catpage, 'List', img)
    utils.eod()


@site.register()
def Series(url):
    nextpg = True
    match = []
    while nextpg:
        cathtml = utils.getHtml(url, site.url)
        match += re.compile(r'<div\s*itemprop.+?href="([^"]+).+?data-src="([^"]+).+?name">([^<]+).+?p>([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
        if np := re.compile(
            r'class="btn-pagination"\s*itemprop="name"\s*href="([^"]+)">Next',
            re.DOTALL | re.IGNORECASE,
        ).search(cathtml):
            url = site.url[:-1] + np[1]
        else:
            nextpg = False
    match = sorted(match, key=lambda x: x[2])
    for catpage, img, name, videos in match:
        if catpage.startswith('/'):
            catpage = site.url[:-1] + catpage
        if img.startswith('//'):
            img = f'https:{img}'
        name = f"{name.title()} [COLOR deeppink]{videos}[/COLOR]"
        site.add_dir(name, catpage, 'List', img)
    utils.eod()


@site.register()
def Girls(url):
    cathtml = utils.getHtml(url, site.url)
    match = re.compile(r'girl-url.+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+).+?videos\s.+?\s([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, img, name, videos in match:
        if catpage.startswith('/'):
            catpage = site.url[:-1] + catpage
        if img.startswith('//'):
            img = f'https:{img}'
        name = f"{name} [COLOR deeppink]{videos}[/COLOR]"
        site.add_dir(name, catpage, 'List', img)

    if np := re.compile(
        r'class="btn-pagination"\s*itemprop="name"\s*href="([^"]+)">Next',
        re.DOTALL | re.IGNORECASE,
    ).search(cathtml):
        site.add_dir('Next Page', site.url[:-1] + np[1], 'Girls', site.img_next)

    utils.eod()


@site.register()
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(searchUrl, 'Search')
    else:
        title = keyword.replace(' ', '+')
        searchUrl = searchUrl + title
        List(searchUrl)
