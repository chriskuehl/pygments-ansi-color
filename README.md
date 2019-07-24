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
   import pygments.formatters
   import pygments.lexers

   lexer = pygments.lexers.get_lexer_by_name('ansi-color')
   formatter = pygments.formatters.HtmlFormatter(style=MyStyle)
   print(pygments.highlight('your text', lexer, formatter))
   ```


### Example

You can see an example [on fluffy][fluffy-example], the project that this lexer
was originally developed for.

The colors are defined as part of your Pygments style and can be changed.


### Optional: Enable "256 color" support

This library supports rendering terminal output using [256 color
(8-bit)][256-color] ANSI color codes. However, because of limitations in
Pygments tokens, this is an opt-in feature which requires patching the
formatter you're using.

The reason this requires patching the Pygments formatter is that Pygments does
not support multiple tokens on a single piece of text, requiring us to
"compose" a single state (which is a tuple of `(bold enabled, fg color, bg
color)`) into a single token like `Color.Bold.FGColor.BGColor`. We then need to
output the styles for this token in the CSS.

In the default mode where we only support the standard 8 colors (plus 1 for no
color), we need 2 × 9 × 9 - 1 = 161 tokens, which is reasonable to contain in
one CSS file. With 256 colors (plus the standard 8, plus 1 for no color),
though, we'd need 2 × 265 × 265 - 1 = 140,449 tokens defined in CSS. This makes
the CSS too large to be practical.

To make 256-color support realistic, we patch Pygments' HTML formatter so that
it places a class for each part of the state tuple independently. This means
you need only 1 + 265 + 265 = 531 CSS classes to support all possibilities.

If you'd like to enable 256-color support, you'll need to do two things:

1. When calling `color_tokens`, pass `enable_256color=True`:

   ```python
   styles.update(color_tokens(fg_colors, bg_colors, enable_256color=True))
   ```

   This change is what causes your CSS to have the appropriate classes in it.

2. When constructing your formatter, use the `ExtendedColorHtmlFormatterMixin`
   mixin, like this:

   ```python
   from pygments.formatters import HtmlFormatter
   from pygments_ansi_color import ExtendedColorHtmlFormatterMixin

   ...

   class MyFormatter(ExtendedColorHtmlFormatterMixin, HtmlFormatter):
       pass

   ...

   formatter = pygments.formatter.HtmlFormatter(style=MyStyle)
   ```

   This change is what causes the rendered HTML to have the right class names.

Once these two changes have been made, you can use pygments-ansi-color as normal.


[fluffy-example]: https://i.fluffy.cc/3Gq7Fg86mv3dX30Qx9LHMWcKMqsQLCtd.html
[256-color]: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
