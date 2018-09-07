class Message(object):

    def __init__(self, id, ts, user, text):
        self.id = id
        self.ts = ts
        self.user = user
        self.text = text

    def clean(self):
        res = self.text.lower()
        for char in '-.,\n':
            res = self.text.replace(char,' ')
        self.text = res
