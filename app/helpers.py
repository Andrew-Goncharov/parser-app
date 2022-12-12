import uuid


def get_urls(all_data: list[dict]) -> list[str]:
    urls = []

    for row in all_data:
        urls.append(row["img_url"])

    return urls


def remove_duplicates(all_data: list[dict], parsed_images: list[str]) -> list[str]:
    if not all_data:
        return parsed_images

    saved_urls = get_urls(all_data)

    return list(set(parsed_images) - set(saved_urls))


def map_img_url(images: list[str]) -> list[dict]:
    result_map = []

    for img_url in images:
        result_map.append({"id_uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, img_url)), "img_url": img_url})

    return result_map


def calculate_interval(id: int, max_id: int) -> tuple[int, int]:
    assert ((id >= 1) and (id <= max_id)), "ID validation failed"

    start_id = 12 * id - 11     # (id - 1) * 12
    end_id = 12 * id            # start_id + 11

    return start_id, end_id


def calculate_pagination(id: int, max_id: int) -> list[int]:
    numbers = []

    if 1 <= id <= 5:
        numbers = [i for i in range(1, 6)]
    elif id < max_id - 5:
        numbers = [i for i in range(id - 4, id + 1)]
    elif max_id - 1 <= id <= max_id:
        numbers = [i for i in range(max_id - 5, max_id + 1)]

    return numbers
