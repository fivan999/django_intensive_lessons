class GraderZeroIntConverter:
    """конвертер целых положительных чисел"""

    regex = '[1-9][0-9]*'

    def to_python(self, value: str) -> int:
        """конвертируем из нужной строки в число"""
        return int(value)

    def to_url(self, value: int) -> str:
        """сконвертируем из числа в url"""
        return str(value)
