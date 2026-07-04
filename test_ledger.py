from ledger import (add_entry, average, find_by_desc, init_db, is_within_budget,
                    last_n, page, split_bill, total)


def test_total():
    assert total([{"desc": "a", "amount": 2.0}, {"desc": "b", "amount": 3.0}]) == 5.0


def test_last_n_returns_newest():
    entries = [{"desc": str(i), "amount": 1.0} for i in range(5)]
    assert last_n(entries, 2) == entries[-2:]


def test_total_skips_none_amounts():
    assert total([{"desc": "a", "amount": 2.0}, {"desc": "pending", "amount": None}]) == 2.0


def test_average_empty_ledger_is_zero():
    assert average([]) == 0


def test_find_by_desc_is_injection_safe():
    db = init_db()
    db.execute("INSERT INTO entries VALUES ('coffee', 3.5)")
    db.execute("INSERT INTO entries VALUES ('tea', 2.0)")
    assert find_by_desc(db, "coffee") == [("coffee", 3.5)]
    assert find_by_desc(db, "x' OR '1'='1") == []  # injection must not dump the table


def test_is_within_budget_boundary():
    assert is_within_budget(100, 100) is True  # spending exactly the limit is within budget


def test_add_entry_does_not_share_state():
    add_entry({"desc": "a", "amount": 1.0})
    second = add_entry({"desc": "b", "amount": 2.0})
    assert len(second) == 1  # each call must start from an empty ledger


def test_split_bill_keeps_cents():
    assert split_bill(10.0, 4) == 2.5


def test_page_is_one_based():
    entries = list(range(10))
    assert page(entries, 1, 3) == [0, 1, 2]
    assert page(entries, 2, 3) == [3, 4, 5]
