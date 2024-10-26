### Testing:
`pytest -v tests/`

```bash
=========================================================================== test session starts ============================================================================
platform darwin -- Python 3.11.8, pytest-8.3.3, pluggy-1.5.0 -- /Users/g.giallonardi/PycharmProjects/kata_api_rpn/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/g.giallonardi/PycharmProjects/kata_api_rpn
plugins: cov-5.0.0
collected 13 items                                                                                                                                                         

tests/test_app.py::test_no_route_endpoint PASSED                                                                                                                     [  7%]
tests/test_app.py::test_list_operator PASSED                                                                                                                         [ 15%]
tests/test_app.py::test_list_stack PASSED                                                                                                                            [ 23%]
tests/test_app.py::test_create_stack PASSED                                                                                                                          [ 30%]
tests/test_app.py::test_get_stack_by_id PASSED                                                                                                                       [ 38%]
tests/test_app.py::test_get_bad_stack PASSED                                                                                                                         [ 46%]
tests/test_app.py::test_delete_stack_by_id PASSED                                                                                                                    [ 53%]
tests/test_app.py::test_delete_bad_stack PASSED                                                                                                                      [ 61%]
tests/test_app.py::test_push_value_in_stack PASSED                                                                                                                   [ 69%]
tests/test_app.py::test_process_operand PASSED                                                                                                                       [ 76%]
tests/test_app.py::test_process_bad_operator PASSED                                                                                                                  [ 84%]
tests/test_app.py::test_process_operand_bad_stack PASSED                                                                                                             [ 92%]
tests/test_app.py::test_process_operand_single_elem PASSED                                                                                                           [100%]

============================================================================ 13 passed in 0.02s ============================================================================
```

### Code coverage:
`pytest --cov=app tests/`

```bash
=========================================================================== test session starts ============================================================================
platform darwin -- Python 3.11.8, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/g.giallonardi/PycharmProjects/kata_api_rpn
plugins: cov-5.0.0
collected 13 items                                                                                                                                                         

tests/test_app.py .............                                                                                                                                      [100%]

---------- coverage: platform darwin, python 3.11.8-final-0 ----------
Name     Stmts   Miss  Cover
----------------------------
app.py      71      3    96%
----------------------------
TOTAL       71      3    96%


============================================================================ 13 passed in 0.06s ============================================================================
```