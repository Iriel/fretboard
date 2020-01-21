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

STRING_WIDTH = 21
FRET_HEIGHT = 25
CELL_DIAMETER = 17.3
NOTE_FONT_SIZE = 13
ACCIDENTAL_FONT_SIZE = 9

FRET_COUNT = 13.2
STRING_COUNT = 6
FONT_HEIGHT = -1

NUT_LINE_WIDTH = 3
FRET_LINE_WIDTH = 1
SPECIAL_FRET_LINE_WIDTH = 1

SPECIAL_FRET_FILL_COLOR = (0.9, 0.9, 1.0)

STRING_LINE_WIDTH = 1.5

CELL_STYLE_CIRCLE = (1, 0, 1)
CELL_STYLE_HEX = (6, 0, 1.1)
CELL_STYLE_BOX = (4, 0.5, 1.3)
CELL_STYLE_PENT = (5, 0.5, 1.12)
CELL_STYLE_OCT = (8, 0.5, 1.05)
CELL_STYLE_SEPT = (7, 0, 1.1) ## Alternate with (7, 0.5, 1.1)

CELL_STYLE = CELL_STYLE_CIRCLE

CELL_STYLES = (CELL_STYLE_CIRCLE, CELL_STYLE_HEX, CELL_STYLE_BOX, CELL_STYLE_PENT, CELL_STYLE_OCT)

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


surface = cairo.PDFSurface('cairo.pdf', 8.5 * 72, 11 * 72)
context = cairo.Context(surface)

context.set_line_cap(cairo.LINE_CAP_SQUARE)
context.set_line_join(cairo.LINE_JOIN_MITER)

options = cairo.FontOptions()
options.set_antialias(cairo.ANTIALIAS_BEST)

with context:
    context.translate(36, 36)
    context.scale(2.0)

    context.translate(STRING_WIDTH / 2, FRET_HEIGHT)

    # Draw the special frets
    for f in range(1, math.floor(FRET_COUNT) + 1):
        if SPECIAL_FRETS[(f % 12)]:
            with context:
                context.set_source_rgb(*SPECIAL_FRET_FILL_COLOR)
                context.new_path()
                context.rectangle(0, FRET_HEIGHT  * (f - 1), STRING_WIDTH * (STRING_COUNT - 1), FRET_HEIGHT)
                context.fill()

    # Draw the strings
    with context:
        context.set_line_width(STRING_LINE_WIDTH)
        context.set_source_rgb(0.7, 0.7, 0.7)

        for s in range(0, STRING_COUNT):
            context.move_to(STRING_WIDTH * s, 0)
            context.rel_line_to(0, FRET_HEIGHT * FRET_COUNT)
            context.stroke()

    # Draw the nut
    context.set_line_width(NUT_LINE_WIDTH)
    context.move_to(0, 0)
    context.rel_line_to(STRING_WIDTH * (STRING_COUNT - 1), 0)
    context.stroke()

    # Draw the fret lines
    for f in range(1, math.floor(FRET_COUNT) + 1):
        if SPECIAL_FRETS[(f % 12)]:
            context.set_line_width(SPECIAL_FRET_LINE_WIDTH)
        else:
            context.set_line_width(FRET_LINE_WIDTH)
        context.move_to(0, FRET_HEIGHT * f)
        context.rel_line_to(STRING_WIDTH * (STRING_COUNT - 1), 0)
        context.stroke()


    context.set_font_size(NOTE_FONT_SIZE)
    (xb, yb, w, h, xa, ya) = context.text_extents('X')
    FONT_HEIGHT = h

    for s in range(0, STRING_COUNT):
        note_offset = SCALE_OFFSETS[s]
        for f in range(0, math.floor(FRET_COUNT) + 1):
            note = SCALE_NOTES[(f + note_offset) % 12]

            cx = STRING_WIDTH * s
            cy = FRET_HEIGHT * (f - 0.5)
            fcy = FONT_HEIGHT - FONT_HEIGHT / 2 + cy

            if len(note) > 1:
                context.set_line_width(0.5)
            else:
                context.set_line_width(1.5)
            radius = CELL_DIAMETER / 2


            style = CELL_STYLES[(s + f + note_offset) % len(CELL_STYLES)]
            (num_points, point_offset, radius_mul) = style

            context.new_path()
            if num_points < 3:
                context.arc(cx, cy, radius * radius_mul, 0, math.pi * 2)
            else:
                for p in range(0, num_points):
                    angle = math.pi * 2.0 * (p + point_offset) / num_points
                    ox = math.sin(angle) * radius * radius_mul
                    oy = math.cos(angle) * radius * radius_mul
                    if p == 0:
                        context.move_to(cx + ox, cy + oy)
                    else:
                        context.line_to(cx + ox, cy + oy)
                context.close_path()

            with context:
                if note == ('C'):
                    context.set_source_rgb(0, 0, 0)
                else:
                    context.set_source_rgb(0.95, 0.95, 0.95)
                context.fill_preserve()

            context.stroke()

            with context:
                context.move_to(cx, fcy)
                if len(note) > 1:
                    context.set_source_rgb(0.7, 0.7, 0.7)
                if note == ('C'):
                    context.set_source_rgb(1, 1, 1)
                center_note_text(context, note)

