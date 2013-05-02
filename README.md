CompactList
===========

A small python library to compact lists of textual items containing numerical
sequences, into an abbreviated format, such as `foo.[0001-0100].jpg` or
`foo.[1-5,8-10].jpg`.

Subclass CompactList, overriding `pattern` with a regex that matches the
items in the list.  Override `_getNumber()` to return the numerical index
portion of the item's text, and override `_getGeneric()` to return the remainder
of the item's text, with `"{0}"` substituted for the index portion.

For example:

    $ python
    Python 2.6.5 (r265:79063, Apr 16 2010, 13:57:41)
    [GCC 4.4.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import os
    >>> import compactlist
    >>> class FileSequenceList(compactlist.CompactList):
    ...     pattern = re.compile(r'^(?P<name>\D+\.?)(?P<frame>\d+)(?P<ext>\.\w+)$')
    ...     def _getNumber(self, m):
    ...         return m['frame']
    ...     def _getGeneric(self, m):
    ...         return m['name']+'{0}'+m['ext']
    ...
    >>> f = FileSequenceList(os.listdir("tmp"))
    >>> for s in f.itercompact():
    ...   print s
    ...
    singleton.0001.exr
    otherseq.[0001-0100].exr
    foo.txt
    somefilesequence.[1-4,6,8-49,60-100].exr
