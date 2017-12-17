
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
    # {'name': 'START_PAYLOAD',
    #  'response': [
    #      t('i cant help with everything, but I can help you do something'),
    #      opts('what is your particular shame today?',
    #           ['procrastination',
    #            'my mediocrity',
    #            'just overwhelmed',
    #            'so distracted',
    #           ]
    #      ),
    #  ]
    # },
     {'name': 'procrastination',
     'response': [
         opts('apart from a white noise machine or a new brain what do you think would help you?', ['soothe me please', 'make me write']),
     ],
      'types': ['QUICK_REPLY'],
     },
    {'name': 'just overwhelmed',
     'response': [t('...tbc')],
      'types': ['QUICK_REPLY'],
     },
    {'name': 'so distracted',
     'response': [t('i am not very good at staying focused'),
                  t('i can tell u that everyone has a dirty floor so if you think you should clean it instead, dont bother'),
                  t('...tbc'),
                  opts('do options work?', ['just overwhelmed', 'no']),
                  ],
      'types': ['QUICK_REPLY'],
     },
    {'name': 'my mediocrity',
     'response': [
         t('that sounds unpleasant'),
         opts('what would help you right now?', ['advice me', 'spill my guts', 'roast me, archy']),
         ],
      'types': ['QUICK_REPLY'],
     },
    
]

def make_payload(option):
    r = 'PICK/' + option.upper().replace(' ', '_').replace(',', '')
    unexpected = {l for l in r if l not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'}
    if unexpected:
        raise ValueError('Unexpected characters in option: %s' % option)
    return r


def make_callback(name):
    if name == 'START_PAYLOAD':
        return name
    return make_payload(name)


def make_function_name(callback):
    return 'callback_' + callback.lower()


def functions(page):
    fns = {}
    for node in data:
        fn = lambda payload, event: [item.do(page, payload, event) for item in node['response']]
        # tricky, decorator with arg and fn with arg.
        # See http://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#decorators-with-arguments
        callback = make_callback(node['name'])
        fnname = make_function_name(callback)
        print('Callback:', callback, 'fn name:', fnname)

        # fn = page.callback([callback])(fn)
        # Below code adapted from Page.callback decorator
        for _type in node['types']:
            if _type == 'QUICK_REPLY':
                page._quick_reply_callbacks[callback] = fn
            elif _type == 'POSTBACK':
                page._button_callbacks[callback] = fn
            else:
                raise ValueError('callback types must be "QUICK_REPLY" or "POSTBACK"')

        fns[fnname] = fn
    return fns


