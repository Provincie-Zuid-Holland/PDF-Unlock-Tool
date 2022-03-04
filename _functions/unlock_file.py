import logging
import os
import pikepdf
from pikepdf import _cpphelpers #uncomment in py file when making exe with pyinstaller
import subprocess
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import ttk

"""
    This file is called from the main file PDF_unlock_tool.py. It is used to unlock pdf files and save status in a log file.
    
    Author: Joana Cardoso
"""

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                    filename='Logging_UnlockTool.log'
                    )  # to see log in console remove filename


def unlock_pdf(files_to_unlock, process_dir, out_dir):
    """
    Unlocks pdf files and saves the unlocked files in a new directory or with a new name (in case of a single selected file).

    Parameters
    ----------
    files_to_unlock: str
        The pdf files found in the origin(process) directory
    process_dir: str
        The directory of the selected folder
    out_dir: str 
        The output directory where converted files will be placed
        is an array with path to the selected files
    """

    # create progress bar
    parent = tk.Tk()
    w = parent.winfo_reqwidth()
    h = parent.winfo_reqheight()
    ws = parent.winfo_screenwidth()
    hs = parent.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    parent.geometry('+%d+%d' % (x, y))
    parent.iconbitmap('logo.ico')
    parent.title('')

    style = ttk.Style(parent)
    style.layout('text.Horizontal.TProgressbar',
                 [('Horizontal.Progressbar.trough',
                   {'children': [('Horizontal.Progressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'}),
                  ('Horizontal.Progressbar.label', {'sticky': ''})])

    progress = ttk.Progressbar(
        parent,
        orient=tk.HORIZONTAL,
        mode="determinate",
        length=300,
        maximum=100,
        style='text.Horizontal.TProgressbar'
    )
    progress.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    label = ttk.Label(parent, text='Unlocking pdf\'s')
    label.grid(row=2, column=1, pady=5, padx=5, sticky='nswe')
    button = ttk.Button(parent, text='Stop', command=lambda: [parent.destroy(),
                                                                 parent.quit(),
                                                                 logging.shutdown(),
                                                                 logging.info('Tool cancelled')])
    button.grid(row=3, column=2, pady=5, padx=5, sticky='e')
    parent.protocol("WM_DELETE_WINDOW", lambda: [parent.destroy(),
                                                 parent.quit(),
                                                 logging.shutdown(),
                                                 logging.info('Tool cancelled')])

    # set start value PDF unlock
    progress['value'] = 1
    label.configure(text="Busy unlocking pdf\'s")
    style.configure('text.Horizontal.TProgressbar',
                    text='{:g} %'.format(progress['value']))

    # start unloking pdf's
    logging.info('Started unlocking PDF files')

    for file in files_to_unlock:
        # create output directory/subdirectory
        file_out = file.replace(process_dir, out_dir)
        logging.info(f'file_out: {file_out}')
        root_dir = os.path.dirname(file_out)
        try:
            Path(root_dir).mkdir(parents=True, exist_ok=True)  ## Create output dir
            logging.debug(f'Creating output directory: {root_dir}')
        except:
            logging.error(f'Failed to create output directory: {root_dir}')

        # Open pdf and save with pikepdf to get rid of any write protections
        # Copy to tempdir since input file cannot be overwritten
        temp_dir = tempfile.gettempdir()
        cmd = 'copy "%s" "%s"' % (file, temp_dir)
        try:
            subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
            pdf_file = os.path.join(
                temp_dir, os.path.basename(file))  # path to tempfile
            pdf = pikepdf.open(pdf_file)  # Open tempfile
            if 'Metadata' in pdf.Root.keys():  # if PDF metadata is present, delete it
                try:
                    del pdf.Root.Metadata
                    logging.debug(f'Deleting metadata from file: {file}')
                except:
                    logging.error(
                        f'Failed to delete metadata from file: {file}')
            pdf.save(file_out)  # Save processed pdf
            logging.debug(f'Resave PDF file: {file_out}')
        except:
            logging.error(f'Failed to resave PDF file: {file_out}')

        # set progress bar max value
        progress['value'] += 99 / \
            len(files_to_unlock) if len(files_to_unlock) > 0 else 99
        progress.update()
        progress.update_idletasks()
        style.configure(
            'text.Horizontal.TProgressbar',
            text='{:.0f} %'.format(progress['value'])
        )

    parent.destroy()
