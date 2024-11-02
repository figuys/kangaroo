class ECPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_infinity(self):
        return self.x is None and self.y is None

    def __str__(self):
        return f"ECPoint(x={self.x}, y={self.y})"
