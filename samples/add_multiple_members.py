#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from spark.rooms import Room
from spark.session import Session
from spark.memberships import Membership

SPARK_KEY = 'you key'
SPARK_ROOM = 'SpartTestRoom2'


if __name__ == '__main__':
	try:
		ss = Session('https://api.ciscospark.com', SPARK_KEY)
		members = []
		with open('sample.csv', 'r') as memfile:
			reader = csv.reader(memfile, delimiter=',')
			for row in reader:
				if '@' not in row[0]:
					members.append(row[0]+'@cisco.com')
				else:
					members.append(row[0])

		room = Room.get(ss, SPARK_ROOM)
		if not isinstance(room, Room):
			room = Room()
			room.title = SPARK_ROOM
			room.create(ss)
		for m in members:
			Membership.create( ss, room.id, m)
		room.send_message(ss, "안녕하세요 :) 테스트로 추가했습니다. 이해해주세요 ~~ .!!")
	except ValueError:
		exit("  Exiting as I failed to authenticate your Spark API key")
