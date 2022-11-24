import os
import tempfile
import hashlib
import requests
import pytest
from page_loader import download


test_page = {"url": 'https://ru.hexlet.io/courses',
             "local": 'page-stub.html',
             "result": 'expected/page-stub-result.html',
             "expected_name": "ru-hexlet-io-courses.html",
             "expected_assets_directory": "ru-hexlet-io-courses_files"}
test_assets = [
    {"url": 'https://ru.hexlet.io/assets/professions/nodejs.png',
     "local": 'assets/nodejs.png',
     "expected_name": "ru-hexlet-io-assets-professions-nodejs.png"},
    {"url": 'https://ru.hexlet.io/assets/application.css',
     "local": 'assets/application.css',
     "expected_name": "ru-hexlet-io-assets-application.css"},
    {"url": 'https://ru.hexlet.io/packs/js/runtime.js',
     "local": 'assets/runtime.js',
     "expected_name": "ru-hexlet-io-packs-js-runtime.js"},
    {"url": 'https://ru.hexlet.io/courses',
     "local": 'page-stub.html',
     "expected_name": "ru-hexlet-io-courses.html"}
]


def get_fixture_path(local_filename):
    return os.path.join('tests/fixtures', local_filename)


def get_mocked_path(save_location, local_filename):
    return os.path.join(save_location, local_filename)


def get_hash(file_contents):
    return hashlib.md5(file_contents).hexdigest()


def open_file(filename, is_asset=False):
    mode = 'r' if not is_asset else 'rb'
    with open(filename, mode) as file:
        return file.read()


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        page_stub = get_fixture_path(test_page['local'])
        page_expected = get_fixture_path(test_page['result'])
        assets_stub_hash = set()
        assets_mocked_hash = set()
        assets_stub_listdir = set()

        page_stub_content = open_file(page_stub)
        requests_mock.get(test_page['url'], text=page_stub_content)

        for test_asset in test_assets:
            assets_stub_listdir.add(test_asset['expected_name'])
            asset_stub = get_fixture_path(test_asset['local'])
            asset_stub_content = open_file(asset_stub, is_asset=True)
            requests_mock.get(test_asset['url'], content=asset_stub_content)
            asset_stub_hash = get_hash(asset_stub_content)
            assets_stub_hash.add(asset_stub_hash)

        page_mocked = download(test_page['url'], tempdir)
        page_mocked_content = open_file(page_mocked)
        page_expected_content = open_file(page_expected)

        assets_mocked_dir = get_mocked_path(tempdir, test_page['expected_assets_directory'])
        assets_mocked_listdir = set(os.listdir(assets_mocked_dir))
        for asset_mocked in assets_mocked_listdir:
            asset_mocked = get_mocked_path(assets_mocked_dir, asset_mocked)
            asset_mocked_content = open_file(asset_mocked, is_asset=True)
            asset_mocked_hash = get_hash(asset_mocked_content)
            assets_mocked_hash.add(asset_mocked_hash)

        assert page_mocked_content == page_expected_content
        assert test_page['expected_assets_directory'] in os.listdir(tempdir)
        assert assets_mocked_listdir == assets_stub_listdir
        assert assets_mocked_hash == assets_stub_hash


def test_io_errors(requests_mock):
    page_stub = get_fixture_path(test_page['local'])
    page_stub_content = open_file(page_stub)
    requests_mock.get(test_page['url'], text=page_stub_content)

    with pytest.raises(FileNotFoundError):
        download(test_page['url'], '/not_exist_dir')

    with pytest.raises(PermissionError):
        with tempfile.TemporaryDirectory() as temp_dl_dir:
            os.chmod(temp_dl_dir, 400)
            download(test_page['url'], temp_dl_dir)

    with pytest.raises(NotADirectoryError):
        with tempfile.NamedTemporaryFile() as temp_file:
            download(test_page['url'], temp_file.name)


def test_network_errors(requests_mock):
    page_stub = get_fixture_path(test_page['local'])
    page_stub_content = open_file(page_stub)

    with pytest.raises(requests.HTTPError):
        requests_mock.get(test_page['url'], text=page_stub_content, status_code=404)
        with tempfile.TemporaryDirectory() as tempdir:
            download(test_page['url'], tempdir)

    with pytest.raises(requests.Timeout):
        requests_mock.get(test_page['url'], exc=requests.Timeout)
        with tempfile.TemporaryDirectory() as tempdir:
            download(test_page['url'], tempdir)

    with pytest.raises(requests.ConnectionError):
        requests_mock.get(test_page['url'], exc=requests.ConnectionError)
        with tempfile.TemporaryDirectory() as tempdir:
            download(test_page['url'], tempdir)
