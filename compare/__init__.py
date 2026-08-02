from __future__ import unicode_literals, division, absolute_import, print_function

__license__   = 'GPL v3'
__copyright__ = '2026, Generated'

from calibre.customize import InterfaceActionBase


class ActionCompare(InterfaceActionBase):
    name = 'BC-Diff'
    description = 'Compare selected book EPUB files in Beyond Compare'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'auto-generated'
    version = (0, 1, 0)
    minimum_calibre_version = (1, 0, 0)

    actual_plugin = 'calibre_plugins.compare.action:CompareAction'
