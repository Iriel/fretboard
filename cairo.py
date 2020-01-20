#!/usr/bin/env python3

import cairocffi as cairo



#surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 200)
surface = cairo.PDFSurface('cairo.pdf', 300, 800)
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
FRET_HEIGHT = 30
NOTE_FONT_SIZE = 20
ACCIDENTAL_FONT_SIZE = 14

FRET_COUNT = 10
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
    context.translate(10, 10)

    context.move_to(0, FRET_HEIGHT * (FRET_COUNT + 1))
    context.line_to(0, FRET_HEIGHT)
    context.line_to(STRING_WIDTH * STRING_COUNT, FRET_HEIGHT)
    context.line_to(STRING_WIDTH * STRING_COUNT, FRET_HEIGHT * (FRET_COUNT + 1))
    context.stroke()

    context.set_line_width(0.25)

    for s in range(1, STRING_COUNT):
        context.move_to(STRING_WIDTH * s, FRET_HEIGHT)
        context.rel_line_to(0, FRET_HEIGHT * FRET_COUNT)
        context.stroke()

    context.set_line_width(1.0)

    for f in range(2, FRET_COUNT + 2):
        context.move_to(0, FRET_HEIGHT * f)
        context.rel_line_to(STRING_WIDTH * STRING_COUNT, 0)
        context.stroke()

    context.set_font_size(NOTE_FONT_SIZE)
    (xb, yb, w, h, xa, ya) = context.text_extents('X')
    FONT_HEIGHT = h

    context.move_to(STRING_WIDTH * 0.5, FONT_HEIGHT + (FRET_HEIGHT - FONT_HEIGHT) / 2)

    center_note_text(context, ('F', '#'))
