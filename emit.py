import codecs
import sys


def _emit(text):
    """Print a line, replacing characters the console encoding cannot represent.

    Windows consoles and pipes default to cp1252, where the turtle's emoji raise
    UnicodeEncodeError instead of printing.
    """
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        text.encode(encoding)
    except (LookupError, UnicodeEncodeError):
        try:
            encoding = codecs.lookup(encoding).name
        except LookupError:
            encoding = "utf-8"
        text = text.encode(encoding, "replace").decode(encoding, "replace")
    print(text)
