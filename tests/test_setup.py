from __future__ import annotations

from pathlib import Path

import pytest
from check_setup import SetupFailure, check_bash_script


@pytest.mark.parametrize(
    ("newline", "extra", "error"),
    [
        ("\n", "", None),
        ("\r\n", "", "contains CRLF"),
        ("\n", "if true; then\n", "invalid syntax"),
    ],
    ids=["valid-lf", "windows-crlf", "invalid-bash"],
)
def test_bash_helper_validation_does_not_execute(
    tmp_path: Path, newline: str, extra: str, error: str | None
) -> None:
    marker = tmp_path / "must-not-exist"
    helper = tmp_path / "task-start"
    source = f'#!/usr/bin/env bash\ntouch "{marker.as_posix()}"\n{extra}'
    helper.write_bytes(source.replace("\n", newline).encode("utf-8"))

    if error is None:
        check_bash_script(helper)
    else:
        with pytest.raises(SetupFailure, match=error):
            check_bash_script(helper)

    assert not marker.exists()
