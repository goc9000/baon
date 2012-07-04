from Match import Match

class StartAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def execute(self, context):
        if context.position == 0:
            return ''
        else:
            return False
