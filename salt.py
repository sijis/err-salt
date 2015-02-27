from errbot import BotPlugin, botcmd
from optparse import OptionParser

import json
import shlex
import logging
import requests

log = logging.getLogger(name='errbot.plugins.Salt')

try:
    import pepper
except ImportError:
    log.error("Please install 'salt-pepper' python package")


class Salt(BotPlugin):
    """Plugin to run salt commands on hosts"""

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'paste_api_url': None,
            'api_url': None,
            'api_user': None,
            'api_pass': None,
            'api_auth': None,
        }
        return config

    def pastebin(self, data):
        ''' Post the output to pastebin '''
        clean_data = data
        url = requests.post(
            self.config['paste_api_url'],
            data={
                'content': clean_data,
            },
        )
        log.debug('url: {}'.format(url))
        return url.text.strip('"')

    @botcmd
    def salt(self, msg, args):
        ''' executes a salt command on systems
            example:
            !salt log*.local cmd.run 'cat /etc/hosts'
            !salt log*.local test.ping
        '''
        parser = OptionParser()
        (options, args) = parser.parse_args(shlex.split(args))

        if len(args) < 2:
            response = '2 parameters required. see !help salt'
            self.send(msg.frm,
                      response,
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return

        targets = args.pop(0)
        action = args.pop(0)

        api = pepper.Pepper(self.config['api_url'], debug_http=False)
        auth = api.login(self.config['api_user'],
                         self.config['api_pass'],
                         self.config['api_auth'])
        ret = api.local(targets,
                        action,
                        arg=args,
                        kwarg=None,
                        expr_form='pcre')
        results = json.dumps(ret, sort_keys=True, indent=4)
        self.send(msg.frm,
                  self.pastebin(results),
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)
