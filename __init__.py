from typing import Callable, Iterable, NewType, Optional

import aqt  # noqa: F401
from anki.rsbackend import DeckTreeNode
from aqt import gui_hooks, mw

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


def visible(deck_id):
    """Test if the deck is visible."""
    parrents = mw.col.decks.parents(deck_id)
    for parrent in parrents:
        if parrent["collapsed"]:
            return False
    return True


def get_next(
    all_decks: Iterable, current: DeckId, constraint_check: Callable
) -> Optional[DeckTreeNode]:
    """Get the first element following element `current` that fulfills the constraint."""
    found_current = False
    next_elem = None
    for deck in all_decks:
        if found_current and constraint_check(deck.id, current) and visible(deck.id):
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
        if constraint_check(deck.id, current) and visible(deck.id):
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
    alldecks = mw.col.decks.all_names_and_ids(skip_empty_default=True)
    new_deck = func(alldecks, current, constraint_check)
    if new_deck:
        new_deck_id = new_deck.id
        parrents = mw.col.decks.parents(new_deck_id)
        while not visible(new_deck_id) and len(parrents) > 0:
            new_deck_id = parrents.pop().get("id")
        goto(new_deck_id)


def toggle_collapse():
    current = mw.col.decks.selected()
    mw.col.decks.collapse(current)
    mw.deckBrowser.show()


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

str2func = {
    "goto_first_deck": goto_first_deck,
    "goto_last_deck": goto_last_deck,
    "goto_next_deck": goto_next_deck,
    "goto_next_deck_same_lvl": goto_next_deck_same_lvl,
    "goto_parent_deck": goto_parent_deck,
    "goto_previous_deck": goto_previous_deck,
    "goto_previous_deck_same_lvl": goto_previous_deck_same_lvl,
    "open_overview": mw.onOverview,
    "study": study,
    "toggle_collapse": toggle_collapse,
}

config = mw.addonManager.getConfig(__name__)
shortcut_config = []
for key, action in config["keys"].items():
    shortcut_config.append((key, str2func[action]))
scuts = mw.applyShortcuts(shortcut_config)


def setup(state, _oldstate):
    """Enable the shortcuts only in the deck browser"""
    if state == "deckBrowser":
        for scut in scuts:
            scut.setEnabled(True)
    else:
        for scut in scuts:
            scut.setEnabled(False)


gui_hooks.state_did_change.append(setup)
