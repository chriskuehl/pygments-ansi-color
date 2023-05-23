# pygments-ansi-color

[![build status](https://github.com/chriskuehl/pygments-ansi-color/actions/workflows/main.yml/badge.svg)](https://github.com/chriskuehl/pygments-ansi-color/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/chriskuehl/pygments-ansi-color/main.svg)](https://results.pre-commit.ci/latest/github/chriskuehl/pygments-ansi-color/main)
[![PyPI version](https://badge.fury.io/py/pygments-ansi-color.svg)](https://pypi.python.org/pypi/pygments-ansi-color)

This project adds **parsing and coloring of ANSI sequences to Pygments**.

![](https://i.fluffy.cc/nHPkL3gfBtj5Kt4H3RR51T9TJLh6rtv2.png)


## Installation

The project is [available on PyPi under the `pygments-ansi-color` name
](https://pypi.org/project/pygments-ansi-color/):

```shell-session
$ pip install pygments-ansi-color
```


## Basic usage

Once installed, you can highlight your content with Pygments' regular API. All
you need is to use the dedicated ANSI lexer and formatter provided by
`pygments-ansi-color`:

```python
from pygments import highlight
from pygments_ansi_color import AnsiHtmlFormatter, AnsiColorLexer

code = "\x1b[0m\x1b[34mA\x1b[0m\x1b[35mN\x1b[0m\x1b[36mS\x1b[0m\x1b[31mI\x1b[0m\x1b[32m"
print(highlight(code, AnsiColorLexer(), AnsiHtmlFormatter()))
```

This produce the following HTML code, with ANSI codes properly interpreted and
linked to their color:

```html
<div class="highlight">
   <pre>
      <span></span>
      <span class=" -Color -Color-Blue -C-Blue">A</span>
      <span class=" -Color -Color-Magenta -C-Magenta">N</span>
      <span class=" -Color -Color-Cyan -C-Cyan">S</span>
      <span class=" -Color -Color-Red -C-Red">I</span>
   </pre>
</div>
```

And here are is the corresponding CSS style:

```python
print(AnsiHtmlFormatter().get_style_defs('.highlight'))
```

```css
pre { line-height: 125%; }
(...)
.highlight .-Color-Blue { color: #3465a4 } /* Color.Blue */
.highlight .-Color-Cyan { color: #34e2e2 } /* Color.Cyan */
.highlight .-Color-Magenta { color: #c509c5 } /* Color.Magenta */
(...)
```


## Design

In the code above, we rely on a custom `AnsiColorLexer`. Its role is to produce
custom color tokens for the highlighter. That's because existing Pygments
lexers are built around contextual tokens (think `Comment` or `Punctuation`)
rather than actual colors.

In the case of ANSI escape sequences, colors have no context beyond the color
themselves; we'd always want a `red` rendered as `red`, regardless of your
particular theme. Hence these custom tokens.

Now for the rendering part, we again need a custom `AnsiHtmlFormatter`, so we
have a way to interpret these color tokens, and produce the corresponding
custom CSS classes with the right style.


## Pygments integration

`pygments-ansi-color` is properly integrated to Pygments, so you do not need
custom code to integrate with it.

At intallation, `pygments-ansi-color` registers its custom lexers and
formatters. You can fetch them from their own IDs:

```pycon
>>> from pygments.lexers import get_lexer_by_name
>>> get_lexer_by_name('ansi-color')
<pygments.lexers.AnsiColorLexer>
```

```pycon
>>> from pygments.formatters import get_formatter_by_name
>>> get_formatter_by_name('ansi-html')
<pygments_ansi_color.AnsiHtmlFormatter object at 0x1044cbf10>
```


## Default ANSI colors

By default, `pygments-ansi-color` renders [the 8 basic ANSI colors and their
bright variants
](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit), for both
foreground and background.

But the default colors are not set to the primary hues from the VGA-era.
Instead, the set has been carefully crafted for readability, and are [loosely
based on the color scheme used by iTerm2
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


## Custom ANSI theme

Still, you may want to use your own colors, to tweak the rendering to your
background, or to match your own theme.

For that you can override each color individually, by passing them as
arguments to `AnsiHtmlFormatter`:

```python
AnsiHtmlFormatter(
   fg_colors={'Cyan': '#00ffff', 'BrightCyan': '#00ffff'},
   bg_colors={'BrightWhite': '#000000'},
)
```


## Pygments style

You can [use any Pygments style you want](https://pygments.org/styles/) with
`AnsiHtmlFormatter`:

```python
AnsiHtmlFormatter(style="monokai")
```

Behind the scene, `AnsiHtmlFormatter` will create a custom, local copy of the
style you choose, and augment it with our custom directives, so we can apply
styles to the custom color tokens produced by `AnsiColorLexer`.

> **Note**: Custom style
>
> For some reasons, you might want to replicate this behavior and manually
> manage your style. Here is how to do it.
>
> First, choose an exising Pygments style to be used as a base. Let's do that
> with `pygments.styles.xcode.XcodeStyle` as reference and make our final
> `MyStyle` custom style:
>
> ```python
> from pygments.styles.xcode import XcodeStyle
>
> from pygments_ansi_color import color_tokens
>
> class MyStyle(XcodeStyle):
>    styles = dict(XcodeStyle.styles)
>    styles.update(color_tokens())
> ```
>
> You can customize the styling further as `color_tokens` takes the same
> `fg_colors` and `bg_colors` parameters as `AnsiHtmlFormatter` (see above).


## `256-color` support

This library supports rendering terminal output using the [`256-color` (8-bit)
mode](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit) of ANSI codes.

This is **not active by default** and is an opt-in feature, because of its
underlaying complexity.

To enable `256-color` support, you only need to pass `enable_256color=True`,
and then you can use Pygments as normal:

```python
from pygments import highlight
from pygments_ansi_color import AnsiHtmlFormatter, AnsiColorLexer

formatter = AnsiHtmlFormatter(enable_256color=True)

code = "\x1b[0m\x1b[34mA\x1b[0m\x1b[35mN\x1b[0m\x1b[36mS\x1b[0m\x1b[31mI\x1b[0m\x1b[32m"
print(highlight(code, AnsiColorLexer(), formatter))
```

> **Note**: `256-color` design
>
> Pygments' tokens are not allowed to overlap. Which means we cannot
> accumulates the effects of multiple tokens over a segment of text. So we use
> a trick which consist in the composition of a single state into a single
> token. That way, the state tuple of `(bold_state, fgcolor, bgcolor)` is
> encoded as the `Color.Bold.FGColor.BGColor` token.
>
> In the default mode where we only support the standard 8 colors (plus 1 for
> no color), we need `2 × 9 × 9 - 1 = 161` tokens, which is reasonable to have
> them all contained within one CSS file. With 256 colors (plus the standard 8,
> plus 1 for no color) though, we'd need `2 × 265 × 265 - 1 = 140,449`
> individual tokens defined in CSS. This makes the CSS too large to be
> practical.
>
> To make the `256-color` mode support realistic, we patch Pygments' HTML
> formatter so that it places a class for each part of the state tuple
> independently. This means you only need `1 + 265 + 265 = 531` CSS classes to
> support all possibilities.


## Language lexers with ANSI output

With this project, you can provide strings of ANSI codes and have them rendered
in HTML by Pygments. Which means you can parse and render pure ANSI content
like ANSI art files. Or build your own lexer that produces ANSI output.

Now there are some [languages supported by Pygments
](https://pygments.org/languages/) that produce ANSI output. For example, the
[`console` lexer can be used to highlight shell sessions
](https://pygments.org/docs/terminal-sessions/). If the general structure of
the shell session will be highlighted, the ANSI codes in the output will not be
interpreted and will be rendered as-is.

To fix that, you need [ANSI-capable lexers from Click Extra
](https://kdeldycke.github.io/click-extra/pygments.html#lexers). These can
parse both the language syntax and the ANSI codes.

With Click Extra, you will be able to use the `ansi-console` lexer to highlight
shell sessions with ANSI support.


## Used by

- [fluffy](https://fluffy.cc) - A file-sharing web app that doesn't suck, and
  the project that [this lexer was originally developed for
  ](https://i.fluffy.cc/3Gq7Fg86mv3dX30Qx9LHMWcKMqsQLCtd.html).
- [Click Extra](https://github.com/kdeldycke/click-extra) - A ready-to-use
  wrapper for Click, with extra colorization and configuration loading.
- [PrairieLearn](https://github.com/PrairieLearn/PrairieLearn) - Online
  problem-driving learning system.
- [pygments-pytest](https://github.com/asottile/pygments-pytest) - A pygments
  lexer for pytest output.
