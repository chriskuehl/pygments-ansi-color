pygments-ansi-color
--------

[![Build Status](https://travis-ci.org/chriskuehl/pygments-ansi-color.svg?branch=master)](https://travis-ci.org/chriskuehl/pygments-ansi-color)
[![Coverage Status](https://coveralls.io/repos/github/chriskuehl/pygments-ansi-color/badge.svg?branch=master)](https://coveralls.io/github/chriskuehl/pygments-ansi-color?branch=master)
[![PyPI version](https://badge.fury.io/py/pygments-ansi-color.svg)](https://pypi.python.org/pypi/pygments-ansi-color)

An ANSI color-code highlighting lexer for Pygments.

![](https://i.fluffy.cc/nHPkL3gfBtj5Kt4H3RR51T9TJLh6rtv2.png)


### Usage

1. `pip install pygments-ansi-color`

2. Configure your Pygments style with the appropriate color tokens. It's
   necessary to add additional tokens because existing Pygments lexers are
   built around contextual tokens (think "Comment" or "String") rather than
   actual colors.

   In the case of ANSI escape sequences, colors have no context beyond the
   color themselves; we'd always want a "red" rendered as "red", regardless of
   your particular theme.

   Here's an example:

   ```python
   from pygments_ansi_color import color_tokens

   # Note: You can use different background colors for improved readability.
   fg_colors = bg_colors = {
       'Black': '#000000',
       'Red': '#EF2929',
       'Green': '#8AE234',
       'Yellow': '#FCE94F',
       'Blue': '#3465A4',
       'Magenta': '#c509c5',
       'Cyan': '#34E2E2',
       'White': '#ffffff',
   }
   class MyStyle(pygments.styles.xcode.XcodeStyle):
       styles = dict(pygments.styles.xcode.XcodeStyle.styles)
       styles.update(color_tokens(fg_colors, bg_colors))
   ```

3. Render your code!

   ```python
   import pygments
   import pygments.formatter
   import pygments.lexers

   lexer = pygments.lexers.get_lexer_by_name('ansi-color')
   formatter = pygments.formatter.HtmlFormatter(style=MyStyle)
   print(pygments.highlight('your text', lexer, formatter))
   ```


### Example

You can see an example [on fluffy][fluffy-example], the project that this lexer
was originally developed for.

The colors are defined as part of your Pygments style and can be changed.


[fluffy-example]: https://i.fluffy.cc/zr9RVt0gcrVtKH06hkqRCJPP1S91z3Mz.html
