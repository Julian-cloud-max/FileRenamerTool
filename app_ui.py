import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import re

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
        self.HIGHLIGHT_ADD_COLOR = "#FFD700" # Gold
        self.HIGHLIGHT_REMOVE_COLOR = "#E57373" # Red
        self.PREVIEW_COLOR = "#5bc0de"   # Light Blue

        # --- WINDOW CONFIGURATION ---
        self.title("批量文件重命名工具 v2.2 - 智能排序")
        self.geometry("950x850")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- STATE VARIABLES ---
        self.selected_folder = None
        self.undo_log_path = None
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
        self.select_folder_button.grid(row=0, column=0, padx=15, pady=10)
        
        self.folder_path_label = ctk.CTkLabel(self.top_frame, text="请选择一个文件夹开始...", anchor="w", font=self.path_font)
        self.folder_path_label.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        self.undo_button = ctk.CTkButton(self.top_frame, text="撤销上一次操作", command=self.undo_last_rename, font=self.button_font, corner_radius=8, state="disabled")
        self.undo_button.grid(row=0, column=2, padx=15, pady=10)

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

        # ... (Previous controls remain the same) ...
        ctk.CTkLabel(self.bottom_frame, text="后缀操作:", font=self.label_font).grid(row=0, column=0, padx=(15, 5), pady=5, sticky="w")
        self.suffix_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="输入后缀...", corner_radius=8)
        self.suffix_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览添加", command=lambda: self.preview_changes("suffix", "add"), font=self.button_font, corner_radius=8).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkButton(self.bottom_frame, text="预览移除", command=lambda: self.preview_changes("suffix", "remove"), font=self.button_font, corner_radius=8).grid(row=0, column=4, padx=(5, 15), pady=5)
        ctk.CTkLabel(self.bottom_frame, text="前缀操作:", font=self.label_font).grid(row=1, column=0, padx=(15, 5), pady=5, sticky="w")
        self.prefix_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="输入前缀...", corner_radius=8)
        self.prefix_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览添加", command=lambda: self.preview_changes("prefix", "add"), font=self.button_font, corner_radius=8).grid(row=1, column=3, padx=5, pady=5)
        ctk.CTkButton(self.bottom_frame, text="预览移除", command=lambda: self.preview_changes("prefix", "remove"), font=self.button_font, corner_radius=8).grid(row=1, column=4, padx=(5, 15), pady=5)
        ctk.CTkLabel(self.bottom_frame, text="替换操作:", font=self.label_font).grid(row=2, column=0, padx=(15, 5), pady=5, sticky="w")
        self.find_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="查找内容...", corner_radius=8)
        self.find_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.replace_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="替换为...", corner_radius=8)
        self.replace_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览替换", command=lambda: self.preview_changes("replace"), font=self.button_font, corner_radius=8).grid(row=2, column=3, columnspan=2, padx=(5, 15), pady=5, sticky="ew")
        ctk.CTkLabel(self.bottom_frame, text="扩展名操作:", font=self.label_font).grid(row=3, column=0, padx=(15, 5), pady=5, sticky="w")
        self.old_ext_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="原始扩展名 (如: .jpg)", corner_radius=8)
        self.old_ext_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.new_ext_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="新扩展名 (如: .png)", corner_radius=8)
        self.new_ext_entry.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.bottom_frame, text="预览修改", command=lambda: self.preview_changes("extension"), font=self.button_font, corner_radius=8).grid(row=3, column=3, columnspan=2, padx=(5, 15), pady=5, sticky="ew")

        # Numbering Controls
        ctk.CTkLabel(self.bottom_frame, text="数字排序:", font=self.label_font).grid(row=4, column=0, padx=(15, 5), pady=5, sticky="w")
        self.start_num_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="起始编号", corner_radius=8)
        self.start_num_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.separator_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="分隔符", corner_radius=8)
        self.separator_entry.grid(row=4, column=2, padx=5, pady=5, sticky="ew")
        self.position_menu = ctk.CTkOptionMenu(self.bottom_frame, values=["前缀", "后缀"], corner_radius=8, font=self.button_font)
        self.position_menu.grid(row=4, column=3, padx=5, pady=5)
        self.replace_nums_checkbox = ctk.CTkCheckBox(self.bottom_frame, text="替换已有编号", font=self.button_font)
        self.replace_nums_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkButton(self.bottom_frame, text="预览排序", command=lambda: self.preview_changes("numbering"), font=self.button_font, corner_radius=8).grid(row=5, column=3, columnspan=2, padx=(5, 15), pady=5, sticky="ew")

        self.entry_widgets = [self.suffix_entry, self.prefix_entry, self.find_entry, self.replace_entry, self.old_ext_entry, self.new_ext_entry, self.start_num_entry, self.separator_entry]

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path: self.load_folder_data(folder_path)

    def load_folder_data(self, folder_path):
        self.selected_folder = folder_path
        self.undo_log_path = os.path.join(self.selected_folder, ".rename_undo_log.json")
        self.folder_path_label.configure(text=f"{self.selected_folder}")
        try:
            self.file_list = sorted([f for f in os.listdir(self.selected_folder) if os.path.isfile(os.path.join(self.selected_folder, f)) and not f == ".rename_undo_log.json"], key=self.natural_sort_key)
            self.preview_list = {f: f for f in self.file_list}
            self.operations_to_apply = {}
            self.update_preview_display()
            self.status_bar.configure(text=f"已加载 {len(self.file_list)} 个文件。")
            self.undo_button.configure(state="normal" if os.path.exists(self.undo_log_path) else "disabled")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件夹: {e}")
            self.status_bar.configure(text="错误：无法读取文件夹")

    def update_preview_display(self):
        # ... (This method remains the same)
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
        # ... (This method remains the same)
        if not op_details: ctk.CTkLabel(frame, text=new_name, anchor="w", text_color=self.PREVIEW_COLOR).grid(row=0, column=0, sticky='w'); return
        op_type, op_mode, op_params = op_details['type'], op_details['mode'], op_details['params']
        parts = []
        name_to_process = original_name if op_mode == 'remove' else new_name
        if op_mode == 'add':
            value = op_params
            if op_type == 'prefix': parts = [(value, self.HIGHLIGHT_ADD_COLOR), (name_to_process[len(value):], self.PREVIEW_COLOR)]
            elif op_type == 'suffix': name_part, ext_part = os.path.splitext(name_to_process); parts = [(name_part[:-len(value)], self.PREVIEW_COLOR), (value, self.HIGHLIGHT_ADD_COLOR), (ext_part, self.PREVIEW_COLOR)]
        elif op_mode == 'remove':
            value = op_params
            if op_type == 'prefix' and name_to_process.startswith(value): parts = [(value, self.HIGHLIGHT_REMOVE_COLOR), (name_to_process[len(value):], self.PREVIEW_COLOR)]
            elif op_type == 'suffix' and os.path.splitext(name_to_process)[0].endswith(value): name_part, ext_part = os.path.splitext(name_to_process); parts = [(name_part[:-len(value)], self.PREVIEW_COLOR), (value, self.HIGHLIGHT_REMOVE_COLOR), (ext_part, self.PREVIEW_COLOR)]
        elif op_type == 'replace':
            find, replace = op_params; original_name_part, ext_part = os.path.splitext(original_name)
            if find in original_name_part: split_parts = original_name_part.split(find); parts.append((ext_part, self.PREVIEW_COLOR)); [parts.insert(-1, (replace, self.HIGHLIGHT_ADD_COLOR)) or parts.insert(-1, (p, self.PREVIEW_COLOR)) for i, p in enumerate(reversed(split_parts)) if i < len(split_parts) -1 or p]
            else: parts.append((new_name, self.PREVIEW_COLOR))
        elif op_type == 'extension': name_part, ext_part = os.path.splitext(new_name); parts = [(name_part, self.PREVIEW_COLOR), (ext_part, self.HIGHLIGHT_ADD_COLOR)]
        elif op_type == 'numbering':
            start, sep, pos, _ = op_params; num_str = str(start + self.file_list.index(original_name))
            if pos == "前缀": parts = [(num_str + sep, self.HIGHLIGHT_ADD_COLOR), (new_name[len(num_str+sep):], self.PREVIEW_COLOR)]
            else: name_part, ext_part = os.path.splitext(new_name); base_name = name_part.rsplit(sep, 1)[0]; parts = [(base_name, self.PREVIEW_COLOR), (sep + num_str, self.HIGHLIGHT_ADD_COLOR), (ext_part, self.PREVIEW_COLOR)]
        if not parts: parts.append((new_name, self.PREVIEW_COLOR))
        col = 0
        for text, color in parts: 
            if text: ctk.CTkLabel(frame, text=text, anchor="w", text_color=color, font=self.highlight_font if color != self.PREVIEW_COLOR else None).grid(row=0, column=col, sticky='w'); col += 1

    def preview_changes(self, op_type, op_mode=None):
        if not self.selected_folder: messagebox.showwarning("警告", "请先选择一个文件夹！"); return
        self.operations_to_apply = {}
        op_params = None
        if op_type == "numbering":
            try: op_params = (int(self.start_num_entry.get()), self.separator_entry.get(), self.position_menu.get(), self.replace_nums_checkbox.get())
            except ValueError: messagebox.showerror("错误", "起始编号必须是一个整数。"); return
        else: # Other ops
            params_map = {"suffix": self.suffix_entry.get, "prefix": self.prefix_entry.get, "replace": lambda: (self.find_entry.get(), self.replace_entry.get()), "extension": lambda: (self.old_ext_entry.get(), self.new_ext_entry.get())}
            op_params = params_map[op_type]()
        if not any(op_params if isinstance(op_params, tuple) else [op_params]) and op_type != 'replace': messagebox.showwarning("警告", "请输入操作所需的内容！"); return

        for i, original_name in enumerate(self.file_list):
            name_part, ext_part = os.path.splitext(original_name)
            new_preview_name = original_name

            if op_type == "numbering":
                start, sep, pos, replace_existing = op_params
                base_name = original_name
                if replace_existing:
                    # Regex to find leading/trailing numbers followed by common separators
                    match = re.match(r"^(\d+)[_.-]?(.*)", original_name) or re.match(r"^(.*?)[_.-]?(\d+)(\.[^.]+)$", original_name)
                    if match:
                        # Logic to correctly extract base name depending on pattern is complex.
                        # Simple prefix removal for now:
                        if original_name.startswith(str(match.group(1))):
                            base_name = original_name[len(match.group(1)):].lstrip('._- ')
                
                name_part_new, ext_part_new = os.path.splitext(base_name)
                num_str = str(start + i)
                if pos == "前缀": new_preview_name = f"{num_str}{sep}{base_name}"
                else: new_preview_name = f"{name_part_new}{sep}{num_str}{ext_part_new}"
            else: # Previous logic for other operations
                if op_type == "suffix": value = op_params; new_preview_name = f"{name_part}{value}{ext_part}" if op_mode == "add" else (f"{name_part[:-len(value)]}{ext_part}" if name_part.endswith(value) else original_name)
                elif op_type == "prefix": value = op_params; new_preview_name = f"{value}{original_name}" if op_mode == "add" else (original_name[len(value):] if original_name.startswith(value) else original_name)
                elif op_type == "replace": find, replace = op_params; new_preview_name = f"{name_part.replace(find, replace)}{ext_part}" if find and find in name_part else original_name
                elif op_type == "extension": old_ext, new_ext = op_params; old_ext = f".{old_ext.lstrip('.')}"; new_ext = f".{new_ext.lstrip('.')}"; new_preview_name = f"{name_part}{new_ext}" if ext_part.lower() == old_ext.lower() else original_name

            self.preview_list[original_name] = new_preview_name
            if original_name != new_preview_name: self.operations_to_apply[original_name] = {'type': op_type, 'mode': op_mode, 'params': op_params, 'new_name': new_preview_name}
        
        self.update_preview_display(); self.status_bar.configure(text="预览已更新。点击 '应用重命名' 来保存更改。")

    def apply_changes(self):
        if not self.selected_folder or not self.operations_to_apply:
            messagebox.showinfo("提示", "请先选择文件夹并预览更改。")
            return
        if not messagebox.askyesno("确认操作", f"您确定要重命名 {len(self.operations_to_apply)} 个文件吗？\n此操作可通过'撤销'按钮恢复。"):
            return

        # --- Create Undo Log ---
        undo_log = {op['new_name']: original_name for original_name, op in self.operations_to_apply.items()}
        try:
            with open(self.undo_log_path, 'w', encoding='utf-8') as f:
                json.dump(undo_log, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("错误", f"无法写入撤销日志: {e}")
            return

        # --- Two-Phase Rename --- #
        errors = []
        temp_files = [] # Store (temp_path, final_path)

        # Phase 1: Rename to temporary names
        try:
            for original_name, op in self.operations_to_apply.items():
                original_path = os.path.join(self.selected_folder, original_name)
                final_path = os.path.join(self.selected_folder, op['new_name'])
                temp_path = original_path + ".__rename_temp__"

                if not os.path.exists(original_path):
                    errors.append(f"文件在操作前消失: {original_name}")
                    continue
                
                os.rename(original_path, temp_path)
                temp_files.append((temp_path, final_path))

        except Exception as e:
            errors.append(f"严重错误：第一阶段重命名失败: {e}")
            # Attempt to roll back Phase 1 changes
            for temp_path, _ in temp_files:
                original_path = temp_path.replace(".__rename_temp__", "")
                try:
                    os.rename(temp_path, original_path)
                except Exception as rollback_e:
                    errors.append(f"紧急回滚失败: {rollback_e}")
            messagebox.showerror("严重错误", "重命名过程发生严重错误，已尝试回滚。请检查文件列表。\n" + "\n".join(errors))
            self.load_folder_data(self.selected_folder)
            return

        # Phase 2: Rename from temporary to final names
        changed_count = 0
        for temp_path, final_path in temp_files:
            try:
                os.rename(temp_path, final_path)
                changed_count += 1
            except Exception as e:
                errors.append(f"重命名 {os.path.basename(temp_path)} -> {os.path.basename(final_path)} 失败: {e}")

        if errors:
            messagebox.showerror("完成 (有错误)", f"成功: {changed_count}, 失败: {len(errors)}\n" + "\n".join(errors))
        else:
            messagebox.showinfo("完成", f"成功重命名 {changed_count} 个文件。")
        
        for entry in self.entry_widgets:
            entry.delete(0, 'end')
        self.load_folder_data(self.selected_folder)

    def undo_last_rename(self):
        if not self.undo_log_path or not os.path.exists(self.undo_log_path):
            messagebox.showerror("错误", "未找到撤销日志文件。")
            return

        if not messagebox.askyesno("确认撤销", "您确定要撤销上一次的重命名操作吗？"):
            return
        
        try:
            with open(self.undo_log_path, 'r', encoding='utf-8') as f:
                undo_log = json.load(f)
        except Exception as e:
            messagebox.showerror("错误", f"无法读取撤销日志: {e}")
            return

        undone_count, errors = 0, []
        for new_name, original_name in undo_log.items():
            new_path = os.path.join(self.selected_folder, new_name)
            original_path = os.path.join(self.selected_folder, original_name)
            if not os.path.exists(new_path):
                errors.append(f"文件不存在: {new_name}")
                continue
            try:
                os.rename(new_path, original_path)
                undone_count += 1
            except Exception as e:
                errors.append(f"撤销 {new_name} 失败: {e}")

        if errors:
            messagebox.showerror("撤销完成 (有错误)", f"成功撤销: {undone_count}, 失败: {len(errors)}\n" + "\n".join(errors))
        else:
            messagebox.showinfo("撤销完成", f"成功撤销 {undone_count} 个文件。")

        try:
            os.remove(self.undo_log_path)
        except Exception as e:
            messagebox.showwarning("警告", f"无法删除撤销日志文件: {e}")

        self.load_folder_data(self.selected_folder)

if __name__ == "__main__":
    app = App()
    app.mainloop()