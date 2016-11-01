import itertools





def _build_dbpath(root_path, showid):
    return '{root_path}/database/19{showid}/{showid}'.format(root_path=root_path, showid=showid)

def _dbname(dbpath, dbtype):
    return '{dbpath}{dbtype}.txt'.format(dbpath=dbpath, dbtype=dbtype)





def _read_db(showid, dbtype):
    s = ''
    try:
        with open(_dbname(showid, dbtype)) as f:
            s = f.read()
    finally:
        return s



def _read_sh(showid):
    d6 = showid[-6:]
    showdate = '19{year}-{month}-{day}'.format(year=d6[0:2], month=d6[2:4], day=d6[4:6])

    with open(_dbname(showid, 'sh')) as f:
        band = f.readline().strip()
        venue = f.readline().strip()

    title = showdate+' '+band
    if (venue):
        title = title+' @ '+venue

    return title



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
    with open(_dbname(showid, 'ch')) as f:
        for date, desc in itertools.izip_longest(*[f]*2):
            chs.append({'date': date, 'desc': desc})
    return chs



def _read_ed(showid):
    eds = []
    try:
        with open(_dbname(showid, 'ed')) as f:
            for time, prob, edit in itertools.izip_longest(*[f]*3):
                eds.append({'time': time, 'prob': prob, 'edit': edit})
    finally:
        return eds



def _read_tr(showid):
    tracks = []
    with open(_dbname(showid, 'tr')) as f:
        s = f.readline()
        while s:
            td_class = s
            song_or_quote = ""
            s = f.readline()
            while s.strip() != '.':
                song_or_quote += s
                s = f.readline()
            track = {}
            track['song_or_quote'] = song_or_quote
            track['td_class'] = td_class
            track['offset'] = '[coming soon]'
            tracks.append(track)
            s = f.readline()
    return tracks





def read_show(root_path, showid):
    dbpath = _build_dbpath(root_path, showid)
    return {
        'title' : _read_sh(dbpath),
        'audio' : _read_au(dbpath),
        'info'  : _read_db(dbpath, 'in'),
        'ident' : _read_db(dbpath, 'id'),
        'chain' : _read_ch(dbpath),
        'tracks': _read_tr(dbpath),
        'edits' : _read_ed(dbpath)
    }
