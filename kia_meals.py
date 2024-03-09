meals_dictionary = {
    -1: ['', 'side'],
    5: ['炒海茸', 'side'],
    11: ['莧菜', 'side'],
    15: ['油菜', 'side'],
    18: ['地瓜葉', 'side'],
    23: ['空心菜', 'side'],
    31: ['尼龍菜', 'side'],
    33: ['炒大陸妹', 'side'],
    34: ['麻婆豆腐', 'side'],
    37: ['毛豆雞丁', 'side'],
    38: ['樹子蒸圓鱈', 'main'],
    39: ['蠔油金針菇', 'side'],
    40: ['海帶芽炒蛋', 'side'],
    41: ['烤紅糟里肌', 'main'],
    42: ['照燒南瓜', 'side'],
    44: ['薑汁味增滷雞排', 'main'],
    45: ['蔥爆肉絲', 'side'],   
    46: ['煎紅尾冬魚', 'main'],
    47: ['義式香料燉雞', 'side'],
    48: ['滷白蘿蔔', 'side'],
    49: ['豆鼓小排', 'main'],
    50: ['紅仁玉米筍', 'side'],
    51: ['韭菜炒甜不辣', 'side'],
    81: ['迷迭香烤雞排', 'main']
}

days_dictionary = {
    1: {'lunch': [3, 2, 88, 1], 'dinner': [6, 7, 55, 5]},
    2: {'lunch': [2, 9, 59, 11], 'dinner': [17, 13, 15, 14]},
    3: {'lunch': [], 'dinner': []},
    4: {'lunch': [], 'dinner': []},
    5: {'lunch': [81, 34, 33, 35], 'dinner': [38, 37, 15, 39]},
    6: {'lunch': [41, 40, 23, 42], 'dinner': [44, 45, 31, 5]},
    7: {'lunch': [46, 47, 11, 48], 'dinner': [49, 51, 18, 50]},
    8: {'lunch': [54, 52, 1, 53], 'dinner': [58, 57, 56, 25]},
    9: {'lunch': [6, 60, 15, 59], 'dinner': [24, 62, 33, 61]},
    10: {'lunch': [17, 63, 11, 66], 'dinner': [67, 68, 18, 69]},
    11: {'lunch': [71, 70, 1, 50], 'dinner': [74, 73, 23, 72]},
    12: {'lunch': [49, 75, 55, 76], 'dinner': [77, 13, 33, 29]},
    13: {'lunch': [100, 78, 18, 79], 'dinner': [81, 83, 15, 82]},
    14: {'lunch': [84, 85, 1, 86], 'dinner': [74, 87, 11, 5]},
    15: {'lunch': [89, 90, 33, 88], 'dinner': [112, 91, 15, 50]},
    16: {'lunch': [24, 93, 11, 94], 'dinner': [95, 96, 97, 25]},
    17: {'lunch': [100, 45, 55, 98], 'dinner': [44, 101, 1, 102]},
    18: {'lunch': [104, 103, 18, 105], 'dinner': [107, 106, 15, 66]},
    19: {'lunch': [58, 109, 97, 110], 'dinner': [112, 111, 31, 42]},
    20: {'lunch': [36, 62, 23, 53], 'dinner': [46, 115, 11, 119]},
    21: {'lunch': [49, 35, 18, 116], 'dinner': [71, 118, 33, 117]},
}

def format_meal(meal_id, meal_info):
    meal_name, meal_type = meal_info
    return f"{meal_id} - - - {meal_type}"

def get_meals():
    formatted_meals = [format_meal(meal_id, meal_info) for meal_id, meal_info in meals_dictionary.items()]
    return formatted_meals

def get_meal(meal_day=None, meal_time=None):
    if meal_day not in days_dictionary:
        return "Missing day" if meal_day is None else "Invalid day"
    
    if meal_time not in ['lunch', 'dinner', 'all']:
        return "Missing time" if meal_time is None else "Invalid time"

    if meal_time == 'all':
        all_meals = [meal_id for time in ['lunch', 'dinner'] if time in days_dictionary[meal_day] for meal_id in days_dictionary[meal_day][time]]
    else:
        all_meals = days_dictionary[meal_day].get(meal_time, [])
        
    return [format_meal(meal_id, meals_dictionary.get(meal_id)) for meal_id in all_meals]

def get_custom_meal(meal_list=[]):
    if not meal_list:
        return "Invalid meal list"
    return [format_meal(meal_id, meals_dictionary.get(meal_id)) for meal_id in meal_list]
    