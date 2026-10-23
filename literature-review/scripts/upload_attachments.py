"""Upload PDFs to existing Zotero items as child attachments.

Usage: upload_attachments.py MANIFEST
MANIFEST has one line per file: ``<item key> <path to pdf>``.

zotero_add_from_file doesn't upload files: pyzotero's attachment helpers
send the full path as the filename, the Zotero API rejects it ("cannot
contain a directory path"), and the error is swallowed. This passes the
bare filename with the file's folder as the base directory instead.

Reads ZOTERO_LIBRARY_ID and ZOTERO_API_KEY from the environment.
"""
import os
import sys
from pathlib import Path

from pyzotero import zotero
from pyzotero._upload import Zupload

z = zotero.Zotero(os.environ["ZOTERO_LIBRARY_ID"], "user", os.environ["ZOTERO_API_KEY"])
for line in open(sys.argv[1]):
    if not line.strip():
        continue
    key, path = line.split(maxsplit=1)
    p = Path(path.strip()).resolve()
    t = z.item_template("attachment", "imported_file")
    t.update(title=p.name, filename=p.name, contentType="application/pdf")
    res = Zupload(z, [t], parentid=key, basedir=p.parent).upload()
    # "unchanged": Zotero already stores an identical file and links to it
    status = "ok" if res["success"] else "unchanged" if res["unchanged"] else "FAILED"
    print(f"{key} {p.name}: {status}")
