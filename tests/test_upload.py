from application.services import dataset_services as ds

def test_read(session):
    json = {"path": "SolidCake98/EMI", "pos":0}
    path_struct = ds.DataSetPathStructure(json)

    code, result = path_struct.read()

    assert result['dir'][0]['name'] == 'emii.smp28'

def test_read_with_dirs(session):
    json = {"path": "SolidCake98/ChinesMnist", "pos":0}
    path_struct = ds.DataSetPathStructure(json)

    code, result = path_struct.read()

    assert result['dir'][0]['name'] == 'data'

def test_not_valid_read(session):
    json_new = {"path": "SolidCake98/EM", "pos":0}
    path_struct_new = ds.DataSetPathStructure(json_new)
    code, result = path_struct_new.read()

    assert code == 404

def test_download(session):
    path = "SolidCake98/EMI"
    downloader = ds.DataSetDownloadService()
    code, result = downloader.download(path)
    assert code == 200

def test_download_not_found(session):
    path = "SolidCake98/EM"
    downloader = ds.DataSetDownloadService()
    code, result = downloader.download(path)
    assert code == 404

