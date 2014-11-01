def split_hdf_path(path, sep=':'):
    t = path.split(sep)
    filename = t[0]
    path = ''.join(t[1:])
    if len(path) == 0 or path[0] != '/':
        path = '/' + path
    return (filename, path)
