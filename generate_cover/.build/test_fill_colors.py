"""Run with Python; launches calibre-debug with isolated temporary preferences."""
import os
import sys
import tempfile
from pathlib import Path
from types import ModuleType, SimpleNamespace
from copy import deepcopy

if '--in-calibre' not in sys.argv:
    import shutil
    import subprocess
    with tempfile.TemporaryDirectory(prefix='generate-cover-test-') as config_dir:
        env = dict(os.environ, CALIBRE_CONFIG_DIRECTORY=config_dir, QT_QPA_PLATFORM='offscreen')
        result = subprocess.run([shutil.which('calibre-debug'), '-e', __file__, '--', '--in-calibre'],
                                env=env, timeout=60)
    raise SystemExit(result.returncode)

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'common'))
import calibre_plugins
package = ModuleType('calibre_plugins.generate_cover')
package.__path__ = [str(root / 'generate_cover'), str(root / 'common')]
sys.modules[package.__name__] = package
import common_icons
common_icons.set_plugin_icon_resources('Generate Cover', {
    'images/' + p.name: p.read_bytes() for p in (root / 'generate_cover/images').iterdir() if p.is_file()
})
from calibre.gui2 import ensure_app
ensure_app()
from qt.core import QWidget, QIcon
import builtins
builtins.get_icons = lambda name, *args, **kwargs: QIcon(str(root / 'generate_cover/images' / name))
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.generate_cover import config as cfg, dialogs, draw

# Construct the real Qt dialog and exercise its actual load/save methods.
class Gui(QWidget):
    current_db = SimpleNamespace(new_api=None)

book = Metadata('Test title', ['Test author'])
book.series, book.series_index = 'Test series', 1
parent = SimpleNamespace(gui=Gui())
options = deepcopy(cfg.DEFAULT_CURRENT)
options[cfg.KEY_IMAGE_FILE] = ''
options[cfg.KEY_COLORS]['fill'] = '#123456'
cfg.plugin_prefs[cfg.STORE_CURRENT] = options
with tempfile.TemporaryDirectory() as images:
    dialog = dialogs.CoverOptionsDialog(parent, images, book, False)
    tab = dialog.fonts_tab
    assert tab.use_same_fill_color_checkbox.isChecked()
    for name, _ in dialogs.DIC_name_text_fill_color:
        assert getattr(tab, '_fillColor' + name).text() == '#123456'
    tab._fillColorTitle.setText('#abcdef')
    assert tab._fillColorAuthor.text() == '#abcdef'
    assert not tab._clearFillColorAuthor.isEnabled()
    tab.use_same_fill_color_checkbox.setChecked(False)
    assert tab._clearFillColorAuthor.isEnabled()
    tab._fillColorAuthor.setText('#ff0000')
    dialog.update_current_options()
    assert dialog.current[cfg.KEY_COLORS]['author_fill'] == '#ff0000'
    assert dialog.current[cfg.KEY_COLORS]['fill'] == '#abcdef'
    saved = deepcopy(dialog.current)
    dialog.current = deepcopy(options)
    dialog.apply_options_to_controls()
    dialog.current = saved
    dialog.apply_options_to_controls()
    assert tab._fillColorAuthor.text() == '#ff0000'
    # Profiles containing only the newer per-text keys must also load.
    del dialog.current[cfg.KEY_COLORS]['fill']
    dialog.apply_options_to_controls()
    assert tab._fillColorTitle.text() == '#abcdef'
    dialog._preview_timer.stop()
    dialog.close()
print('PASS: real dialog opens; legacy and per-text settings load/save; linked colors synchronize')

# Capture actual rendering colors while still generating real JPEG covers.
original = draw.create_colored_text_wand
seen = []
def capture(line, fill, *args):
    seen.append(fill)
    return original(line, fill, *args)
draw.create_colored_text_wand = capture
options = deepcopy(cfg.DEFAULT_CURRENT)
options[cfg.KEY_IMAGE_FILE] = ''
options[cfg.KEY_CUSTOM_TEXT] = 'Custom text'
options[cfg.KEY_FIELD_ORDER][-1]['display'] = True
colors = options[cfg.KEY_COLORS]
colors['fill'] = '#123456'
assert draw.generate_cover_for_book(book, options).startswith(b'\xff\xd8')
assert seen == ['#123456'] * 4, seen
seen.clear()
options[cfg.KEY_FILL_COLORS_LINKED] = False
fills = ['#ff0000', '#00ff00', '#0000ff', '#abcdef']
colors.update(zip(['title_fill', 'author_fill', 'series_fill', 'custom_fill'], fills))
del colors['fill']
assert draw.generate_cover_for_book(book, options).startswith(b'\xff\xd8')
assert seen == fills, seen
seen.clear()
options[cfg.KEY_FILL_COLORS_LINKED] = True
options[cfg.KEY_TEXT_BORDER] = True
assert draw.generate_cover_for_book(book, options).startswith(b'\xff\xd8')
assert seen == [fills[0]] * 4, seen
print('PASS: JPEG rendering uses legacy, independent, and linked colors above/below image, including borders')
