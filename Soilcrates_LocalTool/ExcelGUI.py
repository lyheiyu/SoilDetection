import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import pandas as pd


class ExcelMultiSheetGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Excel Multi-Sheet Column Selector & Merger")
        # 稍微给大一点默认窗口
        self.master.geometry("1250x680")

        # 状态
        self.base_dir = os.getcwd()          # 当前目录
        self.file_paths = {}                 # filename -> full path
        self.file_sheets = {}                # filename -> [sheet names]
        self.current_preview_file = None     # 当前预览的文件名
        self.union_columns = []              # 当前选定 sheet 的列名合集

        # 选中的 sheet 名（合并时使用）
        self.selected_sheet_name = tk.StringVar()

        self.create_widgets()
        self.scan_folder()  # 启动时自动扫描一次

    # -------------------- UI -------------------- #
    def create_widgets(self):
        # 顶部：当前目录 + 按钮
        top_frame = ttk.Frame(self.master)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Current folder:").pack(side="left")
        self.lbl_folder = ttk.Label(top_frame, text=self.base_dir, foreground="blue")
        self.lbl_folder.pack(side="left", padx=5)

        btn_refresh = ttk.Button(top_frame, text="Refresh", command=self.scan_folder)
        btn_refresh.pack(side="right", padx=5)

        btn_change_folder = ttk.Button(top_frame, text="Change folder", command=self.change_folder)
        btn_change_folder.pack(side="right", padx=5)

        # 中上：选择 sheet（此处只显示当前选中文件的 sheets）
        sheet_frame = ttk.Frame(self.master)
        sheet_frame.pack(fill="x", padx=10, pady=(0, 5))

        ttk.Label(sheet_frame, text="Sheet to use (of selected file):").pack(side="left")
        self.combo_sheet = ttk.Combobox(
            sheet_frame,
            textvariable=self.selected_sheet_name,
            state="readonly",
            width=30,
        )
        self.combo_sheet.pack(side="left", padx=5)
        self.combo_sheet.bind("<<ComboboxSelected>>", self.on_sheet_change)

        # 主区域：左文件列表，中预览，右列名选择
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 左侧：文件列表
        files_frame = ttk.LabelFrame(main_frame, text="Excel files (.xlsx)")
        files_frame.pack(side="left", fill="y", padx=(0, 5), pady=5)

        self.list_files = tk.Listbox(files_frame, width=35, height=25, exportselection=False)
        self.list_files.pack(side="left", fill="y", padx=5, pady=5)
        self.list_files.bind("<<ListboxSelect>>", self.on_file_select)

        scrollbar_files = ttk.Scrollbar(files_frame, orient="vertical", command=self.list_files.yview)
        scrollbar_files.pack(side="right", fill="y")
        self.list_files.config(yscrollcommand=scrollbar_files.set)

        # 中：预览（加上水平滚动条） # NEW
        preview_frame = ttk.LabelFrame(main_frame, text="Preview (selected sheet, first rows)")
        preview_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 用一个 frame 包一下 Treeview 和滚动条
        preview_inner = ttk.Frame(preview_frame)
        preview_inner.pack(fill="both", expand=True)

        self.tree_preview = ttk.Treeview(preview_inner, show="headings")
        self.tree_preview.grid(row=0, column=0, sticky="nsew")

        # 垂直滚动条
        scrollbar_preview_y = ttk.Scrollbar(preview_inner, orient="vertical", command=self.tree_preview.yview)
        scrollbar_preview_y.grid(row=0, column=1, sticky="ns")

        # 水平滚动条 # NEW
        scrollbar_preview_x = ttk.Scrollbar(preview_inner, orient="horizontal", command=self.tree_preview.xview)
        scrollbar_preview_x.grid(row=1, column=0, sticky="ew")

        self.tree_preview.config(
            yscrollcommand=scrollbar_preview_y.set,
            xscrollcommand=scrollbar_preview_x.set,  # NEW
        )

        # 让内部 frame 可以自适应
        preview_inner.rowconfigure(0, weight=1)
        preview_inner.columnconfigure(0, weight=1)

        # 右侧：列名列表 + 合并按钮（加水平滚动） # NEW
        columns_frame = ttk.LabelFrame(main_frame, text="Columns (from selected sheet across all files)")
        columns_frame.pack(side="left", fill="y", padx=(5, 0), pady=5)

        columns_inner = ttk.Frame(columns_frame)
        columns_inner.pack(fill="y", expand=False)

        self.list_columns = tk.Listbox(
            columns_inner,
            selectmode="extended",   # 多选
            width=35,
            height=20,
            exportselection=False,
        )
        self.list_columns.grid(row=0, column=0, sticky="ns")

        scrollbar_cols_y = ttk.Scrollbar(columns_inner, orient="vertical", command=self.list_columns.yview)
        scrollbar_cols_y.grid(row=0, column=1, sticky="ns")

        scrollbar_cols_x = ttk.Scrollbar(columns_inner, orient="horizontal", command=self.list_columns.xview)
        scrollbar_cols_x.grid(row=1, column=0, sticky="ew")

        self.list_columns.config(
            yscrollcommand=scrollbar_cols_y.set,
            xscrollcommand=scrollbar_cols_x.set,  # NEW
        )

        btn_merge = ttk.Button(columns_frame, text="Merge selected columns", command=self.merge_selected_columns)
        btn_merge.pack(side="bottom", pady=10)

        # 底部：日志
        log_frame = ttk.LabelFrame(self.master, text="Log")
        log_frame.pack(fill="both", expand=False, padx=10, pady=(0, 10))

        self.txt_log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=6)
        self.txt_log.pack(fill="both", expand=True, padx=5, pady=5)

    # -------------------- Utils -------------------- #
    def log(self, message: str):
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)
        print(message)

    def change_folder(self):
        new_dir = filedialog.askdirectory(initialdir=self.base_dir, title="Select folder with Excel files")
        if new_dir:
            self.base_dir = new_dir
            self.lbl_folder.config(text=self.base_dir)
            self.scan_folder()

    # -------------------- Scan & Sheet Handling -------------------- #
    def scan_folder(self):
        """扫描当前目录下所有 .xlsx 文件，记录其路径和 sheet 名。"""
        self.log(f"Scanning folder: {self.base_dir}")
        self.file_paths.clear()
        self.file_sheets.clear()
        self.list_files.delete(0, tk.END)
        self.clear_preview()
        self.list_columns.delete(0, tk.END)
        self.union_columns.clear()
        self.combo_sheet["values"] = []
        self.selected_sheet_name.set("")

        excel_files = [
            f for f in os.listdir(self.base_dir)
            if f.lower().endswith(".xlsx")
        ]

        if not excel_files:
            self.log("No .xlsx files found in this folder.")
            messagebox.showwarning("No Excel files", "No .xlsx files found in this folder.")
            return

        for fname in sorted(excel_files):
            full_path = os.path.join(self.base_dir, fname)
            self.file_paths[fname] = full_path
            self.list_files.insert(tk.END, fname)

            try:
                xls = pd.ExcelFile(full_path, engine="openpyxl")
                sheets = list(xls.sheet_names)
                self.file_sheets[fname] = sheets
                self.log(f"{fname}: sheets = {sheets}")
            except Exception as e:
                self.log(f"Error reading sheets from {fname}: {e}")

        self.log(f"Total {len(self.file_paths)} Excel file(s) found.")

        # 默认选中第一个文件
        if self.file_paths:
            self.list_files.selection_clear(0, tk.END)
            self.list_files.selection_set(0)
            self.on_file_select(None)

    def on_file_select(self, event):
        """当用户选择某个文件时：更新 sheet 下拉框，只显示该文件的 sheets。"""
        selection = self.list_files.curselection()
        if not selection:
            return
        idx = selection[0]
        fname = self.list_files.get(idx)
        full_path = self.file_paths.get(fname)
        if not full_path:
            return

        self.current_preview_file = fname
        sheets = self.file_sheets.get(fname, [])

        # 更新下拉框为当前文件的 sheets
        self.combo_sheet["values"] = sheets

        if sheets:
            prev_sheet = self.selected_sheet_name.get()
            if prev_sheet not in sheets:
                self.selected_sheet_name.set(sheets[0])
        else:
            self.selected_sheet_name.set("")

        # 根据当前选定的 sheet 构建列合集
        self.build_union_for_sheet()

        # 显示当前文件的预览
        self.show_file_preview(full_path)

    def on_sheet_change(self, event=None):
        """当用户在下拉框中切换 sheet 时，重新构建列合集 & 刷新当前文件预览。"""
        self.build_union_for_sheet()

        selection = self.list_files.curselection()
        if selection:
            idx = selection[0]
            fname = self.list_files.get(idx)
            full_path = self.file_paths.get(fname)
            if full_path:
                self.show_file_preview(full_path)

    def build_union_for_sheet(self):
        """根据当前选定的 sheet 名，读取各文件该 sheet 的表头，汇总列名。"""
        sheet_name = self.selected_sheet_name.get()
        if not sheet_name:
            return

        self.log(f"Building union of columns for sheet: {sheet_name}")
        self.union_columns.clear()
        self.list_columns.delete(0, tk.END)

        for fname, full_path in self.file_paths.items():
            sheets = self.file_sheets.get(fname, [])
            if sheet_name not in sheets:
                continue
            try:
                df_header = pd.read_excel(full_path, sheet_name=sheet_name, nrows=0, engine="openpyxl")
                cols = [str(c) for c in df_header.columns]
                for c in cols:
                    if c not in self.union_columns:
                        self.union_columns.append(c)
            except Exception as e:
                self.log(f"Error reading header from {fname} [{sheet_name}]: {e}")

        for col in self.union_columns:
            self.list_columns.insert(tk.END, col)

        self.log(f"Union columns for sheet '{sheet_name}': {len(self.union_columns)} column(s).")

    def clear_preview(self):
        for col in self.tree_preview["columns"]:
            self.tree_preview.heading(col, text="")
        self.tree_preview["columns"] = ()
        for row in self.tree_preview.get_children():
            self.tree_preview.delete(row)

    # -------------------- Preview -------------------- #
    def show_file_preview(self, file_path):
        """预览当前选定 sheet 的前 50 行。"""
        sheet_name = self.selected_sheet_name.get()
        if not sheet_name:
            messagebox.showwarning("No sheet selected", "Please select a sheet name first.")
            return

        self.log(f"Previewing file: {os.path.basename(file_path)} [sheet: {sheet_name}]")
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=50, engine="openpyxl")
        except ValueError as ve:
            self.log(f"Sheet '{sheet_name}' not found in {os.path.basename(file_path)}: {ve}")
            messagebox.showwarning(
                "Sheet not found",
                f"Sheet '{sheet_name}' not found in file:\n{os.path.basename(file_path)}"
            )
            return
        except Exception as e:
            self.log(f"Error reading file for preview: {e}")
            messagebox.showerror("Preview error", f"Error reading file:\n{e}")
            return

        self.clear_preview()

        if df.empty:
            self.log("File or sheet has no rows.")
            return

        cols = [str(c) for c in df.columns]
        self.tree_preview["columns"] = cols

        # 设置列标题，并给一个初始宽度（可以鼠标拖动调整） # NEW
        for col in cols:
            self.tree_preview.heading(col, text=col)
            self.tree_preview.column(col, width=120, stretch=True)

        for _, row in df.iterrows():
            values = [row[col] for col in cols]
            self.tree_preview.insert("", tk.END, values=values)

    # -------------------- Merge -------------------- #
    def merge_selected_columns(self):
        """从所有包含当前 sheet 的文件中，提取所选列合并输出。"""
        sheet_name = self.selected_sheet_name.get()
        if not sheet_name:
            messagebox.showwarning("No sheet selected", "Please select a sheet name for merging.")
            return

        selected_indices = self.list_columns.curselection()
        if not selected_indices:
            messagebox.showwarning("No columns selected", "Please select at least one column to merge.")
            return

        selected_columns = [self.list_columns.get(i) for i in selected_indices]
        self.log(f"Selected columns for merge (sheet={sheet_name}): {selected_columns}")

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save merged Excel as"
        )
        if not output_path:
            return

        all_dfs = []

        for fname, full_path in self.file_paths.items():
            sheets = self.file_sheets.get(fname, [])
            if sheet_name not in sheets:
                self.log(f"Skipping {fname}: sheet '{sheet_name}' not found.")
                continue

            self.log(f"Reading for merge: {fname} [sheet: {sheet_name}]")
            try:
                df = pd.read_excel(full_path, sheet_name=sheet_name, engine="openpyxl")
            except Exception as e:
                self.log(f"Error reading {fname}: {e}")
                messagebox.showerror("Read error", f"Error reading {fname}:\n{e}")
                return

            # 确保所有选定列都存在，没有的列补 NaN
            for col in selected_columns:
                if col not in df.columns:
                    df[col] = pd.NA

            df_selected = df[selected_columns].copy()
            df_selected["SourceFile"] = fname
            all_dfs.append(df_selected)

        if not all_dfs:
            messagebox.showerror("Merge error", "No data to merge for the selected sheet.")
            return

        try:
            merged_df = pd.concat(all_dfs, ignore_index=True)
            merged_df.to_excel(output_path, index=False)
            self.log(f"Merged file saved to: {output_path}")
            messagebox.showinfo("Success", f"Merged Excel saved to:\n{output_path}")
        except Exception as e:
            self.log(f"Error during merge: {e}")
            messagebox.showerror("Merge error", f"Error during merge:\n{e}")


def main():
    root = tk.Tk()
    app = ExcelMultiSheetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
