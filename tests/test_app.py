import json

import app

def test_no_route_endpoint(client):
    response = client.get('/')
    assert response.status_code == 405
    assert response.data == b"Route not allowed"


def test_list_operator(client):
    response = client.get('/rpn/op')
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert 'operators' in data
    assert data['operators'] == app.OPERATOR

def call_stack_list(client):
    response = client.get('/rpn/stack')
    assert response.status_code == 200

    return json.loads(response.data)

def test_list_stack(client):
    response_data = call_stack_list(client)
    assert 'stacks' in response_data

def create_new_stack(client):
    response = client.post('/rpn/stack')
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'id' in response_data

    return response_data['id']


def test_create_stack(client):
    response_data = call_stack_list(client)
    assert 'stacks' in response_data
    initial_stack_length = len(response_data['stacks'])

    create_new_stack(client)

    response_data = call_stack_list(client)
    assert 'stacks' in response_data
    assert 'id' in response_data['stacks'][0]
    assert 'mem' in response_data['stacks'][0]
    new_stack_length = len(response_data['stacks'])

    assert initial_stack_length + 1 == new_stack_length

def test_get_stack_by_id(client):
    last_id = create_new_stack(client)

    response = client.get(f'/rpn/stack/{last_id}')
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert 'id' in response_data
    assert 'mem' in response_data

def test_get_bad_stack(client):
    response = client.get('/rpn/stack/890')
    assert response.status_code == 404

def test_delete_stack_by_id(client):
    last_stack_id = create_new_stack(client)

    response = client.delete(f"/rpn/stack/{last_stack_id}")
    assert response.status_code == 200

def test_delete_bad_stack(client):

    bad_stack_id = 679

    response = client.delete(f"/rpn/stack/{bad_stack_id}")
    assert response.status_code == 404

def test_push_value_in_stack(client):
    last_stack_id = create_new_stack(client)

    bad_key_body = {'data':42}

    response = client.post(f"/rpn/stack/{last_stack_id}", json=bad_key_body, content_type='application/json')
    assert response.status_code == 400

    bad_type_body = {'value': 'abc'}

    response = client.post(f"/rpn/stack/{last_stack_id}", json=bad_type_body, content_type='application/json')
    assert response.status_code == 400

    good_body = {'value': 42}

    response = client.post(f"/rpn/stack/{last_stack_id}", json=good_body, content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert 'id' in response_data
    assert 'mem' in response_data
    assert response_data['mem'][0] == 42

    response = client.post(f"/rpn/stack/{last_stack_id}", json=good_body, content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert len(response_data['mem']) == 2
    assert response_data['mem'][1] == 42

def push_data_to_stack(client, stack_id, value):
    body = {'value': value}
    response = client.post(f"/rpn/stack/{stack_id}", json=body, content_type='application/json')
    assert response.status_code == 200
    return json.loads(response.data)

def test_process_operand(client):
    last_stack_id = create_new_stack(client)

    init_values = [10, 5, 6, 8, 9]
    expected_result = 5.5

    for value in init_values:
        push_data_to_stack(client, last_stack_id, value)

    response = client.get(f'/rpn/stack/{last_stack_id}')
    assert response.status_code == 200

    response_data = json.loads(response.data)
    assert response_data['mem'] == init_values

    op_response = None
    for op in app.OPERATOR:
        op_response = client.post(f"/rpn/op/{op}/stack/{last_stack_id}")
        assert op_response.status_code == 200

    op_response = json.loads(op_response.data)
    assert "result" in op_response
    assert op_response['result'] == expected_result

def test_process_bad_operator(client):
    last_stack_id = create_new_stack(client)

    init_values = [10, 5]

    for value in init_values:
        push_data_to_stack(client, last_stack_id, value)

    op = 'sqrt'
    op_response = client.post(f"/rpn/op/{op}/stack/{last_stack_id}")
    assert op_response.status_code == 403
    assert op_response.data == b"Operator not allowed"

def test_process_operand_bad_stack(client):
    bad_stack_id = 679

    op = 'div'
    op_response = client.post(f"/rpn/op/{op}/stack/{bad_stack_id}")
    assert op_response.status_code == 404
    assert op_response.data == b"Stack not found"

def test_process_operand_single_elem(client):
    last_stack_id = create_new_stack(client)
    push_data_to_stack(client, last_stack_id, 8)

    op = 'add'
    op_response = client.post(f"/rpn/op/{op}/stack/{last_stack_id}")
    assert op_response.status_code == 403
    assert op_response.data == b"Stack contains only one number"
