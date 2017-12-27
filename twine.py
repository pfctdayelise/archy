import os
from bs4 import BeautifulSoup


class Response:
    def do(self, page, payload, event):
        pass


class t(Response):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return 't(%s)' % self.text

    def do(self, page, payload, event):
        recipient = event.sender_id
        page.send(recipient, self.text)


class opts(Response):
    def __init__(self, q, options):
        self.q = q
        self.options = options

    def __str__(self):
        return 'opts(%s)' % self.q

    def do(self, page, payload, event):
        recipient = event.sender_id
        qrs = [{'title': o, 'payload': make_payload(o)} for o in self.options]
        print('QRs:', qrs)
        page.send(recipient,
                  self.q,
                  quick_replies=qrs,
                  metadata='DEVELOPER_DEFINED_METADATA')


def make_payload(option):
    r = 'PICK/' + option.upper().replace(' ', '_').replace(',', '').replace('-', '').replace('?', '').replace("'", '')
    unexpected = {l for l in r if l not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/_'}
    if unexpected:
        raise ValueError('Unexpected characters in option: %s -> %s' % (option, r))
    return r


# data = [
#      {'name': 'procrastination',
#      'response': [
#          opts('apart from a white noise machine or a new brain what do you think would help you?', ['soothe me please', 'make me write']),
#      ],
#      },
#     {'name': 'just overwhelmed',
#      'response': [t('...tbc')],
#      },
#     {'name': 'so distracted',
#      'response': [t('i am not very good at staying focused'),
#                   t('i can tell u that everyone has a dirty floor so if you think you should clean it instead, dont bother'),
#                   t('...tbc'),
#                   ],
#      },
#     {'name': 'my mediocrity',
#      'response': [
#          t('that sounds unpleasant'),
#          opts('what would help you right now?', ['advice me', 'spill my guts', 'roast me, archy']),
#          ],
#      },
    
# ]


def parse_twine():
    homedir = os.path.expanduser(os.getenv('ARCHY_HOME', '~/workspace/archy'))
    print(homedir)
    filename = os.getenv('ARCHY_FILENAME', 'ArchyBot v4.0.1.html')
    f = os.path.join(homedir, filename)
    print(f)
    with open(f) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    passages = soup.find_all('tw-passagedata')
    data = [make_dict(passage) for passage in passages]
    return data


def make_dict(passage):
    try:
        name = passage['name']
        response = parse_response(passage.text)
    except:
        print(passage)
        return None
    return dict(name=name, response=response)


def parse_response(text):
    """
    Assume all options come at the end.

    Example:
    'that sounds unpleasant\nwhat would help you right now?\n[[advice me]]\n[[spill my guts]]\n[[roast me, archy]]'

    ->

    [
     t('that sounds unpleasant'),
     opts('what would help you right now?', ['advice me',
                                             'spill my guts',
                                             'roast me, archy',
                                            ]),
    ]
    """

    lines = text.split('\n')

    def is_option(line):
        return line.startswith('[[')

    def parse_option(line):
        return line.strip('[] ')

    responses = []
    options = []
    for line in reversed(lines):
        if is_option(line):
            options.append(parse_option(line))
        elif options:
            responses.append(opts(line, reversed(options)))
            options = False
        else:
            responses.append(t(line))
    return reversed(responses)


def test():
    for item in parse_twine():
        for t in item['response']:
            if isinstance(t, opts):
                for o in t.options:
                    try:
                        make_payload(o)
                    except:
                        print(item['name'])
                        print(t)
                        print(o)
                        raise
    print("all parsed successfully")
