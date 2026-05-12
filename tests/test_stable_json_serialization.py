from src.pipeline_runner import stable_json_dumps

def test_stable_json_serialization():
    payload = {
        "zeta": 1,
        "alpha": {
            "gamma": 3,
            "beta": 2,
        },
    }

    first = stable_json_dumps(payload)
    second = stable_json_dumps(payload)

    assert first == second

    expected = '''{
  "alpha": {
    "beta": 2,
    "gamma": 3
  },
  "zeta": 1
}'''

    assert first == expected
