"""Utils."""
from astroid.util import Uninferable
from astroid.bases import Instance
from astroid.nodes import ClassDef
from astroid.exceptions import InferenceError


def node_is_subclass(cls, *subclass_names):
    """Checks if cls node has parent with subclass_name."""
    if not isinstance(cls, (ClassDef, Instance)):
        return False

    if cls.bases == Uninferable:
        return False
    for base_cls in cls.bases:
        try:
            for inf in base_cls.inferred():
                if inf.qname() in subclass_names:
                    return True
                if inf != cls and node_is_subclass(inf, *subclass_names):
                    # check up the hierarchy in case we are a subclass of
                    # a subclass of a subclass ...
                    return True
        except InferenceError:
            continue

    return False
