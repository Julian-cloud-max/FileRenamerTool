import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from file_operations import (
    add_suffix, remove_suffix, 
    add_prefix, remove_prefix, 
    find_and_replace, change_extension
)

# --- THEME AND APPEARANCE SETUP ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- FONT DEFINITIONS ---
        self.title_font = ctk.CTkFont(size=20, weight="bold")
        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=12, weight="bold")
        self.path_font = ctk.CTkFont(size=12, slant="italic")
        self.highlight_font = ctk.CTkFont(size=12, weight="bold")

        # --- COLOR DEFINITIONS ---
        self.HIGHLIGHT_ADD_COLOR = "#FFD700" # Gold for additions
        self.HIGHLIGHT_REMOVE_COLOR = "#E57373" # Red for removals
        self.PREVIEW_COLOR = "#5bc0de"   # Light Blue for normal text

        # --- WINDOW CONFIGURATION ---
        self.title("批量文件重命名工具 v1.4")
        self.geometry("950x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- STATE VARIABLES ---
        self.selected_folder = None
        self.file_list = []
        self.preview_list = {}
        self.operations_to_apply = {}

        # --- UI WIDGETS ---
        self._create_main_layout()
        self._create_controls()

    def _create_main_layout(self):
        self.top_frame = ctk.CTkFrame(self, corner_radius=10)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.select_folder_button = ctk.CTkButton(self.top_frame, text="选择文件夹", command=self.select_folder, font=self.button_font, corner_radius=8)
        self.select_folder_button.grid(row=0, column=0, padx=15, pady=15)
        self.folder_path_label = ctk.CTkLabel(self.top_frame, text="请选择一个文件夹开始...", anchor="w", font=self.path_font)
        self.folder_path_label.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.preview_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="文件预览 (原始 -> 新)", label_font=self.label_font, corner_radius=8)
        self.preview_scroll_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.preview_scroll_frame.grid_columnconfigure(2, weight=1)

        self.apply_button = ctk.CTkButton(self, text="应用重命名", command=self.apply_changes, font=self.title_font, fg_color="#28a745", hover_color="#218838", corner_radius=10)
        self.apply_button.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        self.status_bar = ctk.CTkLabel(self, text="准备就绪", anchor="w", font=self.path_font)
        self.status_bar.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

    def _create_controls(self):
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=10)
        self.bottom_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.bottom_frame.grid_columnconfigure((1, 2), weight=1)

        # Suffix
        ctk.CTkLabel(self.bottom_frame, text="后缀操作:", font=self.label_font).grid(row=0, column=0, padx=(15, 5), pady=5, sticky="w")
        self.suffix_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="输入后缀...", corner_radius=8)
        self.suffix_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览添加", command=lambda: self.preview_changes("suffix", "add"), font=self.button_font, corner_radius=8).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkButton(self.bottom_frame, text="预览移除", command=lambda: self.preview_changes("suffix", "remove"), font=self.button_font, corner_radius=8).grid(row=0, column=4, padx=(5, 15), pady=5)

        # Prefix
        ctk.CTkLabel(self.bottom_frame, text="前缀操作:", font=self.label_font).grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        self.prefix_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="输入前缀...", corner_radius=8)
        self.prefix_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览添加", command=lambda: self.preview_changes("prefix", "add"), font=self.button_font, corner_radius=8).grid(row=1, column=3, padx=5, pady=5)
        ctk.CTkButton(self.bottom_frame, text="预览移除", command=lambda: self.preview_changes("prefix", "remove"), font=self.button_font, corner_radius=8).grid(row=1, column=4, padx=(5, 15), pady=5)

        # Replace
        ctk.CTkLabel(self.bottom_frame, text="替换操作:", font=self.label_font).grid(row=2, column=0, padx=(15, 5), pady=5, sticky="w")
        self.find_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="查找内容...", corner_radius=8)
        self.find_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.replace_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="替换为...", corner_radius=8)
        self.replace_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览替换", command=lambda: self.preview_changes("replace"), font=self.button_font, corner_radius=8).grid(row=2, column=3, columnspan=2, padx=(5, 15), pady=5, sticky="ew")

        # Extension
        ctk.CTkLabel(self.bottom_frame, text="扩展名操作:", font=self.label_font).grid(row=3, column=0, padx=(15, 5), pady=5, sticky="w")
        self.old_ext_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="原始扩展名 (如: .jpg)", corner_radius=8)
        self.old_ext_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.new_ext_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="新扩展名 (如: .png)", corner_radius=8)
        self.new_ext_entry.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览修改", command=lambda: self.preview_changes("extension"), font=self.button_font, corner_radius=8).grid(row=3, column=3, columnspan=2, padx=(5, 15), pady=5, sticky="ew")

        self.entry_widgets = [self.suffix_entry, self.prefix_entry, self.find_entry, self.replace_entry, self.old_ext_entry, self.new_ext_entry]

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path: self.load_folder_data(folder_path)

    def load_folder_data(self, folder_path):
        self.selected_folder = folder_path
        self.folder_path_label.configure(text=f"{self.selected_folder}")
        try:
            self.file_list = sorted([f for f in os.listdir(self.selected_folder) if os.path.isfile(os.path.join(self.selected_folder, f))])
            self.preview_list = {f: f for f in self.file_list}
            self.operations_to_apply = {}
            self.update_preview_display()
            self.status_bar.configure(text=f"已加载 {len(self.file_list)} 个文件。")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件夹: {e}")
            self.status_bar.configure(text="错误：无法读取文件夹")

    def update_preview_display(self):
        for widget in self.preview_scroll_frame.winfo_children():
            widget.destroy()

        for i, original_name in enumerate(self.file_list, start=1):
            op_details = self.operations_to_apply.get(original_name)
            
            display_name = self.preview_list.get(original_name, original_name)

            ctk.CTkLabel(self.preview_scroll_frame, text=original_name, anchor="w").grid(row=i, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.preview_scroll_frame, text="->").grid(row=i, column=1, padx=5, pady=2)

            new_name_frame = ctk.CTkFrame(self.preview_scroll_frame, fg_color="transparent")
            new_name_frame.grid(row=i, column=2, padx=10, pady=2, sticky="w")

            self._display_highlighted_name(new_name_frame, original_name, display_name, op_details)

    def _display_highlighted_name(self, frame, original_name, new_name, op_details):
        if not op_details:
            ctk.CTkLabel(frame, text=new_name, anchor="w", text_color=self.PREVIEW_COLOR).grid(row=0, column=0, sticky='w')
            return

        op_type, op_mode, op_params = op_details['type'], op_details['mode'], op_details['params']
        parts = []

        # Use original_name for remove previews, new_name for add/replace previews
        name_to_process = original_name if op_mode == 'remove' else new_name

        if op_mode == 'add':
            value = op_params
            if op_type == 'prefix': parts = [(value, self.HIGHLIGHT_ADD_COLOR), (name_to_process[len(value):], self.PREVIEW_COLOR)]
            elif op_type == 'suffix':
                name_part, ext_part = os.path.splitext(name_to_process)
                parts = [(name_part[:-len(value)], self.PREVIEW_COLOR), (value, self.HIGHLIGHT_ADD_COLOR), (ext_part, self.PREVIEW_COLOR)]
        elif op_mode == 'remove':
            value = op_params
            if op_type == 'prefix' and name_to_process.startswith(value): parts = [(value, self.HIGHLIGHT_REMOVE_COLOR), (name_to_process[len(value):], self.PREVIEW_COLOR)]
            elif op_type == 'suffix' and os.path.splitext(name_to_process)[0].endswith(value):
                name_part, ext_part = os.path.splitext(name_to_process)
                parts = [(name_part[:-len(value)], self.PREVIEW_COLOR), (value, self.HIGHLIGHT_REMOVE_COLOR), (ext_part, self.PREVIEW_COLOR)]
        elif op_type == 'replace':
            find, replace = op_params
            original_name_part, ext_part = os.path.splitext(original_name)
            if find in original_name_part:
                split_parts = original_name_part.split(find)
                for i, p in enumerate(split_parts):
                    parts.append((p, self.PREVIEW_COLOR))
                    if i < len(split_parts) - 1:
                        parts.append((replace, self.HIGHLIGHT_ADD_COLOR))
                parts.append((ext_part, self.PREVIEW_COLOR))
            else:
                 parts.append((new_name, self.PREVIEW_COLOR))
        elif op_type == 'extension':
            name_part, ext_part = os.path.splitext(new_name)
            parts = [(name_part, self.PREVIEW_COLOR), (ext_part, self.HIGHLIGHT_ADD_COLOR)]

        if not parts: parts.append((new_name, self.PREVIEW_COLOR))
        
        col = 0
        for text, color in parts:
            if text:
                ctk.CTkLabel(frame, text=text, anchor="w", text_color=color, font=self.highlight_font if color != self.PREVIEW_COLOR else None).grid(row=0, column=col, sticky='w')
                col += 1

    def preview_changes(self, op_type, op_mode=None):
        if not self.selected_folder: messagebox.showwarning("警告", "请先选择一个文件夹！"); return
        self.operations_to_apply = {}

        params = {
            "suffix": lambda: self.suffix_entry.get(),
            "prefix": lambda: self.prefix_entry.get(),
            "replace": lambda: (self.find_entry.get(), self.replace_entry.get()),
            "extension": lambda: (self.old_ext_entry.get(), self.new_ext_entry.get())
        }
        
        op_params = params[op_type]()
        if not any(op_params) and op_type != 'replace': messagebox.showwarning("警告", "请输入操作所需的内容！"); return

        for original_name in self.file_list:
            name_part, ext_part = os.path.splitext(original_name)
            new_preview_name = original_name

            if op_type == "suffix":
                value = op_params
                if op_mode == "add": new_preview_name = f"{name_part}{value}{ext_part}"
                elif op_mode == "remove" and name_part.endswith(value): new_preview_name = f"{name_part[:-len(value)]}{ext_part}"
            elif op_type == "prefix":
                value = op_params
                if op_mode == "add": new_preview_name = f"{value}{original_name}"
                elif op_mode == "remove" and original_name.startswith(value): new_preview_name = original_name[len(value):]
            elif op_type == "replace":
                find, replace = op_params
                if find and find in name_part: new_preview_name = f"{name_part.replace(find, replace)}{ext_part}"
            elif op_type == "extension":
                old_ext, new_ext = op_params
                if not old_ext.startswith('.'): old_ext = '.' + old_ext
                if not new_ext.startswith('.'): new_ext = '.' + new_ext
                if ext_part.lower() == old_ext.lower(): new_preview_name = f"{name_part}{new_ext}"

            self.preview_list[original_name] = new_preview_name
            if original_name != new_preview_name:
                self.operations_to_apply[original_name] = {
                    'type': op_type, 'mode': op_mode, 'params': op_params, 'new_name': new_preview_name
                }
        
        self.update_preview_display()
        self.status_bar.configure(text="预览已更新。点击 '应用重命名' 来保存更改。")

    def apply_changes(self):
        if not self.selected_folder or not self.operations_to_apply: messagebox.showinfo("提示", "请先选择文件夹并预览更改。"); return
        if not messagebox.askyesno("确认操作", f"您确定要重命名 {len(self.operations_to_apply)} 个文件吗？此操作无法撤销。"):
            return

        changed_count, errors = 0, []
        for original_name, op in self.operations_to_apply.items():
            original_path = os.path.join(self.selected_folder, original_name)
            if not os.path.exists(original_path): continue

            result = ""
            try:
                op_type, op_params = op['type'], op['params']
                if op_type == "suffix": result = add_suffix(original_path, op_params) if op['mode'] == "add" else remove_suffix(original_path, op_params)
                elif op_type == "prefix": result = add_prefix(original_path, op_params) if op['mode'] == "add" else remove_prefix(original_path, op_params)
                elif op_type == "replace": result = find_and_replace(original_path, op_params[0], op_params[1])
                elif op_type == "extension": result = change_extension(original_path, op_params[0], op_params[1])
                
                if "Error" in result or "Skipped" in result: errors.append(result)
                else: changed_count += 1
            except Exception as e:
                errors.append(f"重命名 {original_name} 失败: {e}")

        if errors:
            messagebox.showerror("完成 (有错误或跳过)", f"成功: {changed_count}, 失败/跳过: {len(errors)}\n" + "\n".join(errors))
        else:
            messagebox.showinfo("完成", f"成功重命名 {changed_count} 个文件。")
        
        # Clear inputs and reload data
        for entry in self.entry_widgets:
            entry.delete(0, 'end')
        self.load_folder_data(self.selected_folder)

if __name__ == "__main__":
    app = App()
    app.mainloop()
