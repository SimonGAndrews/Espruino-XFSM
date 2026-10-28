#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Load an Espruino program and retain an interactive serial transcript."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import threading
import time

import serial

from run_test import (
    open_serial,
    read_available,
    read_until_prompt,
    send_and_capture,
    send_script_paced,
    sync_repl,
)


class Transcript:
    """Mirror complete host and serial output to a durable, flushed file."""

    def __init__(self, path: Path) -> None:
        self._file = path.open("x", encoding="utf-8")
        self._lock = threading.Lock()

    def write(self, text: str) -> None:
        if not text:
            return
        with self._lock:
            self._file.write(text)
            self._file.flush()
            sys.stdout.write(text)
            sys.stdout.flush()

    def close(self) -> None:
        with self._lock:
            self._file.close()


def capture(args: argparse.Namespace) -> int:
    source = args.source.read_text(encoding="utf-8")
    transcript = Transcript(args.output)
    stop_reader = threading.Event()

    try:
        with open_serial(args.port, args.baud) as repl:
            transcript.write(
                f"HOST_CAPTURE transport=paced_pyserial port={args.port} "
                f"baud={args.baud}\n"
            )
            sync_repl(repl)
            transcript.write("HOST_CAPTURE reset_begin\n")
            reset_output = send_and_capture(repl, "reset();\n", settle=0.3)
            transcript.write(reset_output)
            if not reset_output.rstrip().endswith(">"):
                transcript.write(read_until_prompt(repl, 8.0))

            transcript.write("HOST_CAPTURE upload_begin\n")
            transcript.write(send_and_capture(repl, "echo(false);\n", settle=0.2))
            repl.reset_input_buffer()
            transcript.write(send_script_paced(repl, source))
            transcript.write(read_available(repl, 1.0))
            transcript.write(send_and_capture(repl, "echo(true);\n", settle=0.3))
            transcript.write("HOST_CAPTURE upload_end\n")

            if args.initial_command:
                command = args.initial_command.rstrip("\r\n") + "\n"
                transcript.write("HOST_SEND " + command)
                transcript.write(send_and_capture(repl, command, settle=0.5))

            # Serial notifications and operator input must be serviced
            # concurrently or an event can be lost while waiting at input().
            def serial_reader() -> None:
                while not stop_reader.is_set():
                    try:
                        waiting = repl.in_waiting
                        if waiting:
                            transcript.write(
                                repl.read(waiting).decode("utf-8", "replace")
                            )
                        else:
                            time.sleep(0.02)
                    except (OSError, serial.SerialException) as error:
                        transcript.write(f"HOST_CAPTURE serial_error={error}\n")
                        stop_reader.set()

            reader = threading.Thread(target=serial_reader, daemon=True)
            reader.start()
            transcript.write(
                "HOST_CAPTURE interactive_ready; enter .capture-end to stop\n"
            )

            try:
                for line in sys.stdin:
                    if line.rstrip("\r\n") == ".capture-end":
                        break
                    if stop_reader.is_set():
                        break
                    command = line.rstrip("\r\n") + "\n"
                    transcript.write("HOST_SEND " + command)
                    repl.write(command.encode("utf-8"))
                    repl.flush()
            except KeyboardInterrupt:
                transcript.write("HOST_CAPTURE keyboard_interrupt\n")
            finally:
                # Allow the final command's response to reach the transcript
                # before closing the port and stopping the reader.
                time.sleep(args.final_settle)
                stop_reader.set()
                reader.join(timeout=2.0)
                transcript.write("HOST_CAPTURE complete\n")
    finally:
        transcript.close()

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--initial-command")
    parser.add_argument("--final-settle", type=float, default=1.0)
    return capture(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
