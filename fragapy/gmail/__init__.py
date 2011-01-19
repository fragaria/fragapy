import chardet
from datetime import datetime
import email
from email.parser import HeaderParser
import imaplib
import re
import time
from StringIO import StringIO

from django.core.validators import email_re
from django.utils.encoding import smart_str

__all__ = ('Email', 'PyGmail')

ENC_DEFAULT = 'iso-8859-2'
ENC_GUESS_LIST = ['iso-8859-1', 'iso-8859-2', 'windows-1250', 'utf-8']

def _decode_token(elem):
    if elem[1]:
        return unicode(elem[0], elem[1])
    else:
        return unicode(elem[0])

class EmailMessage(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.parsed_data = HeaderParser().parsestr(self.raw_data[0][1])
    
    def _decode(self, parsed_data):
        return " ".join(map(_decode_token, email.header.decode_header(parsed_data)))
    
    def get_from(self):
        return self._decode(self.parsed_data['From'])
    
    def get_from_email(self):
        matches = re.search(r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}', self.get_from())
        if matches is not None:
            return matches.group(0)
        return None
    
    def get_to(self):
        return self._decode(self.parsed_data['To'])
    
    def get_subject(self):
        return self._decode(self.parsed_data['Subject'])
    
    def get_reply_to(self):
        return self._decode(self.parsed_data['Reply-To'])
    
    def get_received_on(self):
        return datetime.fromtimestamp(time.mktime(email.utils.parsedate(self.parsed_data['Received'].split("\n")[1].strip())))
    
    def get_content(self, content_type='plain'):
        mail = email.message_from_string(self.raw_data[0][1])
        payloads = []
 
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue
            # we are interested only in the given content_type
            if part.get_content_subtype() != content_type:
                continue
            
            
            payloads.append(part.get_payload(decode=True))
            
        content = " ".join(payloads)
            
        if self.parsed_data.get_content_charset() is not None:
            content = unicode(content, self.parsed_data.get_content_charset())
        else:
            enc = chardet.detect(content)['encoding']
            if not enc in ENC_GUESS_LIST:
                enc = ENC_DEFAULT
            content = unicode(content, enc)
            
        return content

class PyGmail(object):
    def __init__(self, host='imap.gmail.com', port=993):
        self.IMAP_SERVER = host
        self.IMAP_PORT = port
        self.M = None
        self.response = None
        self.mailboxes = None
        self.logged_in = False
        self.user = None
        
    def __del__(self):
        if self.logged_in:
            self.logout()

    def login(self, username, password):
        """
        Logs in to the gmail imap service using username and password
        """
        self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        rc, self.response = self.M.login(username, password)
        if rc == 'OK':
            self.logged_in = True
            self.user = username
        return rc

    def load_mailboxes(self):
        """
        Loads up list of mailboxes from the mail account 
        """
        self.mailboxes = []
        rc, self.response = self.M.list()
        for item in self.response:
            self.mailboxes.append(item.split()[-1])
        return rc
    
    def get_mailboxes(self):
        """
        Returns list of available mailboxes for the current account
        """
        if self.mailboxes is None:
            self.load_mailboxes()
        return self.mailboxes

    def get_mail_count(self, folder='INBOX'):
        """
        Returns total number of e-mail in the given folder
        """
        rc, self.response = self.M.select(folder)
        return self.response[0]

    def get_unread_count(self, folder='INBOX'):
        """
        Returns total number of unread messages in given folder
        """
        rc, self.response = self.M.status(folder, "(UNSEEN)")
        unreadCount = re.search("UNSEEN (\d+)", self.response[0]).group(1)
        return unreadCount

    def get_imap_quota(self):
        quotaStr = self.M.getquotaroot("INBOX")[1][1][0]
        r = re.compile('\d+').findall(quotaStr)
        if r == []:
            r.append(0)
            r.append(0)
        return float(r[1])/1024, float(r[0])/1024

    def _parse_mail_list(self, response):
        email_ids = [e_id for e_id in response[0].split()]
        return email_ids

    def get_all_mails(self, folder='INBOX'):
        """
        Returns list of all e-mail ids in given folder
        """
        status, count = self.M.select(folder)
        status, response = self.M.search(None, 'ALL')
        return self._parse_mail_list(response)

    def get_mails_from(self, uid, folder='INBOX'):
        """
        Returns list of e-mail ids in given folder whose sender is uid
        """
        status, count = self.M.select(folder)
        status, response = self.M.search(None, 'FROM', uid)
        return self._parse_mail_list(response)

    def get_mail_from_id(self, id):
        """
        Returns EmailMessage object for given e-mail id
        """
        status, response = self.M.fetch(id, '(RFC822)')
        return EmailMessage(response)
    
    def move_mail(self, id, destination_folder):
        """
        Moves mail of given id to the destination folder
        """
        if self.M.copy(id, destination_folder)[0] == 'OK':
            return self.M.store(id, '+FLAGS', r'(\Deleted)')[0] == 'OK'
        return False
    
    def move_mails(self, ids, destination_folder):
        """
        Moves all mails of given ids to the destination folder
        """
        unsucessfull = []
        for id in ids:
            if not self.move_mail(id, destination_folder):
                unsucessfull.append(id)
        self.M.expunge()
        return unsucessfull

    def rename_mailbox(self, oldmailbox, newmailbox):
        """
        Renames `oldmailbox` mailbox to new name 
        """
        rc, self.response = self.M.rename(oldmailbox, newmailbox)
        return rc

    def create_mailbox(self, mailbox):
        """
        Creates new mailbox with name `mailbox`
        """
        rc, self.response = self.M.create(mailbox)
        return rc

    def delete_mailbox(self, mailbox):
        """
        Deletes mailbox named `mailbox`
        """
        rc, self.response = self.M.delete(mailbox)
        return rc

    def logout(self):
        """
        Logs out of gmail account
        """
        if self.logged_in:
            self.M.logout()