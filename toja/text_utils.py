"""Utility functions for dealing with Joke text."""
from copy import deepcopy
from typing import List


def raw_text(node: dict) -> str:
    """Extract the raw text from a Prosemirror JSON node.

    :param node: The node to extract the text from
    :type node: dict
    :return: The extracted text
    :return_type: str
    """
    if 'text' in node:
        return node['text']
    elif 'content' in node:
        return ''.join([raw_text(child) for child in node['content']])
    else:
        return ''


def annotations(node: dict) -> List[dict]:
    """Extract all annotations from a Prosemirror JSON node.

    :param node: The node to extract the annotations from
    :type node: dict
    :return: The extracted annotations
    :return_type: List[dict]
    """
    result = []
    if 'marks' in node:
        for mark in node['marks']:
            annotation = deepcopy(mark)
            annotation['text'] = raw_text(node)
            if annotation['text'].strip():
                result.append(annotation)
    if 'content' in node:
        for child in node['content']:
            result.extend(annotations(child))
    return result
