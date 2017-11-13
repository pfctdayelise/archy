
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
        options = [{'title': o, 'payload': make_payload(o)} for o in self.opts]
        page.send(recipient,
                  self.q,
                  quick_replies=options,
                  metadata='DEVELOPER_DEFINED_METADATA')



data = [
    {'name': 'START_PAYLOAD',
     'response': [
         t('i cant help with everything, but I can help you do something'),
         opts('what is your particular shame today?',
              ['procrastination',
               'my mediocrity',
               'just overwhelmed',
               'so distracted',
              ]
         ),
     ]
    },
    {'name': 'procrastination',
     'response': [
         opts('apart from a white noise machine or a new brain what do you think would help you?', ['soothe me please', 'make me write']),
     ]
     },
    {'name': 'my mediocrity',
     'response': [
         t('that sounds unpleasant'),
         opts('what would help you right now?', ['advice me', 'spill my guts', 'roast me, archy']),
         ],
     },
    {'name': 'just overwhelmed',
     'response': [t('...tbc')],
     },
    {'name': 'so distracted',
     'response': [t('i am not very good at staying focused'),
                  t('i can tell u that everyone has a dirty floor so if you think y should clean it instead, dont bother'),
                  t('...tbc')],
     },
    
]

def make_payload(option):
    r = 'PICK_' + option.upper().replace(' ', '_').replace(',', '')
    unexpected = {l for l in r if l not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'}
    if unexpected:
        raise ValueError('Unexpected characters in option: %s' % option)
    return r


def make_callback(name):
    if name == 'START_PAYLOAD':
        return name
    return make_payload(name)


def functions(page):
    fns = {}
    for node in data:
        fn = lambda payload, event: [item.do(page, payload, event) for item in node['response']]
        # tricky, decorator with arg and fn with arg.
        # See http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#decorators-with-arguments
        fn = page.callback([make_callback(node['name'])])(fn)
        fns[make_callback(node['name']).lower()] = fn
        return fns


