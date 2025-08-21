import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import os

class ConflictDialog(Toplevel):
    def __init__(self, parent, filename):
        super().__init__(parent)
        self.title("文件名冲突")
        self.geometry("400x150")
        self.resizable(False, False)
        self.result = "skip"  # Default action is to skip

        label = tk.Label(self, text=f"文件 '{filename}' 已存在。", wraplength=380, pady=10)
        label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="覆盖", command=lambda: self.set_result("overwrite")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="跳过", command=lambda: self.set_result("skip")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="覆盖全部", command=lambda: self.set_result("overwrite_all")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="跳过全部", command=lambda: self.set_result("skip_all")).pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.wait_window(self)

    def set_result(self, result):
        self.result = result
        self.destroy()

    def on_closing(self):
        self.result = "skip"
        self.destroy()

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件批量重命名工具")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.prefix_text = tk.StringVar()
        self.apply_to_all = None # Can be 'overwrite_all' or 'skip_all'

        self._create_widgets()

    def _create_widgets(self):
        folder_frame = tk.Frame(self.root, padx=10, pady=10)
        folder_frame.pack(pady=5, fill=tk.X)
        tk.Label(folder_frame, text="选择文件夹:").pack(side=tk.LEFT, padx=(0, 10))
        self.folder_entry = tk.Entry(folder_frame, textvariable=self.folder_path, width=40, state='readonly')
        self.folder_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        browse_button = tk.Button(folder_frame, text="浏览...", command=self._browse_folder)
        browse_button.pack(side=tk.LEFT, padx=(10, 0))

        prefix_frame = tk.Frame(self.root, padx=10, pady=10)
        prefix_frame.pack(pady=5, fill=tk.X)
        tk.Label(prefix_frame, text="输入文本:").pack(side=tk.LEFT, padx=(0, 10))
        self.prefix_entry = tk.Entry(prefix_frame, textvariable=self.prefix_text, width=40)
        self.prefix_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.prefix_entry.focus_set()

        action_frame = tk.Frame(self.root, padx=10, pady=10)
        action_frame.pack(pady=10)
        rename_button = tk.Button(action_frame, text="添加前缀", command=self._add_prefix, height=2, width=20)
        rename_button.pack(side=tk.LEFT, padx=(0, 10))
        remove_button = tk.Button(action_frame, text="移除前缀", command=self._remove_prefix, height=2, width=20)
        remove_button.pack(side=tk.LEFT)

    def _browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def _process_files(self, action):
        self.apply_to_all = None # Reset state for each run
        folder = self.folder_path.get()
        text = self.prefix_text.get()

        if not folder:
            messagebox.showwarning("警告", "请先选择一个文件夹！")
            return
        if not text:
            messagebox.showwarning("警告", f"请输入要{'添加' if action == 'add' else '移除'}的文本！")
            return

        try:
            files = os.listdir(folder)
            renamed_count = 0
            skipped_count = 0

            for filename in files:
                old_file_path = os.path.join(folder, filename)
                if not os.path.isfile(old_file_path):
                    continue

                new_filename = None
                if action == 'add':
                    new_filename = text + filename
                elif action == 'remove' and filename.startswith(text):
                    new_filename = filename[len(text):]
                else:
                    continue # Skip if action is 'remove' and prefix doesn't match

                new_file_path = os.path.join(folder, new_filename)

                if os.path.exists(new_file_path):
                    if self.apply_to_all == 'skip_all':
                        skipped_count += 1
                        continue
                    
                    decision = self.apply_to_all or self._ask_conflict_resolution(new_filename)

                    if decision == 'overwrite' or decision == 'overwrite_all':
                        if decision == 'overwrite_all':
                            self.apply_to_all = 'overwrite_all'
                        os.rename(old_file_path, new_file_path)
                        renamed_count += 1
                    else: # 'skip' or 'skip_all'
                        if decision == 'skip_all':
                            self.apply_to_all = 'skip_all'
                        skipped_count += 1
                        continue
                else:
                    os.rename(old_file_path, new_file_path)
                    renamed_count += 1
            
            messagebox.showinfo("完成", f"操作完成！\n成功重命名: {renamed_count}个文件\n跳过: {skipped_count}个文件")

        except Exception as e:
            messagebox.showerror("错误", f"重命名过程中发生错误: {e}")

    def _add_prefix(self):
        self._process_files('add')

    def _remove_prefix(self):
        self._process_files('remove')

    def _ask_conflict_resolution(self, filename):
        dialog = ConflictDialog(self.root, filename)
        return dialog.result

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
