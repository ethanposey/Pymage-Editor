import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageTk

class TwoIntDialog(simpledialog.Dialog):
    def __init__(self, parent, title="Enter size", labels=("Width", "Height"), initial=(400, 400)):
        self.labels = labels
        self.initial = initial
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.labels[0] + ":").grid(row=0, column=0, padx=6, pady=4, sticky="e")
        tk.Label(master, text=self.labels[1] + ":").grid(row=1, column=0, padx=6, pady=4, sticky="e")

        self.e1 = tk.Entry(master) 
        self.e2 = tk.Entry(master)
        self.e1.grid(row=0, column=1, padx=6, pady=4)
        self.e2.grid(row=1, column=1, padx=6, pady=4)

        if self.initial and len(self.initial) == 2:
            self.e1.insert(0, str(self.initial[0]))
            self.e2.insert(0, str(self.initial[1]))
        return self.e1

    def validate(self):
        try:
            w, h = int(self.e1.get()), int(self.e2.get())
            if w <= 0 or h <= 0: 
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid size", "Width and height must be positive integers.")
            return False
        return True

    def apply(self):
        self.result = (int(self.e1.get()), int(self.e2.get()))


class ImageCanvas(tk.Canvas):
    """Canvas that can display a PIL image and drag it around."""
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.image_id = None
        self.photo = None
        self._drag_data = {"x": 0, "y": 0}

    def show(self, pil_img, at=(100, 100)):
        self.photo = ImageTk.PhotoImage(pil_img)
        if self.image_id is None:
            x, y = at
            self.image_id = self.create_image(x, y, anchor="nw", image=self.photo)
            self.tag_bind(self.image_id, "<ButtonPress-1>", self._on_start_drag)
            self.tag_bind(self.image_id, "<B1-Motion>", self._on_drag)
        else:
            self.itemconfigure(self.image_id, image=self.photo)

    def _on_start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.move(self.image_id, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y


class HistoryPanel(tk.Frame):
    """Sidebar with a history list that stores (desc, PIL.Image) snapshots."""
    def __init__(self, master, on_select=None, **kwargs):
        super().__init__(master, bg="#2b2b2b", **kwargs)
        self._on_select = on_select
        self._states = []
        self._cursor = -1

        tk.Label(self, text="History", bg="#2b2b2b", fg="#ffffff").pack(
            anchor="w", padx=6, pady=(0, 2)
        )

        self.list = tk.Listbox(
            self, height=20, bg="#3e3e3e", fg="#dddddd",
            activestyle="none", highlightthickness=0, borderwidth=0
        )
        self.list.pack(side="left", fill="y", padx=(8, 0), pady=(0, 8))

        sb = tk.Scrollbar(self, command=self.list.yview)
        sb.pack(side="right", fill="y", padx=(0, 8), pady=(0, 8))
        self.list.config(yscrollcommand=sb.set)

        self.list.bind("<<ListboxSelect>>", self._on_list_select)

    def reset(self):
        self._states.clear()
        self._cursor = -1
        self.list.delete(0, "end")

    def push(self, desc, pil_img):
        # trim redo branch
        if self._cursor < len(self._states) - 1:
            self._states = self._states[: self._cursor + 1]
            self.list.delete(self._cursor + 1, "end")

        self._states.append((desc, pil_img.copy()))
        self._cursor = len(self._states) - 1

        self.list.insert("end", desc)
        self._select(self._cursor)

    def step(self, delta):
        if not self._states:
            return
        new = self._cursor + delta
        if 0 <= new < len(self._states):
            self._cursor = new
            self._select(new)
            desc, img = self._states[new]
            if self._on_select:
                self._on_select(desc, img.copy())

    def _select(self, idx):
        self.list.selection_clear(0, "end")
        self.list.selection_set(idx)
        self.list.see(idx)

    def _on_list_select(self, _event=None):
        if not self.list.curselection():
            return
        self._cursor = self.list.curselection()[0]
        desc, img = self._states[self._cursor]
        if self._on_select:
            self._on_select(desc, img.copy())
