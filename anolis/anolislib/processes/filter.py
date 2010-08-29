from lxml import cssselect

def filter(ElementTree, **kwargs):
    if not "filter" in kwargs or kwargs["filter"] == None:
        return
    selector = cssselect.CSSSelector(kwargs["filter"])
    for element in selector(ElementTree.getroot()):
        element.drop_tree()
