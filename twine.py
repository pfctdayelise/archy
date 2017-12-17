
class Response:
    def do(self, page, payload, event):
        pass


class t(Response):
    def __init__(self, text):
        self.text = text

    def do(self, page, payload, event):
        recipient = event.sender_id
        page.send(recipient, self.text)


class opts(Response):
    def __init__(self, q, options):
        self.q = q
        self.options = options

    def do(self, page, payload, event):
        recipient = event.sender_id
        qrs = [{'title': o, 'payload': make_payload(o)} for o in self.options]
        print('QRs:', qrs)
        page.send(recipient,
                  self.q,
                  quick_replies=qrs,
                  metadata='DEVELOPER_DEFINED_METADATA')



data = [
     {'name': 'procrastination',
     'response': [
         opts('apart from a white noise machine or a new brain what do you think would help you?', ['soothe me please', 'make me write']),
     ],
     },
    {'name': 'just overwhelmed',
     'response': [t('...tbc')],
     },
    {'name': 'so distracted',
     'response': [t('i am not very good at staying focused'),
                  t('i can tell u that everyone has a dirty floor so if you think you should clean it instead, dont bother'),
                  t('...tbc'),
                  ],
     },
    {'name': 'my mediocrity',
     'response': [
         t('that sounds unpleasant'),
         opts('what would help you right now?', ['advice me', 'spill my guts', 'roast me, archy']),
         ],
     },
    
]
