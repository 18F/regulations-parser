from pyparsing import LineEnd, LineStart, SkipTo

from regparser.grammar import atomic, unified, utils


section = (
    atomic.section_marker.copy().leaveWhitespace()
    + unified.part_section
    + SkipTo(LineEnd())
)


par = (
    atomic.section.copy().leaveWhitespace()
    + unified.depth1_p
    + SkipTo(LineEnd())
)


marker_par = (
    atomic.paragraph_marker.copy().leaveWhitespace()
    + atomic.section
    + unified.depth1_p
)


appendix = (
    atomic.appendix_marker.copy().leaveWhitespace()
    + atomic.appendix
    + SkipTo(LineEnd())
)


parser = utils.QuickSearchable(
    LineStart() + (section | marker_par | par | appendix))
