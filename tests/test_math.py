import math
import random

import pytest
from sqlalchemy.sql import select

from conesearch_alchemy import math as sql_math


@pytest.mark.parametrize("name", ["cos", "sin", "tan"])
def test_trig_function_radians(name, session):
    """Test trig functions that expect radians."""
    angle = random.uniform(-math.pi, math.pi)
    func = getattr(math, name)
    sql_func = getattr(sql_math, name)
    ((result,),) = session.execute(select(sql_func(angle)))
    assert result == pytest.approx(func(angle))


@pytest.mark.parametrize("name", ["cos", "sin", "tan"])
def test_trig_function_degrees(name, session):
    """Test trig functions that expect degrees."""
    angle = random.uniform(-180, 180)
    func = getattr(math, name)
    sql_func = getattr(sql_math, f"{name}d")
    ((result,),) = session.execute(select(sql_func(angle)))
    assert result == pytest.approx(func(angle * math.pi / 180))
