import numpy as np
import traceback

from typing import Any, List
# from Project.graphtaint import getMatchingTemplates
from Project.scanner import scanUserName, scanPasswords, isValidKey
from Project.parser import getValsFromKey, keyMiner

def fuzz(method, fuzzed_args: List[Any]):
    for args in fuzzed_args:
        try:
            result = method(*args)
        except Exception as exc:
            print(f"Fuzz: {method.__name__} Failed")
            traceback.print_exc()
        else:
            print(f"Fuzz: {method.__name__} Passed ({result})")


if __name__ == "__main__":
    fuzz_targets = [
        (
            keyMiner, [
                (None, None),
                (1, 2),
                (1.0, 2.0),
                ([], {}),
                ("bad-filename", "random"),
            ]
        ),
        (
            scanUserName, [
                (None, None),
                ("bad", "args"),
                ([], {}),
                (float("inf"), float("inf")),
                (float("-inf"), float("inf")),
                (1j, 1),
                (np.NAN, np.NAN)
            ]
        ),
        (
            scanPasswords, [
                ([], ""),
                (None, 0),
                (None, 1.0),
                (None, "bad-iterable"),
                (None, [None, None, None]),
                (None, []),
                (None, np.zeros((1, 50))),
            ]
        ),
        (
            isValidKey, [
                (None,),
                (0,),
                (1.0,),
                ([],),
                ({},),
                ("bad-model-name",),
            ]
        ),
        (
            getValsFromKey, [
                (0, 0, None,),
                (None, None, 0,),
                ("doesnt", "matter", 1.0,),
                (float("-inf"), float("inf"), [],),
                ([], [], {},),
                ([], [], "bad-model-name",),
            ]
        )
    ]
    for method, fuzzed_args in fuzz_targets:
        fuzz(method, fuzzed_args)