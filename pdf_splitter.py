import os
import pathlib
import sys
import tkinter
import tkinter.filedialog
from tkinter import messagebox
from typing import Union

import pypdf


def select_pdf():
    file_path = tkinter.filedialog.askopenfilename()

    if len(file_path) != 0:
        # ファイルが選択された場合
        if file_path[-4:] in [".pdf", "PDF"]:
            return file_path
        else:
            messagebox.showerror('エラー', 'PDFファイルを選択してください')
            return select_pdf()

    else:
        # ファイル選択がキャンセルされた場合
        return None

def select_dir()  -> Union[None, str]:
    dir_path = tkinter.filedialog.askdirectory()

    if len(dir_path) != 0:
        # ファイルが選択された場合
        return dir_path
    else:
        # ファイル選択がキャンセルされた場合
        return None


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # アプリのタイトル
        self.title("PDF分割")
        self.pdf_path = None
        self.output_dir = None

        # テキスト表示キャンバスの作成と配置
        self.text_canvas = tkinter.Canvas(
            self,
            width=900,
            height=300,
            bg="#D0D0D0"
        )
        self.text_canvas.pack()

        self.update_view()

        self.info_label = tkinter.Label(
            self,
            text='',
            bg="#D0D0D0"
        )
        self.info_label.place(x=150, y=160)
        self.update_info('PDFファイルと出力フォルダを選択')

        # 読み込みボタンの作成と配置
        self.select_pdf_button = tkinter.Button(
            self,
            text='ファイル読み込み',
            command=self.select_pdf_button_func
        )
        self.select_pdf_button.pack()

        self.select_output_dir_button = tkinter.Button(
            self,
            text='出力先フォルダを選択',
            command=self.select_output_dir_button_func
        )
        self.select_output_dir_button.pack()

        self.start_process_button = tkinter.Button(
            self,
            text='処理開始',
            command=self.process
        )
        self.start_process_button.pack()


    def select_pdf_button_func(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        self.pdf_path = select_pdf()
        self.update_view()

    def select_output_dir_button_func(self):
        '読み込みボタンが押された時の処理'

        # ファイルを読み込み
        self.output_dir = select_dir()
        self.update_view()

    def process(self):
        if self.pdf_path is None:
            messagebox.showerror('エラー', 'PDFファイルを選択してください')
            return 1
        else:
            pdf_basename = os.path.basename(self.pdf_path)[:-4]
        if self.output_dir is None:
            messagebox.showerror('エラー', '出力先フォルダを選択してください')
            return 1
        else:
            output_dir_path = pathlib.Path(self.output_dir) / pdf_basename

        self.update_info('処理中……')
        reader= pypdf.PdfReader(self.pdf_path)
        os.makedirs(output_dir_path, exist_ok=True)

        for i, page in enumerate(reader.pages):
            save_name =  output_dir_path / f"page_{i:03}.pdf"
            writer = pypdf.PdfWriter()
            pdfOutput = open(save_name, 'wb')
            writer.add_page(page)
            writer.write(pdfOutput)
            pdfOutput.close()
        app.after(1)
        self.update_info('処理完了')

        ret = messagebox.askyesno('確認', '別のpdfも分割しますか？')
        if ret == True:
            self.update_info('PDFファイルと出力フォルダを選択')
            self.pdf_path = None
            self.output_dir = None
            self.update_view()
        else:
            sys.exit()

    def update_view(self):
        if self.pdf_path is None:
            Static1 = tkinter.Label(text='選択中のpdf: ')
            Static1.place(x=150, y=80)

        else:
            Static1 = tkinter.Label(text=f'選択中のpdf: {self.pdf_path}')
            Static1.place(x=150, y=80)

        if self.output_dir is None:
            Static2 = tkinter.Label(text='出力先: ')
            Static2.place(x=150, y=120)

        else:
            Static2 = tkinter.Label(text=f'出力先: {self.output_dir}')
            Static2.place(x=150, y=120)
        self.update()

    def update_info(self, message):
        self.info_label["text"] = message
        self.update()



# GUIアプリ生成
app = Application()
app.mainloop()