import hashlib
import io

def md5sum_whole(src):
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        content = fd.read()
        md5.update(content)
    return md5

def md5sum_chunks(src, length=io.DEFAULT_BUFFER_SIZE):
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        for chunk in iter(lambda: fd.read(length), b''):
            md5.update(chunk)
    return md5

def md5sum_full(src):
    md5 = hashlib.md5()
    m = hashlib.md5()
    with open( src , "rb" ) as f:
        while True:
            buf = f.read(8192)
            if not buf:
                break
            m.update( buf )
    return m
    

def md5sum_progress(src, callback, length=io.DEFAULT_BUFFER_SIZE):
    calculated = 0
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        for chunk in iter(lambda: fd.read(length), b''):
            md5.update(chunk)
            calculated += len(chunk)
            callback(calculated)
    return md5

