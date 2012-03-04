import sys
import poplib
import getpass
import cPickle

def fetch_mail_to(fname):
    client = poplib.POP3_SSL('pop.gmail.com')
    client.user('hao2dw')
    client.pass_(getpass.getpass())

    mails = []
    cnt = len(client.list()[1])
    print 'total:', cnt

    for i in range(cnt):
        try:
            msg = client.retr(i+1)
        except:
            continue
        if i % 10 == 0:
            print 'fetching ...', i+1
        mails.append(msg)

    with open(fname, 'wb') as f:
        cPickle.dump(mails, f)


if __name__ == '__main__':
    fetch_mail_to(sys.argv[1])
