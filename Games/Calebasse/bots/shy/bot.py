#!/usr/bin/env python2
#-*- coding:utf8-*-  
import json

# The bot is initialized
print "OK"

# Getting his id
uuid = raw_input()

# Ready to start
print "OK"

while raw_input()!='Q':
    # get accounts
    accounts =json.loads(raw_input()) 

    # go to bets
    while raw_input() != "Accepted":
        print min(account[uuid],5)

    # Get bets of everybody
    bets = json.loads(raw_input())

    # Get the winner
    winner = json.loads(raw_input())

