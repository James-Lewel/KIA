meals_dictionary = {
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
    1: {'lunch': [], 'dinner': []},
    2: {'lunch': [], 'dinner': []},
    3: {'lunch': [], 'dinner': []},
    4: {'lunch': [], 'dinner': []},
    5: {'lunch': [81, 34, 33], 'dinner': [38, 37, 15, 39]},
    6: {'lunch': [41, 40, 23, 42], 'dinner': [44, 45, 31, 5]},
    7: {'lunch': [46, 47, 11, 48], 'dinner': [49, 51, 18, 50]},
    8: {'lunch': [], 'dinner': []},
    9: {'lunch': [], 'dinner': []},
    10: {'lunch': [], 'dinner': []},
    11: {'lunch': [], 'dinner': []},
    12: {'lunch': [], 'dinner': []},
    13: {'lunch': [], 'dinner': []},
    14: {'lunch': [], 'dinner': []},
    15: {'lunch': [], 'dinner': []},
    16: {'lunch': [], 'dinner': []},
    17: {'lunch': [], 'dinner': []},
    18: {'lunch': [], 'dinner': []},
    19: {'lunch': [], 'dinner': []},
    20: {'lunch': [], 'dinner': []},
    21: {'lunch': [], 'dinner': []},
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
    