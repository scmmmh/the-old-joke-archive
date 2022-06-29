"""Utility functions for dealing with Joke text."""


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
