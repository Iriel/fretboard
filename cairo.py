#!/usr/bin/env python3

import math
import cairocffi as cairo

SPECIAL_FRETS = (True, False, False, True,
                 False, True, False, True,
                 False, True, False, False)

SCALE_NOTES = (
    ('A'),
    ('A', '#'),
    ('B'),
    ('C'),
    ('C', '#'),
    ('D'),
    ('D', '#'),
    ('E'),
    ('F'),
    ('F', '#'),
    ('G'),
    ('G', '#'))

SCALE_OFFSETS = (7, 0, 5, 10, 2, 7)

#surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 200)
surface = cairo.PDFSurface('cairo.pdf', 8.5 * 72, 11 * 72)
context = cairo.Context(surface)
with context:
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()
# Restore the default source which is black.
#context.move_to(90, 140)
#context.rotate(-0.5)
#context.set_font_size(20)
#context.show_text('Hi from cairo!')
#

STRING_WIDTH = 20
FRET_HEIGHT = 25
NOTE_FONT_SIZE = 13
ACCIDENTAL_FONT_SIZE = 9

FRET_COUNT = 12
STRING_COUNT = 6
FONT_HEIGHT = -1


def center_note_text(ctx, note):
    ctx.set_font_size(NOTE_FONT_SIZE)
    (nxb, nyb, nw, nh, nxa, nya) = ctx.text_extents(note[0])

    wid = (nw + nxb)
    axofs = 0

    if len(note) > 1:
        ctx.set_font_size(ACCIDENTAL_FONT_SIZE)
        (axb, ayb, aw, ah, axa, aya) = ctx.text_extents(note[1])
        wid += aw * 0.85
        axofs = -axb - (aw * 0.15)
        ctx.set_font_size(NOTE_FONT_SIZE)

    ctx.rel_move_to(wid / -2, 0)
    ctx.show_text(note[0])

    if len(note) > 1:
        ctx.rel_move_to(axofs, 0)
        ctx.set_font_size(ACCIDENTAL_FONT_SIZE)
        ctx.show_text(note[1])


context.set_line_cap(cairo.LINE_CAP_SQUARE)
context.set_line_join(cairo.LINE_JOIN_MITER)

options = cairo.FontOptions()
options.set_antialias(cairo.ANTIALIAS_BEST)

with context:
    context.translate(36, 36)
    context.scale(2.0)

    context.translate(STRING_WIDTH / 2, FRET_HEIGHT)

#    context.move_to(0, FRET_HEIGHT * (FRET_COUNT + 1))
    context.set_line_width(4)
    context.move_to(0, 0)
    context.rel_line_to(STRING_WIDTH * (STRING_COUNT - 1), 0)
    context.stroke()

    context.set_line_width(0.25)

    for s in range(0, STRING_COUNT):
        context.move_to(STRING_WIDTH * s, 0)
        context.rel_line_to(0, FRET_HEIGHT * FRET_COUNT)
        context.stroke()

    context.set_line_width(1.0)

    for f in range(1, FRET_COUNT + 1):
        if SPECIAL_FRETS[(f % 12)]:
            context.set_line_width(2.0)
        else:
            context.set_line_width(1.0)
        context.move_to(0, FRET_HEIGHT * f)
        context.rel_line_to(STRING_WIDTH * (STRING_COUNT - 1), 0)
        context.stroke()

    context.set_font_size(NOTE_FONT_SIZE)
    (xb, yb, w, h, xa, ya) = context.text_extents('X')
    FONT_HEIGHT = h

    for s in range(0, STRING_COUNT):
        note_offset = SCALE_OFFSETS[s]
        for f in range(0, FRET_COUNT + 1):
            note = SCALE_NOTES[(f + note_offset) % 12]

            cx = STRING_WIDTH * s
            cy = FRET_HEIGHT * (f - 0.5)
            fcy = FONT_HEIGHT - FONT_HEIGHT / 2 + cy

            context.set_line_width(1.5)
            context.new_path()
            context.arc(cx, cy, STRING_WIDTH / 2.3, 0, math.pi * 2)
            with context:
                context.set_source_rgb(0.95, 0.95, 0.95)
                context.fill_preserve()

            context.stroke()

            context.move_to(cx, fcy)
            center_note_text(context, note)

