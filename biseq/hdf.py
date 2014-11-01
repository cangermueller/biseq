import h5py as h5


PATH_SEP = '/'

def split_filename(path, sep=':'):
    t = path.split(sep)
    filename = t[0]
    path = ''.join(t[1:])
    if len(path) == 0 or path[0] != PATH_SEP:
        path = PATH_SEP + path
    return (filename, path)

def ls(filename, path=None):
    f = h5.File(filename)
    if path is None or len(path) == 0:
        path = PATH_SEP
    items = list(f[path].keys())
    f.close()
    return items

