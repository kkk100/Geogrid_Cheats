import json
import itertools
from colorama import Fore, Style

def get_all_category_names() -> None:
    categories = set()
    for i in range(1, 669):
        with open(f"data/{i}_cdn.json") as f:
            data = json.load(f)
        data1 = data["rows"]
        data2 = data["columns"]
        for row in data1:
            categories.add(row["name"])
        for column in data2:
            categories.add(column["name"])
    print(len(categories))


def get_categories(board_num: int) -> dict[str, list[str]]:
    with open(f"data/{board_num}_cdn.json") as f:
        data = json.load(f)
    rows = data["rows"]
    columns = data["columns"]
    answers = data["answers"]
    category_map = dict()
    category_map[rows[0]["name"]] = answers["match_box_1"] + answers["match_box_2"] + answers["match_box_3"]
    category_map[rows[1]["name"]] = answers["match_box_4"] + answers["match_box_5"] + answers["match_box_6"]
    category_map[rows[2]["name"]] = answers["match_box_7"] + answers["match_box_8"] + answers["match_box_9"]
    category_map[columns[0]["name"]] = answers["match_box_1"] + answers["match_box_4"] + answers["match_box_7"]
    category_map[columns[1]["name"]] = answers["match_box_2"] + answers["match_box_5"] + answers["match_box_8"]
    category_map[columns[2]["name"]] = answers["match_box_3"] + answers["match_box_6"] + answers["match_box_9"]
    return category_map
def get_categories_correct() -> None:
    big_map = dict()
    for i in range (1, 669):
        categories_one = get_categories(i)
        for key, val in categories_one.items():
            if key in big_map.keys():
                for country in val:
                    big_map[key].add(country)
            else:
                big_map[key] = set(val)
    big_map_2 = dict()
    for key, val in big_map.items():
        big_map_2[key] = list(val)
    with open("categories.json", "w", encoding="utf-8") as plik:
        json.dump(big_map_2, plik, ensure_ascii=False, indent=4)
    with open("category_names.json", "w", encoding="utf-8") as plik:
        json.dump(sorted(list(big_map_2.keys())), plik, ensure_ascii=False, indent=4)
def find_crossing(category1:str, category2:str) -> list[tuple[int, int]]:
    #returns board numbers and numbers of square on the board
    boards = []
    for i in range(1, 669):
        with open(f"data/{i}_cdn.json") as f:
            data = json.load(f)
        data1 = data["rows"]
        data2 = data["columns"]
        rows = [row["name"] for row in data1]
        columns = [column["name"] for column in data2]
        square = -1
        if category1 in rows and category2 in columns:
            square = (rows.index(category1) * 3) + columns.index(category2) + 1
        elif category2 in rows and category1 in columns:
            square = (rows.index(category2) * 3) + columns.index(category1) + 1
        if square != -1:
            boards.append([i, square])
    return boards
def find_crossing_single(category: str) -> list[tuple[int, int]]:
    boards = []
    for i in range(1, 669):
        with open(f"data/{i}_cdn.json") as f:
            data = json.load(f)
        data1 = data["rows"]
        data2 = data["columns"]
        rows = [row["name"] for row in data1]
        columns = [column["name"] for column in data2]
        if category in rows:
            idx = rows.index(category)
            for field in range(idx*3, idx*3+3):
                boards.append([i, field + 1])
        if category in columns:
            idx = columns.index(category)
            for field in range(0, 7, 3):
                boards.append([i, field + idx + 1])
    return boards

def find_rarest(category1:str = "", category2:str = "") -> list[str]:
    rarest = []
    if category1 and category2:
        boards = find_crossing(category1, category2)
    elif category1:
        boards = find_crossing_single(category1)
    elif category2:
        boards = find_crossing_single(category2)
    else:
        boards = []
    for board in boards:
        with open(f"data/{board[0]}_api.json") as f:
            data = json.load(f)
        posible_rarest = data[f"match_box_{board[1]}"]
        least_count = 10000000000000000
        temp_rarest = []
        for country, count in posible_rarest.items():
            if count == least_count:
                temp_rarest.append(country)
            elif (count < least_count) and count > 1:
                temp_rarest.clear()
                temp_rarest.append(country)
                least_count = count
        rarest += temp_rarest

    return rarest
def determine_rarest(category1:str, category2:str) -> tuple[list[str], int]:
    rarest = find_rarest(category1, category2)
    if rarest:
        return rarest, 0
    temp1 = set(find_rarest(category1))
    temp2 = set(find_rarest(category2))
    combined = temp1 & temp2
    if combined:
        return list(combined), 1
    else:
        return [], 2


def get_all_rarest() -> None:
    with open("category_names.json", "r", encoding="utf-8") as plik:
        data = json.load(plik)
    for pair in itertools.combinations(data, 2):
        rarest_dict = dict()
        key = tuple(pair)
        rarest = determine_rarest(key[0], key[1])
        rarest_dict[key] = rarest
def search_category(category: str) -> list[int]:
    result = []
    for i in range(1, 669):
        with open(f"data/{i}_cdn.json") as f:
            data = json.load(f)
        data1 = data["rows"]
        data2 = data["columns"]
        rows = [row["name"] for row in data1]
        columns = [column["name"] for column in data2]
        if (category in rows) or (category in columns):
            result.append(i)
            continue
    return result
def get_correct_answers(category1: str, category2: str) -> list[str]:
    with open("categories.json", "r", encoding="utf-8") as plik:
        data = json.load(plik)
    set1 = set(data[category1])
    set2 = set(data[category2])
    result = sorted(list(set1.intersection(set2)))
    return result
def rainbow(text:str) -> str:
    raibow = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA,
    ]
    result = ""
    for i, char in enumerate(text):
        color = raibow[i % len(raibow)]
        result += color + char
    return result + Style.RESET_ALL
if __name__ == "__main__":
    print(search_category("Flag with black"))
    print(determine_rarest("Flag with black", "Fewer than 10 Olympic medals"))