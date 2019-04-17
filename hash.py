import hashlib
import io

class md5sum:
    def whole(src):
        md5 = hashlib.md5()
        with io.open(src, mode="rb") as fd:
            content = fd.read()
            md5.update(content)
        return md5

    def chunks(src, length=io.DEFAULT_BUFFER_SIZE):
        md5 = hashlib.md5()
        with io.open(src, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(length), b''):
                md5.update(chunk)
        return md5

    def progress(src, callback, length=io.DEFAULT_BUFFER_SIZE):
        calculated = 0
        md5 = hashlib.md5()
        with io.open(src, mode="rb") as fd:
            for chunk in iter(lambda: fd.read(length), b''):
                md5.update(chunk)
                calculated += len(chunk)
                callback(calculated)
        return md5
