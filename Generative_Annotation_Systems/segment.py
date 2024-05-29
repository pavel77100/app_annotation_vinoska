import numpy as np
import genetic4 as gg
# from genetic4 import genetic_generator_loop



class Segment():
    scale_sheet = 100
    ft_to_mm = 304.8
    sheet_scale_convert = ft_to_mm / scale_sheet


    def __init__(self, V_b_l,U_b_l, V_t_r, U_t_r, field_img, field_compress_img, lenght_V_of_img, lenght_U_of_img, scale_conv, optimaze_k):
        self.V_b_l = V_b_l
        self.U_b_l = U_b_l
        self.V_t_r = V_t_r
        self.U_t_r = U_t_r

        self.lenght_V_of_img = lenght_V_of_img
        self.lenght_U_of_img = lenght_U_of_img

        self.result_gen = []
        self.deserial_gen = []

        self.scale_conv = scale_conv
        self.optimaze_k = optimaze_k


        self.dot_array = []
        self.dots_convert_array = []
        self.field_img = field_img
        self.field_compress_img = field_compress_img
        pass

    def dot_sort(self, dots_for_sort):

        result = []
        for item in dots_for_sort:
            test1 = self.V_b_l < item["LeaderEnd_V"] <= self.V_t_r
            test2 = self.U_b_l < item["LeaderEnd_U"] <= self.U_t_r
            if test1 and test2:
                result.append(item)
        self.dot_array = result

    def dots_to_segment_coordinates(self):
        for item in self.dot_array:
            elem = {}
            elem["Height"] = np.around(np.divide(item["Width"] * self.scale_conv, self.optimaze_k * 2.2)).astype(int)
            elem["Width"] = np.around(np.divide(item["Height"] * self.scale_conv, self.optimaze_k * 2.2)).astype(int)
            elem["LeaderEnd_V"] = np.ceil(np.divide((item["LeaderEnd_V"] - self.V_b_l) * self.scale_conv, self.optimaze_k)).astype(
                int)
            elem["LeaderEnd_U"] = np.ceil(np.divide((item["LeaderEnd_U"] - self.U_b_l) * self.scale_conv, self.optimaze_k)).astype(
                int)

            elem["TagId"] = item["TagId"]
            self.dots_convert_array.append(elem)

    def generator(self):
        result = gg.genetic_generator_loop((self.lenght_V_of_img, self.lenght_U_of_img), self.field_img, self.field_compress_img, self.dots_convert_array)
        result_conv = []
        for item in result:

              otvet = {}
              otvet["V"] = self.V_b_l + item["V"] * self.optimaze_k / self.scale_conv
              otvet["U"] = self.U_b_l + item["U"] * self.optimaze_k / self.scale_conv

              otvet["LeaderElbow_U"] = self.U_b_l + item["LeaderElbow_U"] * self.optimaze_k / self.scale_conv
              otvet["LeaderElbow_V"] = self.V_b_l + item["LeaderElbow_V"] * self.optimaze_k / self.scale_conv

              otvet["TagId"] = item["TagId"]
              result_conv.append(otvet)



        return result_conv






