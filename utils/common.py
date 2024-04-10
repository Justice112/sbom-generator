def convert_to_name_dict(json_list):
    name_dict = {}
    for entry in json_list:
        name = entry.get('name')
        if name:
            if name not in name_dict:
                name_dict[name] = [entry]
            else:
                name_dict[name].append(entry)
    return name_dict