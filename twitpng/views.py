# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse

import logging

from twython import Twython
from PIL import Image, ImageFont, ImageDraw
import os

__author__ = 'mrasmus'

IMAGE_WIDTH = 438
IMAGE_HEIGHT = 180
main_font = ImageFont.truetype("HelveticaNeue.ttf",14*2,encoding='unic')

def wraptext(text, width=(IMAGE_WIDTH-2)*2):
    words = text.split()
    result = ''
    while (words):
        count = 0
        while (main_font.getsize(' '.join(words[:count+1]))[0] < width) and (count < len(words)):
            count += 1
        result += ' '.join(words[:count]) + '\n'
        words = words[count:]
    return result

def post_longtweet(request):
    """An example view with Twython/OAuth hooks/calls to fetch data about the user in question."""
    #if request.method == 'GET':
    #    return HttpResponseRedirect('/')
    tweetbody = request.REQUEST['tweet']
    user = request.user.twitterprofile
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
                      user.oauth_token, user.oauth_secret)

    success = False
    if len(tweetbody) <= 140:
        try:
            twitter.update_status(status=tweetbody)
            success = True
        except:
            pass
        result = '|'+ tweetbody +'|'
    else:
        text = tweetbody[:(140-33)].rsplit(' ', 1)[0] + u'…'
        imgtext = wraptext(u'…' + tweetbody[len(text)-1:])
        height = len(imgtext.splitlines()) * main_font.getsize(imgtext)[1]
        result = '|'+ text +'|' + imgtext + '|'
        img = Image.new("RGBA", (IMAGE_WIDTH*2,IMAGE_HEIGHT*2),(255,255,255,255))
        draw = ImageDraw.Draw(img)
        h = 0
        for line in imgtext.splitlines():
            draw.text((1,h),line,(0,0,0),font=main_font)
            h += main_font.getsize(line)[1]

        img = img.resize((IMAGE_WIDTH,IMAGE_HEIGHT),Image.ANTIALIAS)

        filename = str(hash(imgtext)) + '.png'
        try:
            img.save(filename)
            imgfile = open(filename, 'rb')
            twitter.update_status_with_media(status=text, media=imgfile)
            imgfile.close()
            success = True
        except:
            pass

        os.remove(filename)


    #return HttpResponse(result)
    if (success):
        return HttpResponseRedirect('/tweetsent')
    else:
        HttpResponse('There was some issue! D: Links in tweets occasionally break things, try your tweet again w/out links. Working on fixing that one.<br><br> Redirecting...<meta http-equiv="refresh" content="5;url=/" />')

def tweet_sent(request):
    return HttpResponse('Tweet sent successfully! Redirecting...<meta http-equiv="refresh" content="3;url=/" />')