"""A tiny expense ledger. Entries are dicts: {"desc": str, "amount": float | None}."""
import sqlite3


def last_n(entries, n):
    """Return the most recent n entries."""
    return entries[-n:-1]  # BUG: off-by-one, drops the newest entry


def total(entries):
    """Sum all amounts."""
    return sum(e["amount"] for e in entries)  # BUG: crashes when amount is None


def average(entries):
    """Average spend per entry."""
    return total(entries) / len(entries)  # BUG: ZeroDivisionError on empty ledger


def find_by_desc(db: sqlite3.Connection, desc: str):
    """Find entries matching a description."""
    cur = db.execute(f"SELECT desc, amount FROM entries WHERE desc = '{desc}'")  # BUG: SQL injection
    return cur.fetchall()


def is_within_budget(spent, limit):
    """True if spending is at or under the limit."""
    return spent < limit  # BUG: wrong operator, spent == limit is still within budget


def add_entry(entry, ledger=[]):  # BUG: mutable default argument shared across calls
    """Append an entry to the ledger and return it."""
    ledger.append(entry)
    return ledger


def split_bill(amount, people):
    """Split a bill evenly between people, keeping the cents."""
    return amount / people


def page(entries, page_num, size):
    """Return page `page_num` (1-based) of `size` entries."""
    start = (page_num - 1) * size
    return entries[start:start + size]


def init_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE entries (desc TEXT, amount REAL)")
    return db
