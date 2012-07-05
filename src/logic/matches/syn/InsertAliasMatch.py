from InsertionMatch import InsertionMatch

class InsertAliasMatch(InsertionMatch):
    alias = None
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)

        self.alias = alias
    
    def _execute(self, context):
        context.last_match_pos = None
        
        if self.alias in context.aliases:
            return context.aliases[self.alias]
        else:
            context.forward_aliases.add(self.alias)
            return ''