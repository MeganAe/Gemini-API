import json
import requests
from typing import Union
from .constants import IMAGE_PUSH_ID


def extract_code(text: str) -> str:
    """
    Extracts code snippets from the given text.
    If only one snippet is found, returns it directly instead of a list.
    If no snippets are found, returns the original text.

    Args:
        text (str): The text containing mixed code snippets.

    Returns:
        str or list of str: A single code snippet string if only one is found, otherwise a list of all extracted code snippets. Returns the original text if no snippets are found.
    """

    snippets = []
    start_pattern = "```"
    end_pattern = "```"
    start_idx = text.find(start_pattern)

    while start_idx != -1:
        end_idx = text.find(end_pattern, start_idx + len(start_pattern))
        if end_idx != -1:
            snippet = text[start_idx : end_idx + len(end_pattern)].strip()
            snippets.append(snippet)
            start_idx = text.find(start_pattern, end_idx + len(end_pattern))
        else:
            break

    # Return directly if only one snippet is found
    if len(snippets) == 1:
        return snippets[0]
    elif len(snippets) > 1:
        return snippets
    else:
        # Return the original text if no snippets are found
        return text


def upload_image(file: Union[bytes, str]) -> str:
    """
    Upload image into bard bucket on Google API, do not need session.

    Returns:
        str: relative URL of image.
    """
    if isinstance(file, str):
        with open(file, "rb") as f:
            file_data = f.read()
    else:
        file_data = file

    response = requests.post(
        url="https://content-push.googleapis.com/upload/",
        headers={
            "Push-ID": IMAGE_PUSH_ID,
            "Content-Type": "application/octet-stream",
        },
        data=file_data,
        allow_redirects=True,
    )
    response.raise_for_status()

    return response.text


def prepare_replit_data(instructions: str, code: str, filename: str) -> list:
    """
    Creates and returns the input image data structure based on provided parameters.

    Args:
        instructions (str): The instruction text.
        code (str): The code.
        filename (str): The filename.

    Returns:
        list: The input image data structure.
    """
    return [
        [
            [
                "qACoKe",
                json.dumps([instructions, 5, code, [[filename, code]]]),
                None,
                "generic",
            ]
        ]
    ]


def max_token(text: str, n: int) -> str:
    """
    Return the first 'n' tokens (words) of the given text.

    Args:
        text (str): The input text to be processed.
        n (int): The number of tokens (words) to be included in the result.

    Returns:
        str: The first 'n' tokens from the input text.
    """
    if not isinstance(text, str):
        raise ValueError("Input 'text' must be a valid string.")

    tokens = text.split()  # Split the text into tokens (words)
    if n <= len(tokens):
        return " ".join(tokens[:n])  # Return the first 'n' tokens as a string
    else:
        return text


def max_sentence(text: str, n: int):
    """
    Print the first 'n' sentences of the given text.

    Args:
        text (str): The input text to be processed.
        n (int): The number of sentences to be printed from the beginning.

    Returns:
        None
    """
    punctuations = set("?!.")

    sentences = []
    sentence_count = 0
    for char in text:
        sentences.append(char)
        if char in punctuations:
            sentence_count += 1
            if sentence_count == n:
                result = "".join(sentences).strip()
                return result
