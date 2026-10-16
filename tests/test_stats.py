import stats as st
import pytest as pt 

def test_generate_stat():
    assert st.generate_stat({}, {})

def test_print_stat():
    assert st.print_stat({})


