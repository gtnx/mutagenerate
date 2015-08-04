============
mutagenerate
============

.. image:: https://travis-ci.org/gtnx/mutagenerate.svg?branch=master
    :target: https://travis-ci.org/gtnx/mutagenerate


Expanding automatically id3 tags using available web resources (Amazon
for instance). Based on mutagen.

Motivation
----------

You may have songs with very few tags (only title & artist for example)
and you want to have more info so that your music database is the most
complete. For instance, having normalized genres will allow you to
easily build playslists. Time is precious and filling manually those
info seems a monkey work to you. The goal of this package is to build
automatically this info with reasonnable error rate.

Ideas
-----

In many cases, having the title & the artist is not ambiguous and is
enough to gather other tags by querying available web resources. Amazon
have a huge database and querying it with those two info often gives you
the good result in first position.

The package queries Amazon and then gather the following info:

-  Genre
-  Album
-  Cover
-  Amazon url

Usage
-----

Using binary
~~~~~~~~~~~~

Use only Amazon first results

::

    mid3generate.py --source amazon "My Song.mp3"

Use MusicBrainz API

::

    mid3generate.py --source musicbrainz "My Song.mp3"


Human listing of id3 tagged files

:: 

    mid3ls ~/Music
                                                                      filename |      artist |                                 album |                                           title | track | genre |  cover | year
           The Beatles - Sgt. Pepper's Lonely Hearts Club Band-DP82hSD_BXU.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |           Sgt. Pepper’s Lonely Hearts Club Band |     1 |   Pop | 30734c | 1987
              The Beatles - With a Little Help from My Friends-aXYdXBbVhU4.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |              With a Little Help From My Friends |     2 |   Pop | 30734c | 1987
                   The Beatles - Lucy in the Sky with Diamonds-e38oGAJ09f8.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                   Lucy in the Sky With Diamonds |     3 |   Pop | 30734c | 1987
                                  The Beatles - Getting Better-QxqueWiTrPA.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                                  Getting Better |     4 |   Pop | 30734c | 1987
                                   The Beatles - Fixing a Hole-SZXZRtsuN8s.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                                   Fixing a Hole |     5 |   Pop | 30734c | 1987
                              The Beatles - She's Leaving Home-oxYpUlcuQSM.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                              She’s Leaving Home |     6 |   Pop | 30734c | 1987
              The Beatles - Being for the Benefit of Mr. Kite!--ly7NYOLGck.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |              Being for the Benefit of Mr. Kite! |     7 |   Pop | 30734c | 1987
                          The Beatles - Within You Without You-xVuZ83XgA9A.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                          Within You Without You |     8 |   Pop | 30734c | 1987
                             The Beatles - When I'm Sixty-Four-P0IgrkFMinI.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                             When I’m Sixty‐Four |     9 |   Pop | 30734c | 1987
                                     The Beatles - Lovely Rita-f00-n_blwC4.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                                     Lovely Rita |    10 |   Pop | 30734c | 1987
                       The Beatles - Good Morning Good Morning-as9txvOctPc.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                       Good Morning Good Morning |    11 |   Pop | 30734c | 1987
 The Beatles  - Sgt. Pepper's Lonely Hearts Club Band(Reprise)-RPovvrhlBJM.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band | Sgt. Pepper’s Lonely Hearts Club Band (reprise) |    12 |   Pop | 30734c | 1987
                               The Beatles - A Day in the Life-shZh-gFCeVU.mp3 | The Beatles | Sgt. Pepper’s Lonely Hearts Club Band |                               A Day in the Life |    13 |   Pop | 30734c | 1987

Set cover for files

::

    mid3cover --set-cover path/to/cover song1.mp3 song2.m4a

Expand cover

::

    mid3cover --expand-cover song1.mp3 song2.mp3

Using library
~~~~~~~~~~~~~

::

    from mutagen.id3 import ID3
    from mutagenerate.amazon import AmazonSource
    from mutagenerate.musicbrainz import MusicBrainzSource

    mp3 = ID3("My Song.mp3")
    AmazonSource().generate_and_save(mp3, update=False, yes=True)
    user = 'my-user-here'
    password = 'my-password-here'
    MusicBrainzSource(user, password).generate_and_save(mp3, update=False, yes=True)
