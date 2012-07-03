from Action import Action

class SaveToAliasAction(Action):
    alias = None
    
    def __init__(self, alias):
        Action.__init__(self)
        
        self.alias = alias