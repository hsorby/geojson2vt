import os

import pytest

from geojson2vt.geojson2vt import geojson2vt
from geojson2vt.utils import current_dir, get_json


@pytest.mark.parametrize("input_file,expected_file,options", [
    # ('us-states.json', 'us-states-tiles.json',
    #  {'indexMaxZoom': 7, 'indexMaxPoints': 200}),
    # ('dateline.json', 'dateline-tiles.json',
    #  {'indexMaxZoom': 0, 'indexMaxPoints': 10000}),
    # ('dateline.json', 'dateline-metrics-tiles.json',
    #  {'indexMaxZoom': 0, 'indexMaxPoints': 10000, 'lineMetrics': True}),
    # ('feature.json', 'feature-tiles.json',
    #  {'indexMaxZoom': 0, 'indexMaxPoints': 10000}),
    # ('collection.json', 'collection-tiles.json',
    #  {'indexMaxZoom': 0, 'indexMaxPoints': 10000}),
    ('single-geom.json', 'single-geom-tiles.json',
     {'indexMaxZoom': 0, 'indexMaxPoints': 10000}),
    # ('ids.json', 'ids-promote-id-tiles.json',
    #  {'indexMaxZoom': 0, 'promoteId': 'prop0', 'indexMaxPoints': 10000}),
    # ('ids.json', 'ids-generate-id-tiles.json',
    #  {'indexMaxZoom': 0, 'generateId': True, 'indexMaxPoints': 10000})
])
def test_tiles(input_file, expected_file, options):
    cur_dir = current_dir(__file__)
    file_path = os.path.join(cur_dir, f'fixtures/{expected_file}')
    expected = get_json(file_path)

    file_path = os.path.join(cur_dir, f'fixtures/{input_file}')
    input_data = get_json(file_path)

    tiles = gen_tiles(input_data, options)
    for t, j in zip(tiles.items(), expected.items()):
        assert t == j


def test_empty_geojson():
    cur_dir = current_dir(__file__)
    file_path = os.path.join(cur_dir, 'fixtures/empty.json')
    expected = get_json(file_path)
    result = gen_tiles(expected, {})

    assert {} == result


def test_none_geometry():
    cur_dir = current_dir(__file__)
    file_path = os.path.join(cur_dir, 'fixtures/feature-null-geometry.json')
    expected = get_json(file_path)

    assert {} == gen_tiles(expected, {})


def test_invalid_geo_json():
    with pytest.raises(Exception):
        gen_tiles({'type': 'Polygon'}, {})


def gen_tiles(data, options):
    geo_json_vt = geojson2vt(data, options)

    output = {}

    for id_ in geo_json_vt.tiles:
        tile = geo_json_vt.tiles[id_]
        z = tile.get('z')
        output[f'z{z}-{tile.get("x")}-{tile.get("y")}'] = geo_json_vt.get_tile(
            z, tile.get('x'), tile.get('y')).get('features')
    return output


if __name__ == "__main__":
    test_tiles('dateline.json', 'dateline-tiles.json',
               {'indexMaxZoom': 0, 'indexMaxPoints': 10000})
