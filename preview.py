#!/usr/bin/env python3
"""Build, serve and automatically rebuild the local preview when sources change."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse
import importlib
import threading

import build as site_builder

ROOT = site_builder.ROOT


def source_state() -> dict:
    files = [ROOT / "build.py"]
    for directory in ["data", "templates", "assets", "files"]:
        files.extend(path for path in (ROOT / directory).rglob("*") if path.is_file())
    return {str(path): (path.stat().st_mtime_ns, path.stat().st_size) for path in files}


def watch(stop: threading.Event) -> None:
    previous = source_state()
    while not stop.wait(1):
        current = source_state()
        if current != previous:
            try:
                importlib.reload(site_builder).build()
            except (ValueError, OSError, KeyError) as error:
                print(f"Build failed: {error}. Fix the source and save again.", flush=True)
            previous = current


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4002)
    port = parser.parse_args().port
    site_builder.build()
    handler = partial(PreviewHandler, directory=str(ROOT / "dist"))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    stop = threading.Event()
    threading.Thread(target=watch, args=(stop,), daemon=True).start()
    print(f"Local preview: http://127.0.0.1:{port}/", flush=True)
    print("Source changes rebuild automatically. Refresh the browser to see them.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.", flush=True)
    finally:
        stop.set()
        server.server_close()
