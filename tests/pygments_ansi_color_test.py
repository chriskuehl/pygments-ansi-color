from __future__ import annotations

import itertools

import pytest
from pygments.formatters import HtmlFormatter
from pygments.token import Text
from pygments.token import Token

import pygments_ansi_color as main
from pygments_ansi_color import C
from pygments_ansi_color import Color


@pytest.mark.parametrize(
    ('bold', 'faint', 'fg_color', 'bg_color', 'expected'),
    (
        (False, False, False, False, Text),
        (True, False, False, False, Color.Bold),
        (True, False, 'Red', False, Color.Bold.Red),
        (True, False, 'Red', 'Blue', Color.Bold.Red.BGBlue),
        (True, True, 'Red', 'Blue', Color.Bold.Faint.Red.BGBlue),
    ),
)
def test_token_from_lexer_state(bold, faint, fg_color, bg_color, expected):
    ret = main._token_from_lexer_state(bold, faint, fg_color, bg_color)
    assert ret == expected


def test_color_tokens():
    fg_colors = {'Red': '#ff0000'}
    bg_colors = {'Green': '#00ff00'}
    assert main.color_tokens(fg_colors, bg_colors) == {
        Color.BGGreen: 'bg:#00ff00',
        Color.Bold: 'bold',
        Color.Bold.BGGreen: 'bold bg:#00ff00',
        Color.Bold.Red: 'bold #ff0000',
        Color.Bold.Red.BGGreen: 'bold #ff0000 bg:#00ff00',
        Color.Bold.Faint: 'bold',
        Color.Bold.Faint.BGGreen: 'bold bg:#00ff00',
        Color.Bold.Faint.Red: 'bold #ff0000',
        Color.Bold.Faint.Red.BGGreen: 'bold #ff0000 bg:#00ff00',
        Color.Red: '#ff0000',
        Color.Red.BGGreen: '#ff0000 bg:#00ff00',
        Color.Faint: '',
        Color.Faint.BGGreen: 'bg:#00ff00',
        Color.Faint.Red: '#ff0000',
        Color.Faint.Red.BGGreen: '#ff0000 bg:#00ff00',
    }


def test_color_tokens_256color():
    fg_colors = {'Red': '#ff0000'}
    bg_colors = {'Green': '#00ff00'}

    expected = dict(
        itertools.chain.from_iterable(
            (
                (getattr(C, f'C{i}'), value),
                (getattr(C, f'BGC{i}'), f'bg:{value}'),
            )
            for i, value in main._256_colors.items()
        ),
    )
    expected.update({
        C.Red: '#ff0000',
        C.BGGreen: 'bg:#00ff00',
        C.Bold: 'bold',
        C.Faint: '',
    })
    assert main.color_tokens(
        fg_colors, bg_colors,
        enable_256color=True,
    ) == expected


def _highlight(text):
    return tuple(main.AnsiColorLexer().get_tokens(text))


def test_plain_text():
    assert _highlight('hello world\n') == (
        (Text, 'hello world\n'),
    )


def test_simple_colors():
    assert _highlight(
        'plain text\n'
        '\x1b[31mred text\n'
        '\x1b[1;32mbold green text\n'
        '\x1b[39mfg color turned off\n'
        '\x1b[0mplain text after reset\n'
        '\x1b[1mbold text\n'
        '\x1b[43mbold from previous line with yellow bg\n'
        '\x1b[49mbg color turned off\n'
        '\x1b[92mfg bright green\n'
        '\x1b[101mbg bright red\n'
        '\x1b[39;49mcolors turned off\n'
        '\x1b[2mfaint turned on\n'
        '\x1b[22mbold turned off\n',
    ) == (
        (Text, 'plain text\n'),
        (Color.Red, 'red text\n'),
        (Color.Bold.Green, 'bold green text\n'),
        (Color.Bold, 'fg color turned off\n'),
        (Text, 'plain text after reset\n'),
        (Color.Bold, 'bold text\n'),
        (Color.Bold.BGYellow, 'bold from previous line with yellow bg\n'),
        (Color.Bold, 'bg color turned off\n'),
        (Color.Bold.BrightGreen, 'fg bright green\n'),
        (Color.Bold.BCBrightRed, 'bg bright red\n'),
        (Color.Bold, 'colors turned off\n'),
        (Color.Bold.Faint, 'faint turned on\n'),
        (Text, 'bold turned off\n'),
    )


def test_256_colors():
    assert _highlight(
        'plain text\n'
        '\x1b[38;5;15mcolor 15\n'
        '\x1b[1mbold color 15\n'
        '\x1b[48;5;8mbold color 15 with color 8 bg\n'
        '\x1b[38;5;11;22mnot bold color 11 with color 8 bg\n'
        '\x1b[0mplain text after reset\n',
    ) == (
        (Text, 'plain text\n'),
        (Color.C15, 'color 15\n'),
        (Color.Bold.C15, 'bold color 15\n'),
        (Color.Bold.C15.BGC8, 'bold color 15 with color 8 bg\n'),
        (Color.C11.BGC8, 'not bold color 11 with color 8 bg\n'),
        (Text, 'plain text after reset\n'),
    )


def test_256_colors_invalid_escapes():
    assert _highlight(
        'plain text\n'
        # second value is "4" instead of expected "5"
        '\x1b[38;4;15mA\n'
        # too few values
        '\x1b[38;15mB\n'
        # invalid values (not integers)
        '\x1b[38;4=;15mC\n'
        # invalid values (color larger than 255)
        '\x1b[38;5;937mD\n',
    ) == (
        (Text, 'plain text\n'),
        (Text, 'A\n'),
        (Text, 'B\n'),
        (Text, 'C\n'),
        (Text, 'D\n'),
    )


def test_highlight_empty_end_specifier():
    ret = _highlight('plain\x1b[31mred\x1b[mplain\n')
    assert ret == ((Text, 'plain'), (Color.Red, 'red'), (Text, 'plain\n'))


@pytest.mark.parametrize(
    's',
    (
        pytest.param('\x1b[99m' 'plain text\n', id='unknown int code'),
        pytest.param('\x1b[=m' 'plain text\n', id='invalid non-int code'),
        pytest.param('\x1b(B' 'plain text\n', id='other unknown vt100 code'),
        pytest.param('\x1b' 'plain text\n', id='stray ESC'),
    ),
)
def test_ignores_unrecognized_ansi_color_codes(s):
    """It should just strip and ignore any unrecognized color ANSI codes."""
    assert _highlight(s) == ((Text, 'plain text\n'),)


def test_ignores_valid_ansi_non_color_codes():
    """It should just strip and ignore any non-color ANSI codes.

    These include things like moving the cursor position, erasing lines, etc.
    """
    assert _highlight(
        # restore cursor position
        '\x1b[u' 'plain '
        # move cursor backwards 55 steps
        '\x1b[55C' 'text\n',
    ) == (
        # Ideally these would be just one token, but our regex isn't smart
        # enough yet.
        (Text, 'plain '),
        (Text, 'text\n'),
    )


def test_ignores_completely_invalid_escapes():
    """It should strip and ignore invalid escapes.

    This shouldn't happen in valid ANSI text, but we could have an escape
    followed by garbage.
    """
    assert _highlight(
        'plain \x1b[%text\n',
    ) == (
        (Text, 'plain '),
        (Text, '%text\n'),
    )


@pytest.fixture
def test_formatter():
    class TestFormatter(main.ExtendedColorHtmlFormatterMixin, HtmlFormatter):
        pass
    return TestFormatter()


@pytest.mark.parametrize(
    ('token', 'expected_classes'),
    (
        # Standard Pygments tokens shouldn't be changed.
        (Text, ''),
        (Token.Comment, 'c'),
        (Token.Comment.Multi, 'c c-Multi'),
        (Token.Operator, 'o'),

        # Non-standard (but non-Color) Pygments tokens also shouldn't be changed.
        (Token.Foo, ' -Foo'),
        (Token.Foo.Bar.Baz, ' -Foo -Foo-Bar -Foo-Bar-Baz'),

        # Color tokens should be split out into multiple, non-nested classes prefixed with "C".
        (Token.Color.Bold, ' -Color -Color-Bold -C-Bold'),
        (Token.Color.Red, ' -Color -Color-Red -C-Red'),
        (Token.Color.Bold.Red, ' -Color -Color-Bold -Color-Bold-Red -C-Bold -C-Red'),
        (
            Token.Color.Bold.Red.BGGreen,
            ' -Color -Color-Bold -Color-Bold-Red -Color-Bold-Red-BGGreen -C-Bold -C-Red -C-BGGreen',
        ),
        (Token.Color.C5, ' -Color -Color-C5 -C-C5'),
        (Token.Color.C5.BGC18, ' -Color -Color-C5 -Color-C5-BGC18 -C-C5 -C-BGC18'),
    ),
)
def test_formatter_mixin_get_css_classes(test_formatter, token, expected_classes):
    assert test_formatter._get_css_classes(token) == expected_classes
