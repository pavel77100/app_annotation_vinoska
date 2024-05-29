
# import json

# with open("res/psevdo_img_test/test_auto/tmpF034_test.json", 'r') as json_file:
#     data = json.load(json_file)
def deserial_funk(data):
    FT_TO_MM = 304.8
    scale_sheet = data["Scale"]
    sheet_scale_convert = FT_TO_MM/scale_sheet

    # corrdinate_zero = ((data["TopRight"]["V"]*sheet_scale_convert), data["TopRight"]["U"]*sheet_scale_convert)
    size_screen = ((data["TopRight"]["V"] - data["BottomLeft"]["V"])*sheet_scale_convert,
                   (data["TopRight"]["U"] - data["BottomLeft"]["U"])*sheet_scale_convert)

    print(f'data["BottomLeft"]["V"]{data["BottomLeft"]["V"]}')
    print(f'data["BottomLeft"]["U"]{data["BottomLeft"]["U"]}')
    print(f'data["TopRight"]["V"]{data["TopRight"]["V"]}')
    print(f'data["TopRight"]["U"]{data["TopRight"]["U"]}')


    y0 = data["BottomLeft"]["V"]
    x0 = data["BottomLeft"]["U"]


    # print(size_screen)
    sizes_for_boxes = []
    coordinates_obj = []
    id_s = []
    for item in data["Tags"]:
        sizes_for_boxes.append((abs(item["Height"])*sheet_scale_convert, abs(item["Width"])*sheet_scale_convert))
        coordinates_obj.append(((item["LeaderEnd"]["V"] - data["BottomLeft"]["V"])*sheet_scale_convert, (item["LeaderEnd"]["U"] - data["BottomLeft"]["U"])*sheet_scale_convert))
        id_s.append(item["TagId"])
    # print(sizes_for_boxes)
    # print(coordinates_obj)
    # print(data.keys())
    print("________________________________")
    return size_screen, sizes_for_boxes, coordinates_obj, id_s, x0, y0, scale_sheet, data["TopRight"]["V"] - data["BottomLeft"]["V"]


def deserial_funk_for_class(data):

    boxes_array = []
    for item in data["Tags"]:
        dict = {}
        dict["TagId"] = item["TagId"]
        dict["Height"] = item["Height"]
        dict["Width"] = item["Width"]
        dict["LeaderEnd_V"] = item["LeaderEnd"]["V"]
        dict["LeaderEnd_U"] = item["LeaderEnd"]["U"]
        boxes_array.append(dict)

    result = {"TopRight_V": data["TopRight"]["V"],
              "TopRight_U": data["TopRight"]["U"],
              "BottomLeft_V": data["BottomLeft"]["V"],
              "BottomLeft_U": data["BottomLeft"]["U"],
              "Scale": data["Scale"],
              "Boxes_list": boxes_array
              }

    return result

def original_size(V_start, U_start, scale_sheet, data):
    FT_TO_MM = 304.8

    sheet_scale_convert = FT_TO_MM/scale_sheet

    y0 = V_start
    x0 = U_start
    # print(size_screen)
    boxes = []

    for item in data["Boxes_list"]:
        data = {}
        data["Size_of_Box"] = (abs(item["Height"])*sheet_scale_convert, abs(item["Width"])*sheet_scale_convert)
        data["Leader_coordinate"]=((item["LeaderEnd_V"] - y0)*sheet_scale_convert, (item["LeaderEnd_U"] - x0)*sheet_scale_convert)
        data["TagId"] = item["TagId"]
        boxes.append(data)
    # print(sizes_for_boxes)
    # print(coordinates_obj)
    # print(data.keys())
    print("________________________________")
    return boxes

