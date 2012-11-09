#coding: utf8
import sys

def trans_bank(bank):
    if bank in (u'农业银行', u'建设银行', u'邮政储蓄', u'工商银行', u'招商银行', u'交通银行', ):
        return bank
    return u'其他银行'

DIST = [
    (u'华东', (u'山东', u'江苏', u'安徽', u'浙江', u'福建', u'上海')),
    (u'华南', (u'广东', u'广西', u'海南')),
    (u'华中', (u'湖北', u'湖南', u'河南', u'江西')),
    (u'华北', (u'北京', u'天津', u'河北', u'山西', u'内蒙古')),
    (u'西北', (u'宁夏', u'新疆', u'青海', u'陕西', u'甘肃')),
    (u'西南', (u'四川', u'云南', u'贵州', u'西藏', u'重庆')),
    (u'东北', (u'辽宁', u'吉林', u'黑龙江')),
]

def trans_prov(prov):
    for dist, plist in DIST:
        for p in plist:
            if prov.find(p) >= 0:
                return dist
    return u'未知'


def update_user(users, appid, amount, phone, _prov, _bank, _idnum):
    if 0:
        prov = _prov.strip()
        bank = _bank.strip()
    else:
        prov = trans_prov(_prov)
        bank = trans_bank(_bank)
    idnum = _idnum.strip()
    if len(idnum) == 18 and idnum[-2].isdigit():
        gender = 'F' if int(idnum[-2]) % 2 == 0 else 'M'
    else:
        gender = 'U'
    phone = phone.strip()

    if phone in users:
        attr = users[phone]
        if 'gender' not in attr or gender != 'U':
            attr['gender'] = gender
        if 'amount' not in attr or amount > attr['amount']:
            attr['amount'] = amount
    else:
        attr = users[phone] = {'gender': gender,
                               'amount': amount,
                               '_bank': _bank,
                               '_prov': _prov,
                               '_idnum': _idnum,
                               }

    attr['appid'] = appid
    attr['prov'] = prov
    attr['bank'] = bank


def amount_grade(amount):
    if amount <= 100:
        return 'L'
    if amount <= 200:
        return 'M'
    return 'H'


def trans_data():
    users = {}

    for line in sys.stdin:
        cols = line.split('\t')
        
        platform = cols[1]
        appid = cols[2]
        amount = int(cols[5])/100
        status = cols[6]
        phone = cols[7]
        prov = cols[8].decode('utf8')
        bank = cols[11].decode('utf8')
        idnum = cols[12]

        if appid in ('test', 'aaaa') or amount > 500 or status != '00' \
            or platform != 'dnapay':
            continue

        update_user(users, appid, amount, phone, prov, bank, idnum)

    print '\t'.join(['APPID',
                     'PROV',
                     'GENDER',
                     'BANK',
                     'AMOUNT',
                     ])
    for phone, user in users.iteritems():
        print '\t'.join([user['appid'],
                         user['prov'].encode('utf8'),
                         user['gender'],
                         user['bank'].encode('utf8'),
                         amount_grade(user['amount']),
#                         str(user['amount']),
#                         user['_prov'].encode('utf8'),
#                         user['_bank'].encode('utf8'),
#                         user['_idnum'],
                         ])


def main():
    trans_data()


main()
