import sys
from argparse import ArgumentParser
from datetime import datetime
from importlib import metadata
from pathlib import Path

from prosperity3submit.submit import submit


def main() -> int:
    parser = ArgumentParser(prog="prosperity3submit", description="Submit an algorithm.")
    parser.add_argument("algorithm", type=str, help="path to the Python file containing the algorithm to submit")
    parser.add_argument(
        "--out", type=str, help="path to save submission logs to (defaults to submissions/<timestamp>.log)"
    )
    parser.add_argument("--no-logs", action="store_true", help="don't download logs when done")
    parser.add_argument("--vis", action="store_true", help="open submission in visualizer when done")
    parser.add_argument(
        "--vis-requests",
        type=int,
        default=2,
        help="number of requests the visualizer is expected to make to the submitter's HTTP server when using --vis",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {metadata.version(__package__)}")

    args = parser.parse_args()

    if args.out is not None and args.no_logs:
        print("--out and --no-logs are mutually exclusive")
        sys.exit(1)

    if args.no_logs and args.vis:
        print("--no-logs and --vis are mutually exclusive")
        sys.exit(1)

    algorithm_file = Path(args.algorithm).expanduser().resolve()
    if not algorithm_file.is_file():
        print(f"{args.algorithm} is not a file")
        sys.exit(1)

    if args.out is not None:
        output_file = Path(args.out).expanduser().resolve()
    elif args.no_logs:
        output_file = None
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = Path.cwd() / "submissions" / f"{timestamp}.log"

    submit(algorithm_file, output_file, args.vis, args.vis_requests)


if __name__ == "__main__":
    main()
