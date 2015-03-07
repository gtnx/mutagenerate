# -*- coding: utf-8 -*-

from log import logger
from util import query_yes_no

import requests
from bs4 import BeautifulSoup
import urllib
from mutagen.id3 import TALB, APIC, WXXX, TCON


class Source(object):
    def generate(self, id3, update=False):
        logger.info("Generating dummy sources for %s" % id3.pprint().replace("\n", ", "))
        retval = self._generate(id3, update)
        logger.info("Generated dummy sources for %s" % id3.pprint().replace("\n", ", "))
        return retval

    def generate_and_save(self, id3, update=False, yes=False):
        if self.generate(id3, update) and (yes or query_yes_no("Confirm saving ?")):
            id3.save()


class AmazonSource(Source):
    def __init__(self):
        self.url = """http://www.amazon.fr/s/ref=nb_sb_noss?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Ddigital-music&field-keywords=KEYWORD&rh=n%3A77196031%2Ck%3AKEYWORD&ajr=0"""

    def _generate(self, id3, update=False):
        kw = "%s %s" % (id3["TPE1"].text[0], id3["TIT2"].text[0])
        url = self.url.replace("KEYWORD", urllib.quote_plus(kw.encode("utf8")))
        logger.debug("Crawling %(url)s" % locals())
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        results = soup.select("table.mp3Tracks tr td.songTitle a")
        if not results:
            logger.warning("No results for %(kw)s" % locals())
            return False
        result = results[0]
        url = result.get("href")
        logger.debug("Found specific url: %(url)s" % locals())
        soup = BeautifulSoup(requests.get(url).content)
        id3.add(WXXX(encoding=3, desc=u"Amazon url", url=url))
        album = soup.select("#fromAlbum a")
        if album and (update or "TALB" not in id3):
            id3.add(TALB(encoding=3, text=album[0].find(text=True).strip(" \n")))
        images = soup.select("div#coverArt_feature_div img")
        if images and (update or "APIC" not in id3):
            data = requests.get(images[0].get("src")).content
            id3.add(APIC(encoding=3, mime="image/jpeg", type=3, desc=u"Cover", data=data))
        details = [filter(lambda x: x not in ("\n", "", " "), detail.find_all(text=True)) for detail in soup.select("div.content li") if detail.find("strong")]
        for detail in details:
            if detail and detail[0] == "Genres:" and (update or "TCON" not in id3) and len(detail) >= 2:
                id3.add(TCON(encoding=3, text=detail[1]))
        return True
