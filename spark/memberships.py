import json
import spark.messages
import spark.rooms

class Membership(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['roomId'] = None
            self.attributes['personEmail'] = None
            self.attributes['isModerator'] = False

    @classmethod
    def url(cls):
        return '/memberships'

    @property
    def id(self):
        return self.attributes['id']

    @id.setter
    def id(self, val):
        self.attributes['id'] = val

    @property
    def personEmail(self):
        return self.attributes['personEmail']

    @personEmail.setter
    def personEmail(self, val):
        self.attributes['personEmail'] = val

    @property
    def isModerator(self):
        return self.attributes['isModerator']

    @isModerator.setter
    def isModerator(self, val):
        self.attributes['isModerator'] = val

    @property
    def roomId(self):
        return self.attributes['roomId']

    @roomId.setter
    def roomId(self, val):
        self.attributes['roomId'] = val

    @property
    def personId(self):
        return self.attributes['personId']

    @personId.setter
    def personId(self, val):
        self.attributes['personId'] = val

    @property
    def created(self):
        return self.attributes['created']

    @created.setter
    def created(self, val):
        self.attributes['created'] = val

    @classmethod
    def get(cls, session):
        """
        Retrieve membership list
        :param session: Session object
        :return: list membership available in the current session
        """
        ret = []
        memberships = json.loads(session.get(cls.url()).text)['items']
        for membership in memberships:
            obj = cls.from_json(membership)
            ret.append(obj)
        return ret

    @classmethod
    def create(cls, session, room, email):
        url = cls.url()
        m = Membership()
        m.roomId = room
        m.personEmail = email 
        resp = session.post(url, m.json())

        #update attributes after creating
        data = resp.json()
        if resp.status_code == 200:
            m.id = data['id']
            m.created = data['created']
            m.personId = data['personId']
        else:
        	m.id = None
        	m.roomId = None
        	m.personEmail = None
        return m

    def delete(self, session):
    	if self.id == None:
    		return None
        url = self.url() + '/{}'.format(self.id)
        resp = session.delete(url)
        return resp

    def json(self):
        return json.dumps(self.attributes)

    @classmethod
    def from_json(cls, obj):
        if isinstance(obj, dict):
            obj = cls(attributes=obj)
        elif isinstance(obj, (str, unicode)):
            obj = cls(attributes=json.loads(obj))
        else:
            raise TypeError('Data must be str or dict')
        return obj