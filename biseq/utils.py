def split_hdf_path(path, sep='/'):
    t = path.split(sep)
    filename = t[0]
    path = sep + sep.join(t[1:])
    return (filename, path)
