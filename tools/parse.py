import os
import re
from BeautifulSoup import BeautifulSoup as BS



def esc(txt):
    txt = txt.replace('&nbsp;', ' ').strip()
    txt = re.sub(r'[^a-zA-Z0-9_]', '_', txt)
    txt = re.sub(r'_+', '_', txt)
    txt = txt.strip('_')
    return txt


def parse():
    soup = BS(open('index').read())
    for item in soup.findAll('div', 'course-item-list-header'):
        section = esc(item.find('h3').next.next)
        ul = item.nextSibling

        print 'echo "downloading %s"' % section
        print 'mkdir -p %s' % section
        for lecture_link in ul.findAll('a', 'lecture-link'):
            links = lecture_link.parent.find('div', 'course-lecture-item-resource').findAll('a')
            script_link = links[-2]
            download_link = links[-1]

            title = esc(lecture_link.next)

            href = download_link['href'] 
            subfix = os.path.basename(href).split('?', 1)[0].split('.')[-1]
            fname = os.path.join(section, '%s.%s' % (title, subfix))

            shref = script_link['href']
            sfname = os.path.join(section, '%s.srt' % (title))

            print '''if [ ! -e "%s" ]; then
    wget --no-cookies --header "Cookie: $(cat cookies.txt)" '%s' -O '%s'
    wget --no-cookies --header "Cookie: $(cat cookies.txt)" '%s' -O '%s'
fi''' % (fname,
    href, fname,
    shref, sfname,
    )
            print

parse()
