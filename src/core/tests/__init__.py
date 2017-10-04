import requests
import gzip
from io import BytesIO


def validate_html(html, content_type):
    # 'node_modules/vnu-jar/build/dist/vnu.jar'
    vnu_url = 'http://vnu:8888'
    with BytesIO() as buf:
        with gzip.GzipFile(fileobj=buf, mode='wb') as gzipper:
            gzipper.write(html)
        gzippeddata = buf.getvalue()

    r = requests.post(
        vnu_url,
        params={
            'out': 'gnu',
            'level': 'error',
        },
        headers={
            'Content-Type': content_type,
            'Accept-Encoding': 'gzip',
            'Content-Encoding': 'gzip',
            'Content-Length': str(len(gzippeddata)),
        },
        data=gzippeddata
    )
    return r.text.strip()

def validate_process(res, html):
    # t = validate_html(html, ct)
    if res == '':
        return

    print(t)
    print('- - - - -')
    res = ''
    errors = res.split('\n')
    for e in errors:
        error_string = e.strip(':')
        rng, cls = error_string.split(':')[0:2]
        msg = error_string[len(rng+cls)+2:].strip()
        # for skip in skips:
        #     if skip in msg:
        #         continue
        print(rng, msg)
        linePos1, linePos2 = rng.split('-')
        line1, pos1 = map(int, linePos1.split('.'))
        line2, pos2 = map(int, linePos2.split('.'))
        # for line in itertools.islice(r.content.split('\n'), line1, line2):
        res += error_string
        for line in html.splitlines()[max(0, line1-1):line2]:
            # res += line + '\n'
            print(line)
        print('')
