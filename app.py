import json

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

OPERATOR = ['add', 'sub', 'mul', 'div']
stacks = []

def stack_is_exists(stack_id):
    """
    :param stack_id: the id of the stack to check if it exists
    :return: True if the stack with the specified id exists, False otherwise
    """
    if stack_id >= len(stacks) or stack_id < 0:
        return False

    return True


@app.route('/')
def no_route():
    """
    :return: Response object with "Route not allowed" message, status code 405, and mimetype 'text/plain'
    """
    return Response(
        "Route not allowed", status=405, mimetype='text/plain'
    )


@app.route('/rpn/op', methods= ['GET'])
def list_operator():
    """
    :return: A JSON object containing a list of operators.
    """
    return jsonify({'operators': OPERATOR})


@app.route('/rpn/op/<op>/stack/<int:stack_id>', methods=['POST'])
def apply_operator_on_stack(stack_id, op):
    """
    :param stack_id: ID of the stack on which the operator will be applied
    :param op: Operator to apply on the stack, should be one of ('add', 'sub', 'mul', 'div')
    :return: JSON response with the computed result after applying the operator on the stack
    """
    if not stack_is_exists(stack_id):
        return Response(
            "Stack not found", status=404, mimetype='text/plain'
        )

    if op not in OPERATOR:
        return Response(
            "Operator not allowed", status=403, mimetype='text/plain'
        )

    if len(stacks[stack_id]) < 2:
        return Response(
            "Stack contains only one number", status=403, mimetype='text/plain'
        )

    result = None

    if op == 'add':
        result = stacks[stack_id][-1] + stacks[stack_id][-2]
    elif op == 'sub':
        result = stacks[stack_id][-1] - stacks[stack_id][-2]
    elif op == 'mul':
        result = stacks[stack_id][-1] * stacks[stack_id][-2]
    elif op == 'div':
        result = stacks[stack_id][-1] / stacks[stack_id][-2]

    stacks[stack_id] = stacks[stack_id][:-2]
    stacks[stack_id].append(result)
    return jsonify({'result': result})


@app.route('/rpn/stack/<int:stack_id>', methods=['GET'])
def get_stack(stack_id: int):
    """
    :param stack_id: The unique identifier of the stack to retrieve
    :return: JSON representation of the stack with the given stack_id
    """

    if not stack_is_exists(stack_id):
        return Response(
            "Stack not found", status=404, mimetype='text/plain'
        )
    return jsonify({'id': stack_id, 'mem': stacks[stack_id]})


@app.route('/rpn/stack/<int:stack_id>', methods=['DELETE'])
def delete_stack(stack_id: int):
    """
    :param stack_id: The unique identifier of the stack to delete
    :return: Response object with success message or error message
    """
    if not stack_is_exists(stack_id):
        return Response(
            "Stack not found", status=404, mimetype='text/plain'
        )

    del stacks[stack_id]
    return jsonify({'message': f'Stack {stack_id} deleted successfully'})


@app.route('/rpn/stack/<int:stack_id>', methods=['POST'])
def push_val_in_stack(stack_id: int):
    """
    :param stack_id: integer ID of the stack to push the value into
    :return: JSON response with the updated stack contents
    """
    if not stack_is_exists(stack_id):
        return Response(
            "Stack not found", status=404, mimetype='text/plain'
        )

    data = request.get_json()
    if 'value' not in data:
        return Response(
            "Value key not found in request data", status=400, mimetype='text/plain'
        )

    if not isinstance(data['value'], (int, float)):
        return Response("Invalid value type, must be a number", status=400, mimetype='text/plain')

    stacks[stack_id].append(data['value'])

    return jsonify({'id': stack_id, 'mem': stacks[stack_id]})


@app.route('/rpn/stack', methods= ['GET'])
def list_stack():
    """
    :return: a list of dictionaries containing the stack id and corresponding value
    """
    return_stacks = [{"id": i, "mem": val} for i, val in enumerate(stacks)]

    return jsonify({'stacks': return_stacks})


@app.route('/rpn/stack', methods= ['POST'])
def create_stack():
    """
    :return: This method creates a new stack and appends it to the stacks list.
    """
    stacks.append([])
    stack_id_created = len(stacks) - 1
    return Response(
        json.dumps({'id': stack_id_created}), status=201, mimetype='text/plain'
    )

@app.errorhandler(404)
def page_not_found(e:Exception) -> Response:
    """
    :param e: The exception object that caused the 404 error.
    :return: A Response object with the error message and status code 404.
    """
    return Response(
        f'{request.path} - Not found', status=404
    )


if __name__ == '__main__':
    app.run(debug=True)
