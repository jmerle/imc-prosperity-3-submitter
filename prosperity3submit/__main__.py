import sys
from datetime import datetime
from importlib import metadata
from pathlib import Path
from typing import Annotated, Optional

from typer import Argument, Option, Typer

from prosperity3submit.submit import submit


def version_callback(value: bool) -> None:
    if value:
        print(f"prosperity3submit {metadata.version(__package__)}")
        sys.exit(0)


app = Typer(context_settings={"help_option_names": ["--help", "-h"]})


@app.command()
def cli(
    algorithm: Annotated[Path, Argument(help="Path to the Python file containing the algorithm to submit.", show_default=False, exists=True, file_okay=True, dir_okay=False, resolve_path=True)],
    out: Annotated[Optional[str], Option(help="File to save submission logs to (defaults to submissions/<timestamp>.log).", show_default=False, dir_okay=False, resolve_path=True)] = None,
    no_out: Annotated[bool, Option("--no-out", help="Don't download logs when done.")] = False,
    vis: Annotated[bool, Option("--vis", help="Open backtest results in https://jmerle.github.io/imc-prosperity-3-visualizer/ when done.")] = False,
    version: Annotated[bool, Option("--version", "-v", help="Show the program's version number and exit.", is_eager=True, callback=version_callback)] = False,
) -> None:  # fmt: skip
    """Submit an IMC Prosperity 3 algorithm."""
    if out is not None and no_out:
        print("--out and --no-logs are mutually exclusive")
        sys.exit(1)

    if no_out and vis:
        print("--no-logs and --vis are mutually exclusive")
        sys.exit(1)

    if out is not None:
        output_file = Path(out).expanduser().resolve()
    elif no_out:
        output_file = None
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = Path.cwd() / "submissions" / f"{timestamp}.log"

    submit(algorithm, output_file, vis)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
