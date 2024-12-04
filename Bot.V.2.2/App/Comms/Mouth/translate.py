


def extract_structure(data, path: str=[], structure: str=[]):

    if isinstance(data, dict):
        for key, value in data.items():
            extract_structure(value, path + [key], structure)

    elif isinstance(data, list):
        for idx, value in enumerate(data):
            extract_structure(value, path + [idx], structure)
            
    else:
        structure.append(path)

    return structure

def go_to_nested_path(data, path):
        current_level = data

        for key in path:
            if isinstance(current_level, dict):
                if key in current_level:
                    current_level = current_level[key]

            elif isinstance(current_level, list):
                index = int(key)
                current_level = current_level[index]
                    
        return current_level


def substitute_idexes(path, desiredPath):
    typ = path[0]
    match typ:
        case "buttons":
            match len(path):
                case 3:
                    desiredPath[3] = path[1]
                case _:
                    pass 
        case "sections":
            match len(path):
                case 3:
                    desiredPath[4] = path[1]
                case 5:
                    desiredPath[4], desiredPath[6] = path[1], path[3]
        case _:
            pass

    return desiredPath