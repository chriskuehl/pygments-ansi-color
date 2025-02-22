pygments-ansi-color
-------------------

[![build status](https://github.com/chriskuehl/pygments-ansi-color/actions/workflows/main.yml/badge.svg)](https://github.com/chriskuehl/pygments-ansi-color/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/chriskuehl/pygments-ansi-color/main.svg)](https://results.pre-commit.ci/latest/github/chriskuehl/pygments-ansi-color/main)
[![PyPI version](https://badge.fury.io/py/pygments-ansi-color.svg)](https://pypi.python.org/pypi/pygments-ansi-color)

An ANSI color-code highlighting lexer for Pygments.

![](https://i.fluffy.cc/nHPkL3gfBtj5Kt4H3RR51T9TJLh6rtv2.png)


### Basic usage

1. Install `pygments-ansi-color`:

   ```shell-session
   $ pip install pygments-ansi-color
   ```

2. `pygments-ansi-color` is not magic (yet?), so you need to [choose an existing
   Pygments style](https://pygments.org/styles/), which will be used as a base
   for your own style.

   For example, let's choose `pygments.styles.xcode.XcodeStyle`, which looks
   great to use. And then we will augment this reference style with
   `pygments-ansi-color`'s color tokens thanks to the `color_tokens` function,
   to make our final `MyStyle` custom style.

   Here is how the code looks like:

   ```python
   from pygments_ansi_color import color_tokens

   class MyStyle(pygments.styles.xcode.XcodeStyle):
       styles = dict(pygments.styles.xcode.XcodeStyle.styles)
       styles.update(color_tokens())
   ```

   That's all the custom code you need to integrate with `pygments-ansi-color`.

3. Now you can highlight your content with the dedicated ANSI lexer and your
   custom style, with the Pygments regular API:

   ```python
   import pygments
   import pygments.formatters
   import pygments.lexers

   lexer = pygments.lexers.get_lexer_by_name('ansi-color')
   formatter = pygments.formatters.HtmlFormatter(style=MyStyle)
   print(pygments.highlight('your text', lexer, formatter))
   ```

### Design

We had to configure above a custom Pygments style with the appropriate color
tokens. That's because existing Pygments lexers are built around contextual
tokens (think `Comment` or `Punctuation`) rather than actual colors.

In the case of ANSI escape sequences, colors have no context beyond the color
themselves; we'd always want a `red` rendered as `red`, regardless of your
particular theme.


### Custom theme

By default, `pygments-ansi-color` maps ANSI codes to its own set of colors.
They have been carefully crafted for readability, and are [loosely based on the
color scheme used by iTerm2
](https://github.com/chriskuehl/pygments-ansi-color/pull/27#discussion_r1113790011).

Default colors are hard-coded by the `pygments_ansi_color.DEFAULT_STYLE`
constant as such:
- ![#000000](https://placehold.co/15/000000/000000) `Black`: `#000000`
- ![#ef2929](https://placehold.co/15/ef2929/ef2929) `Red`: `#ef2929`
- ![#8ae234](https://placehold.co/15/8ae234/8ae234) `Green`: `#8ae234`
- ![#fce94f](https://placehold.co/15/fce94f/fce94f) `Yellow`: `#fce94f`
- ![#3465a4](https://placehold.co/15/3465a4/3465a4) `Blue`: `#3465a4`
- ![#c509c5](https://placehold.co/15/c509c5/c509c5) `Magenta`: `#c509c5`
- ![#34e2e2](https://placehold.co/15/34e2e2/34e2e2) `Cyan`: `#34e2e2`
- ![#f5f5f5](https://placehold.co/15/f5f5f5/f5f5f5) `White`: `#f5f5f5`
- ![#676767](https://placehold.co/15/676767/676767) `BrightBlack`: `#676767`
- ![#ff6d67](https://placehold.co/15/ff6d67/ff6d67) `BrightRed`: `#ff6d67`
- ![#5ff967](https://placehold.co/15/5ff967/5ff967) `BrightGreen`: `#5ff967`
- ![#fefb67](https://placehold.co/15/fefb67/fefb67) `BrightYellow`: `#fefb67`
- ![#6871ff](https://placehold.co/15/6871ff/6871ff) `BrightBlue`: `#6871ff`
- ![#ff76ff](https://placehold.co/15/ff76ff/ff76ff) `BrightMagenta`: `#ff76ff`
- ![#5ffdff](https://placehold.co/15/5ffdff/5ffdff) `BrightCyan`: `#5ffdff`
- ![#feffff](https://placehold.co/15/feffff/feffff) `BrightWhite`: `#feffff`

Still, you may want to use your own colors, to tweak the rendering to your
background color, or to match your own theme.

For that you can override each color individually, by passing them as
arguments to the `color_tokens` function:

```python
from pygments_ansi_color import color_tokens

class MyStyle(pygments.styles.xcode.XcodeStyle):
   styles = dict(pygments.styles.xcode.XcodeStyle.styles)
   styles.update(color_tokens(
      fg_colors={'Cyan': '#00ffff', 'BrightCyan': '#00ffff'},
      bg_colors={'BrightWhite': '#000000'},
   ))
```


### Used by

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
   styles.update(color_tokens(enable_256color=True))
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
