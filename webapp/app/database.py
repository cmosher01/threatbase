import glob
import os
import itertools




def _format_show_id_to_date(showid):
    yy = showid[0:2]
    mm = showid[2:4]
    dd = showid[4:]
    if not dd.isdigit():
        dd = '??'
    return '19{yy}-{mm}-{dd}'.format(yy=yy, mm=mm, dd=dd)

def _build_dbpath(root_path, showid):
    yy = showid[0:2]
    mm = showid[2:4]
    dx = showid[4:]
    return '{root_path}/database/shows/{yy}/{mm}/{dx}/{showid}'.format(root_path=root_path, yy=yy, mm=mm, dx=dx, showid=showid)

def _dbname(dbpath, dbtype):
    return '{dbpath}{dbtype}.txt'.format(dbpath=dbpath, dbtype=dbtype)





def _read_db(showid, dbtype):
    s = ''
    try:
        with open(_dbname(showid, dbtype)) as f:
            s = f.read()
    finally:
        return s.strip()



def _read_lines_as_csv(showid, dbtype):
    csv = u''
    try:
        with open(_dbname(showid, dbtype)) as f:
            s = f.readline()
            while s:
                if len(csv) > 0:
                    csv += u', '
                csv += unicode(s.strip(), 'utf-8')
                s = f.readline()
    finally:
        return csv



def _read_title(showid):
    showdate = _read_db(showid, 'dt')
    if not showdate:
        showdate = _format_show_id_to_date(showid[-6:])

    with open(_dbname(showid, 'sh')) as f:
        band = f.readline().strip()
        venue = f.readline().strip()

    if not venue:
        venue = '[unknown venue]'

    return '{band} (live, {date}: {venue})'.format(band=band, date=showdate, venue=venue)



def _read_venue(showid):
    with open(_dbname(showid, 'sh')) as f:
        band = f.readline().strip()
        venue = f.readline().strip()

    return venue



def _read_au(showid):
    audio = {}
    try:
        with open(_dbname(showid, 'au')) as f:
            audio['orig_file'] = f.readline().strip()
            audio['orig_log'] = f.readline().strip()
    finally:
        return audio



def _read_ch(showid):
    chs = []
    try:
        with open(_dbname(showid, 'ch')) as f:
            for date, desc in itertools.zip_longest(*[f]*2):
                chs.append({'date': date.strip(), 'desc': desc.strip()})
    finally:
        return chs



def _read_ed(showid):
    eds = []
    try:
        with open(_dbname(showid, 'ed')) as f:
            for time, prob, edit in itertools.zip_longest(*[f]*3):
                eds.append({'time': time.strip(), 'prob': prob.strip(), 'edit': edit.strip()})
    finally:
        return eds



def _read_tr(showid):
    tracks = []
    try:
        with open(_dbname(showid, 'tr')) as f:
            s = f.readline()
            while s:
                td_class = s.strip()
                song_or_quote = ""
                s = f.readline()
                while s.strip() != '.':
                    if len(song_or_quote) > 0:
                        song_or_quote += '\n'
                    song_or_quote += s.strip()
                    s = f.readline()
                track = {}
                track['song_or_quote'] = song_or_quote
                track['td_class'] = td_class
                track['offset'] = '[coming soon]'
                tracks.append(track)
                s = f.readline()
    finally:
        return tracks

def _read_tr_brief(showid):
    tracks = ''
    try:
        with open(_dbname(showid, 'tr')) as f:
            s = f.readline()
            while s:
                td_class = s.strip()
                if td_class == 'song':
                    song = ''
                    s = f.readline()
                    while s.strip() != '.':
                        if len(song) > 0:
                            song += '\n'
                        song += s.strip()
                        s = f.readline()
                    if len(tracks) > 0:
                        tracks += ', '
                    tracks += song
                s = f.readline()
    finally:
        return tracks

def _read_show_ids(root_path, bandid):
    shows = {}
    path = '{root_path}/database/bands/{bandid}'.format(root_path=root_path, bandid=bandid)
    with open(path) as f:
        shows['band'] = f.readline().strip()
        showlist = []
        s = f.readline()
        while s:
            showlist.append({'id': s.strip()})
            s = f.readline()
    shows['list'] = showlist
    return shows

def _fill_in_show_details_for_list(root_path, shows):
    for show in shows['list']:
        dbpath = _build_dbpath(root_path, show['id'])
        show['show_date'] = _read_db(dbpath, 'dt')
        if not show['show_date']:
            show['show_date'] = _format_show_id_to_date(show['id'])
        show['venue'] = _read_venue(dbpath)
        show['setlist'] = _read_tr_brief(dbpath)
        show['other_bands'] = _read_lines_as_csv(dbpath, 'ob')
        show['recorded'] = _read_db(dbpath, 'av')

def _find_images(root_path, showid):
    images = []
    yy = showid[0:2]
    mm = showid[2:4]
    dd = showid[4:6]
    pat = '{root_path}/../static/shows/flyers/19{yy}-{mm}-{dd}*'.format(root_path=root_path, yy=yy, mm=mm, dd=dd)
    for file in glob.glob(pat):
        images.append('/threatbase/shows/flyers/'+os.path.basename(file))
    return images





def read_show(root_path, showid):
    dbpath = _build_dbpath(root_path, showid)
    return {
        'title' : _read_title(dbpath),
        'audio' : _read_au(dbpath),
        'info'  : _read_db(dbpath, 'in'),
        'ident' : _read_db(dbpath, 'id'),
        'images': _find_images(root_path, showid),
        'chain' : _read_ch(dbpath),
        'tracks': _read_tr(dbpath),
        'edits' : _read_ed(dbpath)
    }



def read_shows(root_path, bandid):
    shows = _read_show_ids(root_path, bandid)
    _fill_in_show_details_for_list(root_path, shows)
    return shows
