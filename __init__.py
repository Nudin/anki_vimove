from typing import Callable, Iterable, NewType, Optional

from aqt import mw

# TODO better navigate in tree
# tree = mw.deckBrowser._dueTree
# mw.col.decks.find_deck_in_tree(tree, 1607387237528)


# Id of a deck (calld 'did' in Anki code)
DeckId = NewType("DeckId", int)

# Trivial helper class for cleaner code
class NoneId:
    id = None


def get_first(all_decks: Iterable, _) -> Optional[DeckId]:
    try:
        return next(iter(all_decks)).id
    except StopIteration:
        return None


def get_last(all_decks: Iterable, _) -> Optional[DeckId]:
    last = NoneId
    for last in all_decks:
        pass
    return last.id


def get_next(all_decks: Iterable, current: DeckId) -> Optional[int]:
    found = False
    next_elem = NoneId
    for deck in all_decks:
        if found:
            next_elem = deck
            break
        if deck.id == current:
            found = True
    return next_elem.id


def get_previous(all_decks: Iterable, current: DeckId) -> Optional[int]:
    last = NoneId
    for deck in all_decks:
        if deck.id == current:
            break
        last = deck
    return last.id


def goto(target: DeckId):
    if mw is None:
        raise RuntimeError("Can't get interface. Anki not running?")
    mw.col.decks.select(target)
    mw.deckBrowser.show()


def move(func: Callable):
    if mw is None:
        raise RuntimeError("Can't get interface. Anki not running?")
    current = mw.col.decks.selected()
    alldecks = mw.col.decks.all_names_and_ids()
    new_deck_id = func(alldecks, current)
    if new_deck_id:
        goto(new_deck_id)


def goto_next_deck():
    move(get_next)


def goto_first_deck():
    move(get_first)


def goto_last_deck():
    move(get_last)


def goto_previous_deck():
    move(get_previous)


if mw is None:
    raise RuntimeError("Can't get interface. Anki not running?")

mw.applyShortcuts([("j", goto_next_deck)])
mw.applyShortcuts([("k", goto_previous_deck)])
mw.applyShortcuts([("g", goto_first_deck)])
mw.applyShortcuts([("Shift+g", goto_last_deck)])
mw.applyShortcuts([(" ", mw.onOverview)])
mw.applyShortcuts([("Return", mw.onOverview)])
