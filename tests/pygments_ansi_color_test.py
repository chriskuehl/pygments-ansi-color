# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from pygments.token import Text

import pygments_ansi_color as main
from pygments_ansi_color import Color


@pytest.mark.parametrize(
    ('bold', 'fg_color', 'bg_color', 'expected'),
    (
        (False, False, False, Text),
        (True, False, False, Color.Bold),
        (True, 'Red', False, Color.BoldRed),
        (True, 'Red', 'Blue', Color.BoldRedBGBlue),
    ),
)
def test_token_from_lexer_state(bold, fg_color, bg_color, expected):
    assert main._token_from_lexer_state(bold, fg_color, bg_color) == expected


def test_color_tokens():
    fg_colors = {
        'Red': '#ff0000',
    }
    bg_colors = {
        'Green': '#00ff00',
    }
    assert main.color_tokens(fg_colors, bg_colors) == {
        Color.BGGreen: 'bg:#00ff00',
        Color.Bold: 'bold',
        Color.BoldBGGreen: 'bold bg:#00ff00',
        Color.BoldRed: 'bold #ff0000',
        Color.BoldRedBGGreen: 'bold #ff0000 bg:#00ff00',
        Color.Red: '#ff0000',
        Color.RedBGGreen: '#ff0000 bg:#00ff00',
    }


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
        '\x1b[22mbold turned off\n'
    ) == (
        (Text, 'plain text\n'),
        (Color.Red, 'red text\n'),
        (Color.BoldGreen, 'bold green text\n'),
        (Color.Bold, 'fg color turned off\n'),
        (Text, 'plain text after reset\n'),
        (Color.Bold, 'bold text\n'),
        (Color.BoldBGYellow, 'bold from previous line with yellow bg\n'),
        (Color.Bold, 'bg color turned off\n'),
        (Text, 'bold turned off\n'),
    )


def test_ignores_unrecognized_ansi_color_codes():
    """It should just strip and ignore any unrecognized color ANSI codes."""
    assert _highlight(
        # unknown int code
        '\x1b[99m' 'plain text\n'

        # invalid non-int code
        '\x1b[=m' 'plain text\n'
    ) == (
        (Text, 'plain text\n'),
        (Text, 'plain text\n'),
    )


def test_ignores_valid_ansi_non_color_codes():
    """It should just strip and ignore any non-color ANSI codes.

    These include things like moving the cursor position, erasing lines, etc.
    """
    assert _highlight(
        # restore cursor position
        '\x1b[u' 'plain '
        # move cursor backwards 55 steps
        '\x1b[55C' 'text\n'
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
        'plain \x1b[%text\n'
    ) == (
        (Text, 'plain '),
        (Text, '%text\n'),
    )
