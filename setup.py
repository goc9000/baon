from distutils.core import setup

setup(
    name='baon',
    version='3.0.0',
    packages=['', 'baon', 'baon.ui', 'baon.ui.qt_gui', 'baon.ui.qt_gui.forms', 'baon.ui.qt_gui.utils',
          'baon.ui.qt_gui.utils.__tests__', 'baon.ui.qt_gui.mixins', 'baon.ui.qt_gui.widgets',
          'baon.ui.qt_gui.widgets.files_display', 'baon.lib', 'baon.lib.action_functions',
          'baon.lib.simple_text_functions', 'baon.lib.simple_text_functions.__tests__', 'baon.core',
          'baon.core.ast', 'baon.core.ast.rules', 'baon.core.ast.rules.__tests__', 'baon.core.ast.actions',
          'baon.core.ast.actions.__tests__', 'baon.core.ast.matches', 'baon.core.ast.matches.control',
          'baon.core.ast.matches.control.__tests__', 'baon.core.ast.matches.pattern',
          'baon.core.ast.matches.pattern.__tests__', 'baon.core.ast.matches.special',
          'baon.core.ast.matches.special.__tests__', 'baon.core.ast.matches.__tests__',
          'baon.core.ast.matches.insertion', 'baon.core.ast.matches.insertion.__tests__',
          'baon.core.ast.matches.positional', 'baon.core.ast.matches.positional.__tests__',
          'baon.core.ast.__errors__', 'baon.core.plan', 'baon.core.plan.actions',
          'baon.core.plan.actions.__tests__', 'baon.core.plan.actions.__errors__', 'baon.core.plan.__tests__',
          'baon.core.plan.__errors__', 'baon.core.files', 'baon.core.files.__tests__', 'baon.core.files.__errors__',
          'baon.core.rules', 'baon.core.rules.__tests__', 'baon.core.utils', 'baon.core.utils.progress',
          'baon.core.utils.__tests__', 'baon.core.errors', 'baon.core.parsing', 'baon.core.parsing.__tests__',
          'baon.core.parsing.__errors__', 'baon.core.renaming', 'baon.core.renaming.__tests__',
          'baon.core.renaming.__errors__', 'baon.core.__tests__'],
    package_dir={'': 'src'},
    url='https://github.com/goc9000/baon',
    license='GPL-3',
    author='Cristian Dinu',
    author_email='goc9000@gmail.com',
    description='Mass file renamer with ANTLR-like syntax'
)
