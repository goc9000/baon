class MatchContext(object):
    text = None
    position = None
    stop = None
    aliases = None
    forward_aliases = None
    
    def __init__(self, text, initial_aliases=None):
        self.text = text
        self.position = 0
        self.stop = False
        self.forward_aliases = set()
        self.aliases = initial_aliases.copy() if not initial_aliases is None else dict()

    def save(self):
        return (self.text, self.position, self.stop, self.forward_aliases.copy(), self.aliases.copy())

    def restore(self, savepoint):
        self.text, self.position, self.stop, self.forward_aliases, self.aliases = savepoint
