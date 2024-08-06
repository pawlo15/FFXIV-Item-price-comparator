import json
import requests
import csv
import argparse
from typing import List, TypeVar, Optional


_path = "https://universalis.app/api/v2"
T = TypeVar('T')


class PriceData:
    def __init__(self, price: float, worldId: int, dataCenter: str = 'None', worldName: str = 'None'):
        self.price = price
        self.worldId = worldId
        self.worldName = worldName
        self.dataCenter = dataCenter


class ItemInfo:
    def __init__(self, itemId: int, dc: PriceData, region: PriceData, itemName: str = 'None'):
        self.itemId = itemId
        self.dc = [dc]
        self.region = region
        self.Name = itemName


class World:
    def __init__(self, id: int, name: str = 'Unknown'):
        self.id = id
        self.name = name


class DataCenter:
    def __init__(self, name: str, region: str, worlds: List[int]):
        self.name = name
        self.region = region
        self.worlds = [World(world_id) for world_id in worlds]


class CsvItem:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


def parse_json(data: dict, data_center: str) -> List[ItemInfo]:
    result = []
    try:
        for item in data.get('results', []):
            dc_data = item['nq']['minListing']['dc']
            region_data = item['nq']['minListing']['region']

            dc = PriceData(price=dc_data['price'], worldId=dc_data['worldId'], dataCenter=data_center)
            region = PriceData(price=region_data['price'], worldId=region_data['worldId'])

            item_info = ItemInfo(itemId=item['itemId'], dc=dc, region=region)
            result.append(item_info)
    finally:
        return result


def get_data_centers(region: str):
    path = f'{_path}/data-centers'
    response = requests.get(path)

    data_centers = [DataCenter(**item) for item in json.loads(response.content)]
    data_centers = [dc for dc in data_centers if dc.region == region]

    worlds = get_worlds()

    for data_center in data_centers:
        for world in data_center.worlds:
            world_name = get_world_name_by_id(worlds, world.id)
            if world_name is not None:
                world.name = world_name
    return data_centers


def get_worlds():
    path = f'{_path}/worlds'
    response = requests.get(path)
    result = [World(**item) for item in json.loads(response.content)]
    return [item for item in result if item.id]


def get_item_info(dc: str, item_ids: [int]):
    items = ''
    for id in item_ids:
        items = items + f'{id},'
    path = f'{_path}/aggregated/{dc}/{items}'
    response = requests.get(path)
    if response.status_code == 200:
        return parse_json(json.loads(response.content), dc)
    return None


def find_by_id(objects: List[T], id: int, id_attr: str, return_attr: Optional[str] = None) -> Optional[str]:
    for obj in objects:
        if getattr(obj, id_attr) == id:
            return getattr(obj, return_attr) if return_attr else obj
    return None


def get_world_name_by_id(worlds: List[World], id: int) -> Optional[str]:
    return find_by_id(worlds, id, 'id', 'name')


def find_object_by_id(objects: List[ItemInfo], id: int) -> Optional[ItemInfo]:
    return find_by_id(objects, id, 'itemId')


def find_item_by_id(items: List[CsvItem], id: int) -> Optional[str]:
    return find_by_id(items, id, 'id', 'name')


def load_csv(filename: str) -> List[CsvItem]:
    items = []
    with open(filename, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = CsvItem(id=int(row["id"]), name=row["name"])
            items.append(item)
    return items


def print_result(objects: List[ItemInfo], region: str):
    for item in objects:
        print('------------------------------')
        print(f'Item: {item.Name} (ID: {item.itemId})')
        print(f'Region ({region}): {item.region.price} | {item.region.worldName}')
        print(f'Data center:')
        for dc in item.dc:
            print(f'\t{dc.dataCenter}:\t{dc.price}\t| {dc.worldName}')


def price_comparator(region: str, csv: str) -> List[ItemInfo]:
    search_items = load_csv(csv)
    data_centers = get_data_centers(region)

    worlds = [world for dc in data_centers for world in dc.worlds]
    item_ids = [item.id for item in search_items]
    result = []

    for data_center in data_centers:
        data = get_item_info(data_center.name, item_ids)

        for obj in data:
            existing_item = find_object_by_id(result, obj.itemId)
            if existing_item:
                existing_item.dc.append(obj.dc[0])
                if(obj.dc[0].worldId == existing_item.region.worldId):
                    existing_item.region.dataCenter = obj.dc[0].dataCenter
            else:
                obj.Name = find_item_by_id(search_items, obj.itemId)
                obj.region.dataCenter = obj.dc[0].dataCenter
                result.append(obj)

    for item in result:
        item.region.worldName = get_world_name_by_id(worlds, item.region.worldId)
        for dc in item.dc:
            dc.worldName = get_world_name_by_id(worlds, dc.worldId)
    return result


def main():
    parser = argparse.ArgumentParser(description="Process data from a CSV file for a specific region.")
    parser.add_argument('--region', type=str, required=True, help='Name of the region to process')
    parser.add_argument('--file', type=str, required=True, help='Path to the CSV file containing the data')

    args = parser.parse_args()
    result = price_comparator(args.region, args.file)
    print_result(result, args.region)


if __name__ == "__main__":
    main()
