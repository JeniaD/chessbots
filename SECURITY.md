# Security issues
This is the document which describes various security problems
in `chess_api` package.

## Versions
| Version | Codename | Safe  | Supported | Date     |
|:-------:|:---------|:-----:|:---------:|---------:|
| 0.0.1   | Start    |   X   |     X     |13.01.2022|
| 0.1.0   | Release  |&#9745;|  &#9745;  |15.01.2022|

## Security issues
### 0.0.1 Start
- `chess.Board` passing to custom-made class based on `BaseBot` class is a pointer. It means that this bot is in "god mode".