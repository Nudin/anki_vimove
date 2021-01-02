from aqt import mw

# TODO better navigate in tree
# tree = mw.deckBrowser._dueTree
# mw.col.decks.find_deck_in_tree(tree, 1607387237528)


class NoneId:
    id = None


def get_first(all_decks, _):
    try:
        return next(iter(all_decks)).id
    except StopIteration:
        return None


def get_last(all_decks, _):
    last = NoneId
    for last in all_decks:
        pass
    return last.id


def get_next(all_decks, current):
    found = False
    next_elem = NoneId
    for deck in all_decks:
        if found:
            next_elem = deck
            break
        if deck.id == current:
            found = True
    return next_elem.id


def get_previous(all_decks, current):
    last = NoneId
    for deck in all_decks:
        if deck.id == current:
            break
        last = deck
    return last.id


def goto(target):
    mw.col.decks.select(target)
    mw.deckBrowser.show()


def move(func):
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


mw.applyShortcuts([("j", goto_next_deck)])
mw.applyShortcuts([("k", goto_previous_deck)])
mw.applyShortcuts([("g", goto_first_deck)])
mw.applyShortcuts([("Shift+g", goto_last_deck)])
mw.applyShortcuts([(" ", mw.onOverview)])
mw.applyShortcuts([("Return", mw.onOverview)])
