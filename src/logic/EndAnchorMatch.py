from Match import Match

class EndAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def execute(self, context):
        if context.position == len(context.text):
            return ''
        else:
            return False
