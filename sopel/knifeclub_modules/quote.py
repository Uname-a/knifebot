from sopel import *
import random

qdb = "/home/dimaa/.sopel/quote.db"

@module.commands('addquote')
def addquote(bot, trigger):
        quote = trigger.group(2)
        f = open(qdb, 'a')
        f.write("\n%s" % quote)
        f.close()
        bot.reply('Added it...')


@module.commands('quote')
def quote(bot, trigger):
        f = open(qdb, 'r')
        line = random.choice(list(open(qdb)))
        bot.say(line)