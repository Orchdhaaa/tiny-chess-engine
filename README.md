# tiny-chess-engine

A chess engine in at most 4,096 bytes of Python, entered in the make.fun
competition "Build the strongest chess engine in 4 KB of Python"
($500 over 20 places, $100 for 1st; deadline 2026-11-24T17:00:00Z).
`main.py` at the repository root is the whole engine: Python 3.13,
standard library only, deterministic search to a fixed depth or node
count — never to a clock, no unseeded randomness, no model calls.

## How it plays

Each trial is 16 games against eight house engines, weakest first, twice
each (once as White, once as Black) from book openings: alpha-beta
depth-2 (855), depth-3 (1073), depth-4 (1199), nodes-100k (1392),
nodes-250k (1497), nodes-500k (1596), nodes-1M (1667), nodes-2M (1712).
Results become an Elo rating (0-2,112) anchored to those ratings; entries
rank on mean Elo over 6 trials and must beat the house baseline,
sunfish's 4 KB engine, to take a prize.

## Protocol

`main.py` talks to the env at `$MAKEFUN_ENV_URL` only, over HTTP, with
JSON POSTs: `POST /game {}` for the game in play, `POST /move
{"game": n, "move": "<uci>"}` to play a move, `POST /resign {"game": n}`
to resign. Moves are UCI (`e2e4`, `e7e8q`; castling is the king's move,
`e1g1`). A move must reach the env within 10 seconds of the position
being served; a trial has 3,600 seconds of wall time.

## Size

`main.py` is at most 4,096 bytes as committed (comments, whitespace and
any compressed payload included). The whole repository snapshot is at
most 8,192 bytes and no file is over 4,096 bytes.

## Grade it locally

From the competition kit, with Docker and the `makefun` CLI:

    makefun grade-local --kit . --bot <your repository> --driver docker

Then `makefun check` runs the site's pre-submit checks, size caps
included.

## License

MIT. See [LICENSE](LICENSE).
