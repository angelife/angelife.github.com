#!/usr/bin/env python3
"""Write CI diagnostic page from Hugo list all output."""
import sys, os
os.chdir('/opt/data/angelife-clone/hugo-site')

# Get series list from hugo list all
import subprocess
HUGO = '/tmp/hugo'
result = subprocess.run([HUGO, 'list', 'all'], capture_output=True, text=True)
series_lines = [l for l in result.stdout.split('\n') if l and ',series,' in l]

series_data = '\n'.join(series_lines)
ij_count = len([l for l in series_lines if 'information-judgment' in l])

# Get HTML size
ij_html_size = '0'
ij_path = 'public/series/information-judgment/index.html'
if os.path.exists(ij_path):
    ij_html_size = str(os.path.getsize(ij_path))

html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CI Diagnostic</title></head>
<body>
<h1>CI Diagnostic Report</h1>
<p>Hugo: %(hugo)s</p>
<p>Commit: %(commit)s</p>
<p>Series total lines: %(total)d</p>
<p>Lines with information-judgment: %(ij)d</p>
<p>information-judgment/index.html size: %(size)s bytes</p>
<h2>All series list (grep ,series,):</h2>
<pre>%(data)s</pre>
</body></html>''' % {
    'hugo': subprocess.run([HUGO, 'version'], capture_output=True, text=True).stdout.strip(),
    'commit': subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
    'total': len(series_lines),
    'ij': ij_count,
    'size': ij_html_size,
    'data': series_data
}

open('public/_ci_diagnostic.html', 'w').write(html)
print('Diagnostic written:', len(html), 'bytes')
print('ij_count:', ij_count)
print('ij_html_size:', ij_html_size)
print('total_series_lines:', len(series_lines))