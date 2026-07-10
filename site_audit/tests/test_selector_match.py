"""Tests for CSS selector matching: class, id, descendant, specificity."""

from site_audit.css_analyzer.selector_match import (
    specificity, parse_element_selector, selector_contains,
    match_selector, find_best_match
)
from site_audit.css_analyzer.source_index import SourceIndex, build_source_index, SelectorEntry
from site_audit.css_analyzer.parser import CSSRule


def test_specificity_id():
    assert specificity("#header") == 100


def test_specificity_class():
    assert specificity(".post-title") == 10


def test_specificity_tag():
    assert specificity("a") == 1


def test_specificity_combined():
    assert specificity("h1.post-title") == 11  # tag(1) + class(10)


def test_specificity_descendant():
    assert specificity(".article .post-title") == 20  # class(10) + class(10)


def test_parse_tag_only():
    assert parse_element_selector("a") == {"tag": "a", "classes": [], "id": ""}


def test_parse_tag_class():
    r = parse_element_selector("li.post-item")
    assert r["tag"] == "li"
    assert "post-item" in r["classes"]


def test_parse_tag_class_id():
    r = parse_element_selector("div#main.content")
    assert r["tag"] == "div"
    assert r["id"] == "main"
    assert "content" in r["classes"]


def test_selector_contains_tag():
    assert selector_contains("a", "a")
    assert selector_contains("a", "a.post-title")


def test_selector_contains_class():
    assert selector_contains(".post-title", "a.post-title")
    assert selector_contains(".post-item", "li.post-item")


def test_selector_contains_id():
    assert selector_contains("#header", "div#header")


def test_selector_contains_descendant():
    assert selector_contains(".article .title", "h1.title")


def test_selector_contains_no_match():
    assert not selector_contains(".header", ".footer")


def test_match_selector_exact():
    matched, spec = match_selector(".post-title", ".post-title")
    assert matched
    assert spec >= 500  # exact match boost


def test_match_selector_class():
    matched, spec = match_selector(".post-item", "li.post-item")
    assert matched
    assert spec >= 20  # 10 (class) + 10 (loose)


def test_match_selector_no():
    matched, _ = match_selector(".header", ".footer")
    assert not matched


def test_find_best_match_simple():
    idx = SourceIndex()
    idx._exact[".post-title"] = SelectorEntry(".post-title", "a.css", 1, {"color": "#888"})
    idx._exact["a"] = SelectorEntry("a", "b.css", 2, {"color": "#333"})
    # Rebuild indices
    idx._by_class[".post-title"].append(idx._exact[".post-title"])
    idx._by_tag["a"].append(idx._exact["a"])

    matches = find_best_match("a.post-title", idx, "color")
    assert len(matches) >= 1
    # .post-title should rank higher than a for a.post-title
    assert matches[0][0].selector == ".post-title"