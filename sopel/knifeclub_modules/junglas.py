# coding=utf8
"""Junglas module for Sopel"""
from sopel import *

@module.rule('.*((j+u+)|(h+oo+))n+g+l+a+s+.*')
def junglas(bot, trigger): 
    bot.say("HOOOOOOONGLAAAAASSSSSSSSSSS!!!!!111!!!111 I'm testing quotes :P")
