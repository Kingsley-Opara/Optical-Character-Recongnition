import pathlib
from OCR.main import app, BASE_DIR
from fastapi.testclient import TestClient


client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
img = str(BASE_DIR/'fastcare.png')
def test_imgae_upload():
    UPLOAD_DIR = BASE_DIR/'uploads'
    
    # for path in img.glob('*'):
    with open(img, 'rb') as f:
        data = f.read()
    response = client.post('/upload', files={'file': data})
    assert response.status_code == 200
    print(response.headers)
    # print(path.suffix)
    # ftext = str(path.suffix).replace('.', '')
    assert 'jpg' in response.headers['content-type']
