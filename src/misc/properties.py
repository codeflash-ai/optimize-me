class SimpleProcessor:
    def __init__(self, numbers):
        self._numbers = numbers
        self._cached_sum = None
    
    @property
    def sum(self):
        total = 0
        for num in self._numbers:
            total += num
        return total
    