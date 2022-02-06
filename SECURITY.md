# Security issues
This is the document which describes various security problems
in `chessbots` package.

## Versions
| Version | Codename | Safe  | Supported | Date     |
|:-------:|:---------|:-----:|:---------:|---------:|
| 0.0.1   | Start    |   X   |     X     |13.01.2022|
| 0.1.0   | Release  |   X   |     X     |15.01.2022|
| 0.2.0   | Science  |   X   |  &#9745;  |06.02.2022|

## Security issues
### 0.0.1 Start
- `chess.Board` passing to custom-made class based on `BaseBot` class is a pointer. It means that this bot is in "god mode".