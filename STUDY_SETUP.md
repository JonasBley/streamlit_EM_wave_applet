# Study deployment

## Codes and survey handoff

The `pid` URL field carries the hand-generated study code. It is retained for
compatibility with the supplied LimeSurvey structures (pre: 731001; post:
932619); it is not a LimeSurvey response ID. The app trims surrounding whitespace
and uppercases the code, matching the pre-survey's `strtoupper(PIDINPUT.NAOK)`.

Accepted codes contain exactly four letters plus a day from 01 to 31, for
six characters in total. The letters are the first and last letter of the
mother's first given name, then the first and last letter of the father's
first given name (e.g. Anna, Peter, birthday on the fifth: `AAPR05`). No
birthplace component is used. Eight-character codes are rejected.
Missing or invalid codes cannot start the tutorial. There is no test-code
fallback. The post-survey link sends `pid`, `journey`, `lang`, and
`appletcomplete=1`. It does not force a fresh LimeSurvey session with `newtest=Y`.

The revised post-survey maps `pid`, `journey`, and `appletcomplete` to hidden
questions; `lang` selects the survey language. The unused incoming
`appletseconds` field was removed from the revised survey structures.
Both exported surveys enable `savetimings` and `datestamp`. Their survey timing
tables do not measure activity inside the external applet. Joining by code and
subtracting the pre-survey `submitdate` from the post-survey `startdate` gives an
elapsed interval, including transit, pauses, and optional exploration; it is not
active tutorial time. Check these timestamps in a real test export before use.

## Allocation and refresh recovery

`study_session.py` assigns conditions using a SHA-256 hash of a fixed, randomly
generated study seed and the normalized code. This is repeatable pseudorandom
allocation with approximately equal probabilities, not blocked/balanced
allocation. No participant-code database is written. The same code always gets
the same condition, even if the server restarts or the original survey link is
reopened. Duplicate codes therefore also receive the same condition; check
duplicates when matching survey records.

Keep `ALLOCATION_SEED` and `ALLOCATION_CONDITIONS` unchanged once recruitment
starts. This allocation method replaces the old per-session random draw; old
pilot assignments are not recovered or retroactively relabelled.

The `resume` parameter contains the current page and control values. A refresh
of that URL restores them. Reopening the original link without `resume` starts
at the welcome page but retains the code's condition. The URL carries no timing
or interaction history. This checkpoint is not an authentication or completion
verification mechanism, and links should not be shared between participants.
Invalid checkpoints safely restart the tutorial without changing condition.
Changing `CONDITION_VERSION` invalidates older checkpoints, so freeze content
and version during data collection.

## Before recruitment

- Deploy `app.py`, `challenges.py`, and `study_session.py` together.
- Run the tests with `python -m unittest discover -s tests -v`.
- Test both conditions through the deployed pre-survey, applet (including a
  browser refresh), and post-survey. Verify code, condition, completion flag,
  language, and timestamps in exported responses. Local tests validate the URL
  contract; they cannot verify the live survey configuration or saved records.
- Use the revised six-character survey structures, with `PIDINPUT`'s maximum
  length set to 6 and validation `/^[A-Za-z]{4}(0[1-9]|[12][0-9]|3[01])$/`.
  Keep the hidden `pid` equation and the URL parameter names unchanged.
  If importing creates new survey IDs, update the app's survey URLs before
  deployment. Check the post-survey image references after import.
