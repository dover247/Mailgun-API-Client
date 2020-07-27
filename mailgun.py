import smtplib
import requests
import pandas
import argparse
import sys
import time
import datetime
import logging


class MailGun(object):

    def __init__(self):
        
        self.log_levels = {
            1: logging.INFO,
            2: logging.WARNING,
            3: logging.CRITICAL,
            4: logging.DEBUG,
        }
        self.auth = (
            "api", "")
        parser = argparse.ArgumentParser(
            usage='''mailgun <command> [<args>]

            trace           trace message
            send            send message
            domains         retrieves domains      
            ips             retrieves all ips
            stats           retrieves stats
                ''')
        parser.add_argument('command', help='subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            logging.error('Unrecognized Command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def send(self):
        parser = argparse.ArgumentParser(
            description="send message through mailgun's api")
        parser.add_argument('recipient')
        parser.add_argument('subject')
        parser.add_argument('text')
        args = parser.parse_args(sys.argv[2:])

        return requests.post("https://api.mailgun.net/v3/sandboxefe28b049cc04700a3fae12ca1067289.mailgun.org/messages",
                             auth=self.auth,
                             data={"from": "Test <user@sandboxefe28b049cc04700a3fae12ca1067289.mailgun.org>",
                                   "to": [args.recipient],
                                   "subject": args.subject,
                                   "text": args.text})
    def trace(self):
        parser = argparse.ArgumentParser(
            description='trace a message via mailgun api')
        parser.add_argument('recipient')
        parser.add_argument('--limit')
        parser.add_argument('--subject')
        parser.add_argument('--messageid')
        parser.add_argument(
            '--event', choices=['rejected', 'accepted', 'delivered', 'failed', 'complained'])
        args = parser.parse_args(sys.argv[2:])
        logs = requests.get("https://api.mailgun.net/v3/sandboxefe28b049cc04700a3fae12ca1067289.mailgun.org/events",
                           auth=self.auth,
                           params={
                               "ascending": "yes",
                               "limit":  args.limit,
                               "pretty": "yes",
                               "recipient": args.recipient,
                               "subject": args.subject,
                               "message-id": args.messageid,
                               "event": args.event}).text
        logging.info(logs)

   # def domains(self):
    #    parser = argparse.ArgumentParser(description='') def domains(self): 
        #req = requests.get(
         #   'https://api.mailgun.net/v3/domains', auth=self.auth)
        #domains = req.text
        #logging.info(domains)

    def ips(self):
        req = requests.get('https://api.mailgun.net/v3/ips', auth=self.auth)
        ips = req.text
        logging.info(ips)

    def stats(self):
        req = requests.get('https://api.mailgun.net/v3/sandboxefe28b049cc04700a3fae12ca1067289.mailgun.org/stats/total',
                           auth=self.auth,
                           params={"event": ["accepted", "delivered", "failed"], "duration": "1d"})
        stats = req.text
        logging.info(stats)

    def show(self):
        parser = argparse.ArgumentParser(description='retrives data')
        parser.add_argument('-v', action='count', default=1, help='verbosity level')
        subparser = parser.add_subparsers()
        # domains command
        domains = subparser.add_parser('domains')
        domains.add_argument('name')
        # stats command
        stats = subparser.add_parser('stats')
        # ips command
        ips = subparser.add_parser('ips')



        args = parser.parse_args(sys.argv[2:])

        logging.basicConfig(level=self.log_levels[args.v], format='%(asctime)s %(levelname)s: %(message)s')
        


if __name__ == '__main__':
    MailGun()

