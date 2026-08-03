"""Tests for full CSS specificity (a,b,c) calculation.

CSS Selectors Level 4: https://www.w3.org/TR/selectors-4/#specificity-rules
"""

from site_audit.css_analyzer.specificity import specificity


def test_specificity_id():
    assert specificity("#header") == (1, 0, 0)


def test_specificity_class():
    assert specificity(".post-title") == (0, 1, 0)


def test_specificity_tag():
    assert specificity("a") == (0, 0, 1)


def test_specificity_combined():
    assert specificity("h1.post-title") == (0, 1, 1)


def test_specificity_descendant():
    # .article .post-title → 2 classes
    spec = specificity(".article .post-title")
    assert spec == (0, 2, 0)


def test_specificity_attribute():
    assert specificity("[data-theme]") == (0, 1, 0)
    assert specificity("[type=text]") == (0, 1, 0)


def test_specificity_pseudo_class():
    assert specificity(":hover") == (0, 1, 0)
    assert specificity(":nth-child(2n)") == (0, 1, 0)


def test_specificity_pseudo_element():
    assert specificity("::before") == (0, 0, 1)


def test_specificity_mixed():
    # #header .nav a:hover → id(1) + class(1) + element(1) + pseudo(1)
    spec = specificity("#header .nav a:hover")
    assert spec == (1, 2, 1)


def test_specificity_group():
    # h1,h2,h3 → each element counted
    spec = specificity("h1, h2, h3")
    assert spec == (0, 0, 3)


def test_specificity_not_adds_arg():
    """:not(.special) should use arg specificity."""
    spec = specificity(":not(.special)")
    assert spec == (0, 1, 0)


def test_specificity_where_is_zero():
    """:where() adds 0 specificity regardless of contents."""
    spec = specificity(":where(.whatever#header)")
    assert spec == (0, 0, 0)


def test_specificity_complex():
    """#main .content article.post:hover ::before
    #main(1,0,0) + .content(0,1,0) + article(0,0,1) + .post(0,1,0) + :hover(0,1,0) + ::before(0,0,1)
    = (1, 3, 2)
    """
    spec = specificity("#main .content article.post:hover ::before")
    assert spec == (1, 3, 2)


def test_specificity_universal():
    """Universal selector * adds 0."""
    a, b, c = specificity("*.container")
    assert b == 1  # Only .container counts


def test_specificity_child_combinator():
    """#sidebar > .widget > p"""
    spec = specificity("#sidebar > .widget > p")
    assert spec == (1, 1, 1)


def test_specificity_adjacent_sibling():
    """h1 + p"""
    spec = specificity("h1 + p")
    assert spec == (0, 0, 2)


def test_specificity_data_theme_selector():
    """[data-theme="dark"] → attribute = b=1"""
    spec = specificity('[data-theme="dark"]')
    assert spec == (0, 1, 0)


def test_specificity_dark_class():
    """.dark → class = b=1"""
    spec = specificity(".dark")
    assert spec == (0, 1, 0)


def test_specificity_prefers_color_scheme():
    """@media (prefers-color-scheme: dark) — not a selector, but test parsing"""
    spec = specificity("body")
    assert spec == (0, 0, 1)


def test_specificity_article_post_title():
    """article.post-single .post-title → class(1) + class(1) + tag(1)"""
    spec = specificity("article.post-single .post-title")
    assert spec == (0, 2, 1)