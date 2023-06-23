from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

teacher = {
    'teacher_name': 'test',
    'faculty': 'test',
}
teacher_id = ''
teacher_name = ''

def test_create_teacher():
    response = client.post(
        '/teachers/add_teacher',
        data=teacher
    )
    teacher_data = response.json()
    global teacher_id
    global teacher_name
    teacher_id = teacher_data['id']
    teacher_name = teacher_data['teacher_name']
    faculty = teacher_data['faculty']
    assert response.status_code == 201
    assert teacher_name == 'test'
    assert faculty == 'test'
    response = client.post(
        '/teachers/add_teacher',
        data=teacher
    )
    assert response.status_code == 409



def test_delete_teacher():
    response = client.delete(f'/teachers/{teacher_id}')
    assert response.status_code == 204
