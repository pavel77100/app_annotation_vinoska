class Segment():
    scale_sheet = 100
    ft_to_mm = 304.8
    sheet_scale_convert = ft_to_mm / scale_sheet


    def __init__(self, V_b_l,U_b_l, V_t_r, U_t_r, dot_array):
        self.V_b_l = V_b_l
        self.U_b_l = U_b_l
        self.V_t_r = V_t_r
        self.U_t_r = U_t_r
        self.dot_array = dot_array
        pass