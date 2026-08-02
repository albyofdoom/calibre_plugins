from __future__ import unicode_literals, division, absolute_import, print_function

__license__   = 'GPL v3'
__copyright__ = '2026, Generated'

import subprocess

try:
    load_translations()
except NameError:
    pass

from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import sanitize_env_vars, warning_dialog
from calibre.constants import iswindows


class CompareAction(InterfaceAction):

    name = 'BC-Diff'
    action_spec = (_('BC-Diff'), None,
                   _('Compare selected book EPUB files in Beyond Compare'), 'Ctrl+Alt+B')
    action_type = 'current'

    def genesis(self):
        self.is_library_selected = False
        print('CompareAction: genesis called')
        self.qaction.triggered.connect(self.compare_selected)
        try:
            # Ensure keyboard shortcuts are finalized so Calibre recognises them
            self.gui.keyboard.finalize()
        except Exception:
            pass

    def location_selected(self, loc):
        self.is_library_selected = loc == 'library'
        print('CompareAction: location_selected ->', loc, 'is_library_selected=', self.is_library_selected)
        self.qaction.setEnabled(self.is_library_selected)

    def compare_selected(self):
        print('CompareAction: compare_selected called')
        if not self.is_library_selected:
            return
        rows = self.gui.library_view.selectionModel().selectedRows()
        ids = [self.gui.library_view.model().id(r) for r in rows]
        if not ids:
            return

        # If 4 or more selected, take no action
        if len(ids) >= 4:
            return

        db = self.gui.current_db
        epub_paths = []
        for book_id in ids:
            try:
                p = db.format_abspath(book_id, 'EPUB', index_is_id=True)
            except Exception:
                p = None
            epub_paths.append(p)

        print('CompareAction: epub_paths =', epub_paths)

        # For 2 or 3 selected, require all have EPUBs
        if len(ids) in (2, 3):
            if any(p is None for p in epub_paths):
                missing = [self.gui.current_db.title(book_id, index_is_id=True)
                           for book_id, p in zip(ids, epub_paths) if p is None]
                warning_dialog(self.gui, _('Missing EPUB'),
                               _('The following selected books have no EPUB format:'),
                               det_msg='\n'.join(missing), show=True)
                return
        # For single selected, require EPUB
        if len(ids) == 1 and epub_paths[0] is None:
            warning_dialog(self.gui, _('Missing EPUB'),
                           _('The selected book has no EPUB format.'), show=True)
            return

        # Build command for Beyond Compare
        if iswindows:
            app = 'C:\\Program Files\\Beyond Compare 5\\BCompare.exe'
        else:
            app = 'bcompare'

        args = [app] + [p for p in epub_paths if p]
        print('CompareAction: app =', app)
        print('CompareAction: args =', args)
        if len(args) <= 1:
            print('CompareAction: nothing to compare (not enough files)')
            return

        # Launch detached process so Calibre isn't blocked
        DETACHED_PROCESS = 0x00000008
        with sanitize_env_vars():
            try:
                kwargs = {'creationflags': DETACHED_PROCESS} if iswindows else {}
                print('CompareAction: launching subprocess with kwargs=', kwargs)
                subprocess.Popen(args, **kwargs)
            except Exception as e:
                print('CompareAction: failed to launch Beyond Compare:', repr(e))
                try:
                    warning_dialog(self.gui, _('Compare Failed'),
                                   _('Failed to launch Beyond Compare.'),
                                   det_msg=str(e), show=True)
                except Exception:
                    pass
                return
