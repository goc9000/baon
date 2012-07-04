from Match import Match

class EndAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def _execute(self, context):
        if context.position == len(context.text):
            context.last_match_pos = context.position
            return ''
        else:
            return False
