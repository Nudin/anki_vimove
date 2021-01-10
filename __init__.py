from typing import Callable, Iterable, NewType, Optional

from anki.rsbackend import DeckTreeNode
from aqt import mw

# Id of a deck (calld 'did' in Anki code)
DeckId = NewType("DeckId", int)


def get_first(all_decks: Iterable, *_) -> Optional[DeckTreeNode]:
    """Get first element of Iterable."""
    try:
        return next(iter(all_decks))
    except StopIteration:
        return None


def get_last(all_decks: Iterable, *_) -> Optional[DeckTreeNode]:
    """Get last element of Iterable."""
    last = None
    for last in all_decks:
        pass
    return last


def get_next(
    all_decks: Iterable, current: DeckId, constraint_check: Callable
) -> Optional[DeckTreeNode]:
    """Get the first element following element `current` that fulfills the constraint."""
    found_current = False
    next_elem = None
    for deck in all_decks:
        if found_current and constraint_check(deck.id, current):
            next_elem = deck
            break
        if deck.id == current:
            found_current = True
    return next_elem


def get_previous(
    all_decks: Iterable, current: DeckId, constraint_check: Callable
) -> Optional[DeckTreeNode]:
    """Get the last element before `current` that fulfills the constraint."""
    last = None
    for deck in all_decks:
        if deck.id == current:
            break
        if constraint_check(deck.id, current):
            last = deck
    return last


def goto(target: DeckId):
    if mw is None:
        raise RuntimeError("Can't get interface. Anki not running?")
    mw.col.decks.select(target)
    mw.deckBrowser.show()


def compare_level(A_id, B_id):
    """Compare the levels of two decks."""
    tree = mw.col.decks.deck_tree()
    A = mw.col.decks.find_deck_in_tree(tree, A_id)
    B = mw.col.decks.find_deck_in_tree(tree, B_id)
    if A is None or B is None:
        return -1
    return A.level - B.level


def check_same_level(A_id, B_id):
    """Check if two decks have identical level."""
    return compare_level(A_id, B_id) == 0


def check_lower_level(A_id, B_id):
    """Deck A is less deep nested then deck B."""
    return compare_level(A_id, B_id) < 0


def move(func: Callable, constraint_check: Callable = lambda *_: True):
    """Move to a new position found by calling `func`."""
    if mw is None:
        raise RuntimeError("Can't get interface. Anki not running?")
    current = mw.col.decks.selected()
    alldecks = mw.col.decks.all_names_and_ids()
    new_deck_id = None
    new_deck_id = func(alldecks, current, constraint_check)
    if new_deck_id:
        goto(new_deck_id.id)


def goto_next_deck_same_lvl():
    move(get_next, check_same_level)


def goto_next_deck():
    move(get_next)


def goto_previous_deck_same_lvl():
    move(get_previous, check_same_level)


def goto_previous_deck():
    move(get_previous)


def goto_parent_deck():
    move(get_previous, check_lower_level)


def goto_first_deck():
    move(get_first)


def goto_last_deck():
    move(get_last)


def study():
    mw.moveToState("review")


if mw is None:
    raise RuntimeError("Can't get interface. Anki not running?")

mw.applyShortcuts([("j", goto_next_deck)])
mw.applyShortcuts([("Shift+j", goto_next_deck_same_lvl)])
mw.applyShortcuts([("k", goto_previous_deck)])
mw.applyShortcuts([("Shift+k", goto_previous_deck_same_lvl)])
mw.applyShortcuts([("h", goto_parent_deck)])
mw.applyShortcuts([("g", goto_first_deck)])
mw.applyShortcuts([("Shift+g", goto_last_deck)])
mw.applyShortcuts([("o", mw.onOverview)])
mw.applyShortcuts([("Return", study)])
