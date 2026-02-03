import json


def get_all_category_names() -> None:
    category_groups = set()
    category_names = set()
    for i in range(1, 669):
        with open(f"data/{i}_cdn.json") as f:
            data = json.load(f)
        data1 = data["rows"]
        data2 = data["columns"]
        for row in data1:
            category_groups.add(row["id"])
            category_names.add(row["name"])
        for column in data2:
            category_groups.add(column["id"])
            category_names.add(column["name"])
    category_names = sorted(list(category_names))
    category_groups = sorted(list(category_groups))
    for group in category_groups:
        print(group)
    print("\n\n\n\n\n\n\n\n\n")
    for name in category_names:
        print(name)


get_all_category_names()
