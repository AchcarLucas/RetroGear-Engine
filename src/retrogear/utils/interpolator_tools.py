class InterpolatorTools():
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
        t = InterpolatorTools.clamp((t - start) / (end - start), 0.0, 1.0)
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def smootherstep(start, end, t):
        t = InterpolatorTools.clamp((t - start) / (end - start), 0.0, 1.0)
        return t * t * t * (t * (t * 6 - 15) + 10)