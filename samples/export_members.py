#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from spark.rooms import Room
from spark.session import Session
from spark.memberships import Membership

SPARK_KEY = 'OWI4MzhkYjUtYjA3MS00Njc1LWIyMzgtNTQ3YWVlZTJhMjJjNmFhY2U1YjAtNDU2'


if __name__ == '__main__':
	index = 0
	qs = {'roomId': None}
	try:
		ss = Session('https://api.ciscospark.com', SPARK_KEY)
		rooms = Room.get(ss)
		print 'Select room for exporting member lists'

		for i,room in enumerate(rooms):
			try:
				print "{}. {}".format(i, room.title)
			except :
				pass
		index = input('Enter number. ')

		room = rooms[index]
		qs['roomId'] = room.id
		members = Membership.get_room_members(ss, qs)
		with open('export.csv', 'w') as memfile:
			writer = csv.writer(memfile, delimiter=',')
			writer.writerow( ['member'])
			for member in members:
				writer.writerow( [ member.personEmail] )
			print 'Total {} members are saved on export.csv'.format(len(members))

	except ValueError as e:
		print e
		exit("  Exiting as I failed to authenticate your Spark API key")


