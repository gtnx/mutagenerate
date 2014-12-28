# mutagenerate

Expanding automatically id3 tags using available web resources (Amazon for instance). Based on mutagen.

## Motivation

You may have songs with very few tags (only title & artist for example) and you want to have more info so that your music database is the most complete. For instance, having normalized genres will allow you to easily build playslists. Time is precious and filling manually those info seems a monkey work to you. The goal of this package is to build automatically this info with reasonnable error rate.

## Ideas

In many cases, having the title & the artist is not ambiguous and is enough to gather other tags by querying available web resources. 
Amazon have a huge database and querying it with those two info often gives you the good result in first position.

The package queries Amazon and then gather the following info:

- Genre
- Album
- Cover
- Amazon url

## Usage

`mid3generate.py --filename "My Song.mp3"`