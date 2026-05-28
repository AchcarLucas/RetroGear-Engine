class MathTools():
    @staticmethod
    def lerp(start, end, t):
        return start + (end - start) * t
    
    @staticmethod
    def inverse_lerp(start, end, value):
        if end - start == 0:
            return 0
        return (value - start) / (end - start)
    
    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    
    @staticmethod
    def smoothstep(start, end, t):
        t = MathTools.clamp((t - start) / (end - start), 0.0, 1.0)
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def smootherstep(start, end, t):
        t = MathTools.clamp((t - start) / (end - start), 0.0, 1.0)
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    @staticmethod
    def rectangular_wave(t: float, p: float, duty: float):
        """
            t     : time (float ou array)
            p     : period
            duty : duty cycle (0 a 1)
        """
        return (t % p) < (duty * p)

    @staticmethod
    def abs(value: float) -> float:
        return value if value >= 0 else -value
    
    @staticmethod
    def clamp(value: float, max_abs_value: float) -> float:
        if value > max_abs_value:
            return max_abs_value
        elif value < -max_abs_value:
            return -max_abs_value
        else:
            return value
        
    @staticmethod
    def normalize(value: float, min_value: float, max_value: float) -> float:
        if max_value - min_value == 0:
            return 0
        return (value - min_value) / (max_value - min_value)

    @staticmethod
    def floor(x):
        if x >= 0 or x == int(x):
            return int(x)
        return int(x) - 1
    
    @staticmethod
    def avarage_tuple(t_a: tuple, t_b: tuple):
        return tuple((a + b) * 0.5 for a, b in zip(t_a, t_b))
    
    def factor_tupla(t:tuple, factor:float):
        return tuple(a * factor for a in t)