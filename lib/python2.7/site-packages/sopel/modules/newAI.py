# -*- coding: utf-8 -*-

# Copyright (C) 2015 Lee Watson

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from random import randrange, random, randint
from sopel.formatting import bold, color, colors
from sopel.module import rule, commands, event, require_admin, interval
import markovify

markov = None
default_chattiness = 0
markov_file = None


@interval(60 * 30)
def load_markov(bot):
    global markov, markov_file
    markov_file = os.path.join(bot.config.core.homedir, "markov.txt")
    with open(markov_file, 'r+') as f:
        text = f.read()
    markov = markovify.Text(text)


def setup(bot):
    load_markov(bot)


@require_admin
@commands('chattiness')
def ai(bot, trigger):
    global default_chattiness
    chattiness = bot.db.get_channel_value(trigger.sender, 'ai_chattiness')
    if chattiness is None:
        chattiness = default_chattiness
    args = trigger.group(2)
    if not args:
        bot.reply('Current chattiness: {0}'.format(chattiness))
    else:
        chattiness = int(float(''.join(args)))
        chattiness = 100 if chattiness > 100 else 0 if chattiness < 0 else chattiness
        bot.db.set_channel_value(trigger.sender, 'ai_chattiness', chattiness)
        bot.reply("Chattiness set to {0}".format(chattiness))


@rule('.*')
@event("PRIVMSG")
def respond(bot, trigger):
    if trigger.nick == bot.config.core.nick:
        return
    if trigger.group().startswith('.'):
        return
    chattiness = bot.db.get_channel_value(trigger.sender, 'ai_chattiness')
    if chattiness is None:
        chattiness = default_chattiness
    with open(markov_file, 'a') as f:
        f.write(trigger.group() + '\n')
    if chattiness == 0:
        return
    if randrange(1, 100) <= chattiness or bot.config.core.name in trigger.group():
        bot.say(markov.make_short_sentence(150, tries=30).strip())
