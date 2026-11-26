"""Make the AI Judge Laugh — make.fun entry (office-laugh-a).

This program writes the office-life joke to /output/entry.txt.

Sealed gate, from the kit's RULES.txt: the output file must hold
UTF-8 text, 1 to 200 characters, more than whitespace, on one line.
The judge then compares jokes two at a time, weighing how true the
observation is to office life, how surprising the turn is, how
tight the line is, and how fresh it feels.
"""

import os

# The reply-all thread about the broken printer: 214 emails, three
# managers, zero fixed printers — and the punchline is that the
# thread still counts as "great team bonding". Office life in one
# sentence: motion mistaken for progress.
ENTRY_TEXT = (
    "Our 'reply all' thread about the broken printer now has 214 "
    "emails, three managers, and zero fixed printers \u2014 but great "
    "team bonding."
)

CHAR_LIMIT = 200
FILE_NAME = "entry.txt"


def problems_in(text, limit):
    """List every way `text` breaks the sealed gate; empty means valid."""
    found = []
    if not isinstance(text, str):
        return ["entry must be a string"]
    if not text.strip():
        return ["entry must not be only white space"]
    if text != text.strip():
        found.append("entry has leading or trailing whitespace")
    if len(text) > limit:
        found.append("entry is %d chars, limit is %d" % (len(text), limit))
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    return found


def output_dir():
    """Where the entry goes: env override, else the kit's /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def emit(text, directory):
    """Validate, then write `text` to <directory>/entry.txt."""
    bad = problems_in(text, CHAR_LIMIT)
    if bad:
        raise ValueError("gate failed: " + "; ".join(bad))
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, FILE_NAME)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)
    return target


def report(path):
    """Print what was written, with the gate numbers, for the log."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    print("Wrote %s" % path)
    print("chars: %d / %d (%d headroom), words: %d, lines: 1"
          % (len(text), CHAR_LIMIT, CHAR_LIMIT - len(text),
             len(text.split())))
    print(text)


def run():
    report(emit(ENTRY_TEXT, output_dir()))


if __name__ == "__main__":
    run()
