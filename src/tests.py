"""Tests for horsing around."""
import types

from datetime import date


def test_month_converter():
    """Test month converter helper works."""
    from src.helpers import month_converter
    assert month_converter('December') == '12'


def test_date_range_returns_gen():
    """Test date range function returns gen."""
    from src.pdf_getter import date_range
    dr_gen = date_range(1, 2)
    assert isinstance(dr_gen, types.GeneratorType)


def test_url_gen_returns_gen():
    """Test url_gen function returns gen."""
    from src.pdf_getter import url_gen
    u_gen = url_gen()
    assert isinstance(u_gen, types.GeneratorType)


def test_pdf_to_text_returns_gen():
    """Test pdf_to_text function returns gen."""
    from src.pdf_parser import pdf_to_text
    ptt_gen = pdf_to_text()
    assert isinstance(ptt_gen, types.GeneratorType)


def test_page_parser_returns_gen():
    """Test pdf_to_text function returns gen."""
    from src.pdf_parser import page_parser
    pp_gen = page_parser()
    assert isinstance(pp_gen, types.GeneratorType)


def test_date_range_gen_yields_datetime():
    """Test date_range yields datetime obj."""
    from src.pdf_getter import date_range
    dr_gen = date_range(1, 2)
    assert isinstance(next(dr_gen), date)


def test_url_gen_yields_tuple():
    """Test url_gen yields tuple."""
    from src.pdf_getter import url_gen
    u_gen = url_gen()
    assert isinstance(next(u_gen), tuple)


def test_url_gen_tuple_has_date_obj():
    """Test url_gen yeilds tuple with date obj."""
    from src.pdf_getter import url_gen
    u_gen = url_gen()
    assert isinstance(next(u_gen)[2], date)


def test_pdf_gen_yields_str():
    """Test pdf_gen yields str."""
    from src.helpers import pdf_gen
    p_gen = pdf_gen()
    assert isinstance(next(p_gen), str)


def test_pdf_to_text_yields_str():
    """Test pdf_to_text yields str."""
    from src.pdf_parser import pdf_to_text
    ptt_gen = pdf_to_text()
    assert isinstance(next(ptt_gen), str)


def test_page_parser_yields_dict():
    """Test page_parser yields dict."""
    from src.pdf_parser import page_parser
    pp_gen = page_parser()
    assert isinstance(next(pp_gen), dict)


def test_page_parser_first_result():
    """Test page parser parsers winner correctly."""
    from src.pdf_parser import page_parser
    pp_gen = page_parser()
    assert next(pp_gen)['Winner'] == 'HaitianSensation'
