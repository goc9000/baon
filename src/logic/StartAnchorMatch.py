from Match import Match

class StartAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def _execute(self, context):
        if context.position == 0:
            context.last_match_pos = context.position
            return ''
        else:
            return False
