import os
import tkinter as tk
from tkinter import filedialog as fd

from image_processing.operations import (
    apply_effect,
    open_img,
    resize_img,
    rotate_img,
    save_img,
    grayscale_image,
    flip_image,
    mirror_image,
    invert_image,
    sepia_image,
    tint_image
)

from ui.widgets import TwoIntDialog, ImageCanvas, HistoryPanel

class ImageEditorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.iconbitmap("images/app_icon.ico") 
        self.title("Pymage Editor")
        self.geometry("1920x1080")
        self.configure(bg="#1f1f1f")
        self.resizable(True, True)

        self._create_menubar()

        self.canvas = ImageCanvas(self, bg="#343434")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.history = HistoryPanel(self, on_select=self._load_history_state)
        self.history.pack(side="right", fill="y")

        # Current image state
        self.img = None

        # Undo/redo keys route through HistoryPanel
        self.bind("<Control-z>", lambda e: self.history.step(-1))
        self.bind("<Control-y>", lambda e: self.history.step(1))

    # -------- Menus --------
    def _create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open image...", command=self._open_image)
        file_menu.add_command(label="Save image", command=self._save_image)
        file_menu.add_command(label="Save image as...", command=self._save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rotate", command=self._rotate_image)
        edit_menu.add_command(label="Resize", command=self._resize_image)
        edit_menu.add_command(label="Flip", command=self._flip_vertical)
        edit_menu.add_command(label="Mirror", command=self._flip_horizontal)

        effects = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Effects", menu=effects)
        effects.add_command(label="Blur", command=lambda: self._apply("blur", "Blur"))
        effects.add_command(label="Contour", command=lambda: self._apply("contour", "Contour"))
        effects.add_command(label="Detail", command=lambda: self._apply("detail", "Detail"))
        effects.add_command(label="Edge Enhance", command=lambda: self._apply("edge enhance", "Edge Enhance"))
        effects.add_command(label="Emboss", command=lambda: self._apply("emboss", "Emboss"))
        effects.add_command(label="Find Edges", command=lambda: self._apply("find edges", "Find Edges"))
        effects.add_command(label="Sharpen", command=lambda: self._apply("sharpen", "Sharpen"))
        effects.add_command(label="Smooth", command=lambda: self._apply("smooth", "Smooth"))

        # Filter Menu
        filter_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Filters", menu=filter_menu)
        filter_menu.add_command(label="Grayscale", command=self._grayscale)
        filter_menu.add_command(label="Invert", command=self._invert)
        filter_menu.add_command(label="Sepia", command=self._sepia)
        filter_menu.add_command(label="Tint", command=self._tint)

    # -------- File ops --------
    def _open_image(self):
        file_path = fd.askopenfilename(
            title="Open Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*")],
        )
        if not file_path:
            return
        self.current_path = file_path
        self.img = open_img(file_path)
        self.canvas.show(self.img, at=(100, 100))
        self.history.reset()
        self.history.push(f"Open: {os.path.basename(file_path)}", self.img)

    def _save_image(self):
        if not self.img:
            return
        target = getattr(self, "current_path", None)
        if not target:
            return self._save_image_as()
        save_img(self.img, target)

    def _save_image_as(self):
        if not self.img:
            return
        save_path = fd.asksaveasfilename(
            title="Save Image As...",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp"), ("All files", "*.*")],
        )
        if save_path:
            save_img(self.img, save_path)


    # ---------- Edit actions ----------
    def _rotate_image(self):
        if not self.img:
            return
        self.img = rotate_img(self.img)
        self.canvas.show(self.img)
        self.history.push("Rotate", self.img)

    def _resize_image(self):
        if not self.img:
            return
        cur_w, cur_h = self.img.width, self.img.height
        dlg = TwoIntDialog(self, title="Resize Image", labels=("Width (px)", "Height (px)"),
                           initial=(min(cur_w, 400), min(cur_h, 400)))
        if dlg.result:
            w, h = dlg.result
            self.img = resize_img(self.img, w, h)
            self.canvas.show(self.img)
            self.history.push(f"Resize {w}x{h}", self.img)

    def _flip_vertical(self):
        if self.img:
            self.img = flip_image(self.img)
            self.canvas.show(self.img)
            self.history.push("Vertical Flip", self.img)

    def _flip_horizontal(self):
        if self.img:
            self.img = mirror_image(self.img)
            self.canvas.show(self.img)
            self.history.push("Horizontal Flip", self.img)

    # ---------- Effects ----------
    def _apply(self, effect_key: str, label: str):
        if not self.img:
            return
        self.img = apply_effect(self.img, effect_key)
        self.canvas.show(self.img)
        self.history.push(label, self.img)

    # ----------- Filters ----------
    def _grayscale(self):
        if self.img:
            self.img = grayscale_image(self.img)
            self.canvas.show(self.img)
            self.history.push("Grayscale", self.img)

    def _invert(self):
        if self.img:
            self.img = invert_image(self.img)
            self.canvas.show(self.img)
            self.history.push("Invert", self.img)
    
    def _sepia(self):
        if self.img:
            self.img = sepia_image(self.img)
            self.canvas.show(self.img)
            self.history.push("Sepia", self.img)
    
    def _tint(self):
        if self.img:
            self.img = tint_image(self.img, "red")
            self.canvas.show(self.img)
            self.history.push("Tint", self.img)

    # -------- History integration --------
    def _load_history_state(self, _desc: str, img_copy):
        self.img = img_copy
        self.canvas.show(self.img)
