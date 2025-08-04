import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageToPdfConverter:
    def __init__(self, master):
        self.master = master
        master.title("图片转PDF工具")
        master.geometry("500x600")
        master.resizable(False, False)

        self.image_paths = []

        tk.Button(master, text="选择图片", command=self.select_images,
                  font=("Arial", 12), bg="#4CAF50", fg="white",
                  relief="raised", bd=3, padx=10, pady=5).pack(pady=10)

        listbox_frame = tk.Frame(master, bd=2, relief="groove")
        listbox_frame.pack(padx=20, pady=5, fill="both", expand=True)

        self.image_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE,
                                         font=("Arial", 10), height=15, bd=0, highlightthickness=0)
        self.image_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.image_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.image_listbox.config(yscrollcommand=scrollbar.set)

        sort_buttons_frame = tk.Frame(master)
        sort_buttons_frame.pack(pady=5)

        tk.Button(sort_buttons_frame, text="上移", command=self.move_image_up,
                  font=("Arial", 10), bg="#2196F3", fg="white",
                  relief="raised", bd=2, padx=8, pady=4).pack(side="left", padx=5)

        tk.Button(sort_buttons_frame, text="下移", command=self.move_image_down,
                  font=("Arial", 10), bg="#2196F3", fg="white",
                  relief="raised", bd=2, padx=8, pady=4).pack(side="left", padx=5)

        tk.Button(master, text="生成PDF", command=self.generate_pdf,
                  font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
                  relief="raised", bd=3, padx=10, pady=5).pack(pady=10)

        self.status_label = tk.Label(master, text="请选择图片并调整顺序。", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=5)
        tk.Label(master, text="图片转PDF的过程将全程在您的电脑上执行，不会上传到服务器。", fg="black", font=("Arial", 8)).pack(pady=1)
        tk.Label(master, text="由 Github@RuizeSun 制作，以 MIT 协议开放源代码。", fg="black", font=("Arial", 8)).pack(pady=1)

    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif"), ("所有文件", "*.*")]
        )
        if file_paths:
            self.image_paths = list(file_paths)
            self.update_listbox()
            self.status_label.config(text=f"已选择 {len(self.image_paths)} 张图片。")
        else:
            self.status_label.config(text="未选择任何图片。")

    def move_image_up(self):
        try:
            selected_index = self.image_listbox.curselection()[0]
            if selected_index > 0:
                self.image_paths[selected_index], self.image_paths[selected_index - 1] = \
                    self.image_paths[selected_index - 1], self.image_paths[selected_index]
                self.update_listbox()
                self.image_listbox.selection_set(selected_index - 1)
        except IndexError:
            messagebox.showwarning("警告", "请先选择一张图片！")

    def move_image_down(self):
        try:
            selected_index = self.image_listbox.curselection()[0]
            if selected_index < len(self.image_paths) - 1:
                self.image_paths[selected_index], self.image_paths[selected_index + 1] = \
                    self.image_paths[selected_index + 1], self.image_paths[selected_index]
                self.update_listbox()
                self.image_listbox.selection_set(selected_index + 1)
        except IndexError:
            messagebox.showwarning("警告", "请先选择一张图片！")

    def update_listbox(self):
        self.image_listbox.delete(0, tk.END)
        for path in self.image_paths:
            self.image_listbox.insert(tk.END, os.path.basename(path))

    def generate_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("警告", "请先选择图片！")
            return

        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")],
            title="保存PDF文件为"
        )
        if not pdf_path:
            self.status_label.config(text="PDF生成已取消。")
            return

        images = []
        try:
            self.status_label.config(text="正在处理图片并生成PDF，请稍候...")
            self.master.update_idletasks()

            for path in self.image_paths:
                img = Image.open(path)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                images.append(img)

            if images:
                images[0].save(pdf_path, save_all=True, append_images=images[1:])
                self.status_label.config(text=f"PDF已成功生成：{os.path.basename(pdf_path)}", fg="green")
                messagebox.showinfo("成功", f"PDF已成功生成：\n{pdf_path}")
            else:
                self.status_label.config(text="没有可用的图片来生成PDF。", fg="red")

        except Exception as e:
            self.status_label.config(text=f"PDF生成失败：{e}", fg="red")
            messagebox.showerror("错误", f"生成PDF时发生错误：\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()
