import os
import glob

'''
<!--
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'Lecture_4_2_Objects_Everywhere_19_07.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    creation_time   : 1970-01-01 00:00:00
    encoder         : Lavf53.29.100
  Duration: 00:19:46.53, start: 0.000000, bitrate: 244 kb/s
    Stream #0.0(und): Video: h264 (High), yuv420p, 960x540 [PAR 1:1 DAR 16:9], 108 kb/s, 30 fps, 30 tbr, 30 tbn, 60 tbc
    Metadata:
      creation_time   : 1970-01-01 00:00:00
    Stream #0.1(und): Audio: aac, 44100 Hz, stereo, s16, 127 kb/s
    Metadata:
      creation_time   : 1970-01-01 00:00:00

219
00:18:59,247 --> 00:19:05,271
could also implement and further the
integers so including negative numbers and

220
00:19:05,271 --> 00:19:07,380
even floating point numbers.

-->
<video src="Lecture_4_2_Objects_Everywhere_19_07.mp4" controls>
  <track kind="subtitles" label="English subtitles" src="Lecture_4_2_Objects_Everywhere_19_07.vtt" srclang="en" default></track>
</video>
'''

def convert_srt_to_vtt(srt, vtt):
    '''Convert subtitle file from srt format to vtt(WEBVTT) format
    The process is little more than a find-and-replace:
    * Start the text file with WEBVTT
    * Remove the cue markers at the start of each subtitle, or replace them with Cue - prefixes.
    * Optionally, remove the 00: hour marker at the start of each timestamp.
    * Convert the comma before the millisecond mark in every timestamp to a decimal point (easy enough with a find-replace: ,7 to .7, for example).
    * Optionally, add styling markup to the subtitle text.
    * Save the file with a .vtt extension and link to it from a <track> element in an HTML5 page.
    '''
    #FIXME: still have problem with this vtt format, chrome don't use it
    def time_strip(tstring):
        tstring = tstring.strip()
        if tstring.startswith('00:'):
            return tstring[3:]
        return tstring

    def transform(lines):
        yield 'WEBVTT'
        st = 0
        for line in lines:
            line = line.rstrip()
            if not line:
                st = 0
                yield ''
            elif st == 0:
                st = 'cue'
                # just ignore
            elif st == 'cue':
                st = 'time'
                from_, to_ = line.split('-->')
                yield '%s --> %s' % (time_strip(from_), time_strip(to_))
            elif st == 'time':
                st = 'text'
                yield line
            else: # text
                yield line

    with open(srt) as inputfile:
        lines = inputfile.readlines()

    content = '\n'.join(transform(lines))

    with open(vtt, 'w') as outputfile:
        outputfile.write(content)


def make_html():
    '''Search mp4 files in current dir, make each of them a video html tag
    along with its subtitle
    '''
    yield '<script src="http://code.jquery.com/jquery.min.js"></script>'
    yield '''<style>
</style>
<script>
$(function() {
    $('.vlink').click(function() {
        $('video', this).show();
    });
});
</script>
<ul>
'''

    for mp4 in glob.glob('*.mp4'):
        name, _ext = os.path.splitext(mp4)
        srt = '%s.srt' % name
        vtt = '%s.vtt' % name
        convert_srt_to_vtt(srt, vtt)

        yield '''<li>
<a href='#' class='vlink'>
    %(mp4)s (Duration)
    <video src="%(mp4)s" controls style='display:none'>
        <track kind="subtitles" label="English" src="%(vtt)s" srclang="en" default></track>
    </video>
</a></li>
''' % {'mp4': mp4, 'vtt': vtt}
    yield '</ul>'


if __name__ == '__main__':
    print '\n'.join(make_html())
