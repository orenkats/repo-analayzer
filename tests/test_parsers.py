import pytest
from src.analyzers.parsers.language_parsers import (
    PythonParser,
    JavaScriptParser,
    DotNetParser,
    CppParser,
    JavaParser,
)

@pytest.mark.parametrize(
    "parser_class,content,expected_deps",
    [
        (PythonParser, "import os\nimport sys", ["os", "sys"]),
        (JavaScriptParser, "import React from 'react';", ["React"]),
        (DotNetParser, "using System;\nusing System.Collections.Generic;", ["System", "System.Collections.Generic"]),
        (CppParser, "#include <iostream>\n#include \"custom.h\"", ["iostream", "custom.h"]),
        (JavaParser, "import java.util.List;\nimport java.io.File;", ["java.util.List", "java.io.File"]),
    ],
)
def test_parsers(parser_class, content, expected_deps):
    """
    Test all parsers with sample content and expected dependencies.
    """
    parser = parser_class()
    dependencies = parser.parse(content)
    assert sorted(dependencies) == sorted(expected_deps)
