# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>

# ----------------------------------------------------------
# Hamtare: Desktop video downloader with yt_dlp and tkinter
# Author: ByteBurglar
# Source: https://github.com/byteburglar/hamtare
# ----------------------------------------------------------

__version__ = "0.1"

import base64
import os
import re
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import yt_dlp


class Hamtare:
    title = f"Hamtare v{__version__}"
    github_url = "https://github.com/byteburglar/hamtare"

    def __init__(self, root):
        self.root = root
        self.root.title(self.title)
        self.root.resizable(False, False)
        self.root.eval("tk::PlaceWindow . center")

        self.download_path = str(Path.home() / "Videos/Hamtare")
        Path(self.download_path).mkdir(parents=True, exist_ok=True)

        top_frame = ttk.Frame(root, relief="flat", borderwidth=1)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        hamtare_ASCII = """
 _   _                 _                 
| | | | __ _ _ __ ___ | |_ __ _ _ __ ___ 
| |_| |/ _` | '_ ` _ \\| __/ _` | '__/ _ \\
|  _  | (_| | | | | | | || (_| | | |  __/
|_| |_|\\__,_|_| |_| |_|\\__\\__,_|_|  \\___|

"""

        hamtare_logo = ttk.Label(
            top_frame,
            text=hamtare_ASCII,
            font=("Courier", 12, "bold"),
        )
        hamtare_logo.pack(padx=5, pady=(5, 0))

        bottom_frame = ttk.Frame(root, relief="groove", borderwidth=1)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.about_label = ttk.Label(
            bottom_frame,
            text=(
                "A simple video downloader GUI using on yt_dlp and tkinter.\n"
                "Licensed under The Unlicense https://unlicense.org"
            ),
            font=("Arial ", 8),
        )
        self.about_label.pack(fill=tk.X, padx=5, pady=5)

        hamtare_by = ttk.Label(
            bottom_frame, text="Brought to you by ByteBurglar", font=("Arial", 8)
        )
        hamtare_by.pack(fill=tk.X, padx=5, pady=(0, 5))
        hamtare_by_url = ttk.Label(
            bottom_frame,
            text=(
                "The only source to download a legit copy of Hamtare is:\n"
                f"{self.github_url}"
            ),
            font=("Arial", 8, "bold"),
            cursor="hand2",
        )
        hamtare_by_url.bind(
            "<Button-1>", lambda _: webbrowser.open_new(self.github_url)
        )
        hamtare_by_url.pack(fill=tk.X, padx=5, pady=(0, 5))
        hamtare_ver = ttk.Label(bottom_frame, text=f"Version {__version__}")
        hamtare_ver.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.video_link_label = ttk.Label(
            self.root,
            text="Video URL",
            font=("Arial", 12, "bold", "italic"),
        )
        self.video_link_label.pack(padx=5, pady=(0, 3))

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.root, textvariable=self.url_var, width=50)
        self.url_entry.pack(fill=tk.X, padx=5, pady=5, ipadx=10, ipady=5)

        self.set_entry_from_clipboard()

        self.video_var = tk.BooleanVar()
        self.video_checkbtn = ttk.Checkbutton(
            self.root, text="Video only", variable=self.video_var
        )
        self.video_checkbtn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.audio_var = tk.BooleanVar()
        self.audio_checkbtn = ttk.Checkbutton(
            self.root, text="Audio only", variable=self.audio_var
        )
        self.audio_checkbtn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.audiovideo_var = tk.BooleanVar()
        self.audiovideo_checkbtn = ttk.Checkbutton(
            self.root, text="Normal", variable=self.audiovideo_var
        )
        self.audiovideo_checkbtn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.audiovideo_checkbtn.invoke()

        self.download_btn = ttk.Button(
            self.root, text="Download", command=self.handle_download
        )
        self.download_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.root.bind("<Return>", self.handle_download)

        self.root.after(1, lambda: self.url_entry.focus_set())

        self.ydl_opts = {}

    def set_entry_from_clipboard(self):
        url_pattern = (
            r"https?://(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+(?:/[^\s]*)?"
        )
        try:
            clipboard_content = self.root.clipboard_get().strip()
        except tk.TclError:
            clipboard_content = ""

        if clipboard_content and re.match(url_pattern, clipboard_content):
            self.url_var.set(clipboard_content)

    def handle_download(self, event=None):
        if self.download_btn.cget("text") == "Stop":
            self.url_entry.config(state="normal")
            self.video_checkbtn.config(state="normal")
            self.audio_checkbtn.config(state="normal")
            self.download_btn.config(text="Download")
            return

        url = self.url_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        self.url_entry.config(state="disabled")
        self.video_checkbtn.config(state="disabled")
        self.audio_checkbtn.config(state="disabled")
        self.download_btn.config(text="Stop")

        threading.Thread(target=self.download_video).start()

    def download_video(self):
        try:
            formats = []
            if self.video_var.get():
                formats += ["bestvideo[ext=mp4]"]
            if self.audio_var.get():
                formats += ["bestaudio[ext=m4a]"]
            if self.audiovideo_var.get():
                formats += ["best[ext=mp4]"]

            if not formats:
                messagebox.showerror("Error", "Please select at least one format")
                return

            output_path = os.path.join(self.download_path, "%(title)s.%(ext)s")
            self.ydl_opts.update(
                {
                    "format": "+".join(formats),
                    "outtmpl": output_path,
                    "progress_hooks": [self.progress_hook],
                }
            )

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url_var.get()])

            messagebox.showinfo(
                "Success",
                f"Download completed successfully!\nDownloaded to: {self.download_path}",
            )
        except Exception as e:
            messagebox.showerror("Error", "Failed to download video.\n" + str(e))
        finally:
            self.url_entry.config(state="normal")
            self.video_checkbtn.config(state="normal")
            self.audio_checkbtn.config(state="normal")
            self.download_btn.config(text="Download")

    def progress_hook(self, d):
        if d["status"] == "downloading":
            downloaded_bytes = d.get("downloaded_bytes", 0)
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 1)
            progress_percent = int(downloaded_bytes / total_bytes * 100)
            self.root.title(f"Downloading ({progress_percent}%)")
        else:
            self.root.title(self.title)


def main():
    root = tk.Tk()
    app = Hamtare(root)
    root.mainloop()


if __name__ == "__main__":
    main()
