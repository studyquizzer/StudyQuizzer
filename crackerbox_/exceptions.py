class NotEnoughWordsError(Exception):
    def __init__(self, length):
        self.lenght = length
        super().__init__(
            f"Not enough words, Need more words (current words = {length})"
        )
