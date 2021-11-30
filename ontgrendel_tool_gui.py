import logging
import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, filedialog
import _functions.unzip_files as uz
import _functions.unlock_file as uf
import _functions.check_length as cl

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                    filename='Logging_UnlockTool.log'
                    )  # to see log in console remove filename


class Application(tk.Frame):
    """
    This class is a python gui to unlock pdf files.
    Provides functionality such as:
    - Selecting de file location (including unzipping of zip files)
    - Determining the amount of pdf files available for unlocking
    - Unlocking pdf files
    - Determining the amount of unlocked files
    - Making a log file where all the steps can be followed and errors can be traced

    Author: Joana Cardoso
    """

    logging.info('Starting Tool')

    def __init__(self, parent):
        """
        This function initializes the tool and sets up a start screen.
        """

        root.withdraw()
        self.progress = None
        self.style = None
        self.single_file = False
        tk.Frame.__init__(self, master=parent)
        info = 'Deze applicatie ontgrendeld beveiligd PDF bestanden.\n\nSelecteer een bestand of map met bestanden om te ontgrendelen \
vanaf je lokale laptop of OneDrive omgeving.\n\nDeze applicatie is ontwikkeld door het vDWH team van de Provincie Zuid-Holland.'
        self.parent = parent
        parent.iconbitmap('logo.ico')
        messagebox.showinfo(title=None, message=info)
        self.folder_type()

    def folder_type(self):
        """
        This function sets up a screen to select the location of the pdf documents for unlocking.
        Possibilities are: single file, folder or zip file. 
        """

        self.parent = tk.Tk()
        w = self.parent.winfo_reqwidth()
        h = self.parent.winfo_reqheight()
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws / 2.3) - (w / 2.3)
        y = (hs / 2) - (h / 2)
        self.parent.geometry('+%d+%d' % (x, y))
        self.parent.iconbitmap('logo.ico')
        self.parent.title('Bestand type')
        text = 'Wat wil je selecteren?'
        self.parent.resizable(width="false", height="false")
        self.parent.minsize(width=250, height=75)
        self.parent.maxsize(width=250, height=75)
        self.label = tk.Label(self.parent, text=text).place(
            relx=.1, rely=.2, anchor="w")
        self.button2 = tk.Button(self.parent, text='Map', command=self.select_folder).place(
            relx=.38, rely=.7, anchor="c")
        self.button3 = tk.Button(self.parent, text='Zip-bestand',
                                 command=self.select_zip).place(relx=.60, rely=.7, anchor="c")
        self.quit = tk.Button(self.parent, text='Stoppen', command=self.cancel).place(
            relx=.86, rely=.7, anchor="c")
        self.parent.protocol("WM_DELETE_WINDOW", self.cancel)

    def select_zip(self):
        """
        If the option zip file is selected in the folder_type screen, this function calls _functions.unzip_file.unzip_files and 
            gets the path to the selected file.

        self.zip_dir is the path to the selected zip file
        self.process_dir is the directory of the new unzipped folder
        """

        self.parent.destroy()
        zip_dir = filedialog.askopenfilename(initialdir="/Users", title="Zip-bestand selectie",
                                             filetypes=(("ZIP files", "*.ZIP"), ("zip files", "*.zip")))
        if not zip_dir:
            logging.info('Back to select folder type')
            self.folder_type()

        else:
            self.zip_dir = os.path.abspath(zip_dir)
            self.process_dir = os.path.abspath(os.path.splitext(zip_dir)[0])
            logging.info(f'Zip_dir: {zip_dir}')
            logging.info(f'Process directory: {self.process_dir}')
            logging.info(f'Started unzipping folder: {zip_dir}')
            uz.unzip_files(self.zip_dir, self.process_dir)
            self.find_pdf_files()

    def select_folder(self):
        """
        If the option folder is selected in the folder_type screen, this function gets the path to the selected folder.
        It calls the function check_length in file _functions.check_length.
        If necessary calls the function unzip_files in file _functions.unzip_file.

        self.process_dir is the directory of the selected folder
        """

        self.parent.destroy()
        process_dir = filedialog.askdirectory(
            initialdir="/Users", title="Map selectie")

        if not process_dir:
            logging.info('Back to select folder type')
            self.folder_type()

        else:
            self.process_dir = os.path.abspath(process_dir)
            logging.info(f'Process directory: {self.process_dir}')
            for root, dirs, files in os.walk(self.process_dir):
                for file in files:
                    des_dir = os.path.join(root, os.path.dirname(file))
                    file_path = os.path.join(root, file)
                    logging.info(f'File: {file}')
                    logging.info(f'Destination directory: {des_dir}')
                    file_name, long_name = cl.check_length(
                        des_dir=des_dir, file=file)

                    if long_name == True:
                        logging.info(f'Long name')
                        try:
                            os.rename(file_path, file_name)
                            logging.debug(
                                f'Changing name: {file} into {file_name}')
                        except:
                            logging.error(
                                f'Failed to change name: {file} into {file_name}')
                    name_lower = file.lower()
                    if name_lower.endswith('.zip'):
                        zip_dir = os.path.join(root, file)
                        proc_zip = os.path.abspath(
                            os.path.splitext(zip_dir)[0])
                        logging.info(f'Zip_dir: {zip_dir}')
                        logging.info(f'Proc dir: {proc_zip}')
                        uz.unzip_files(zip_dir, proc_zip)
                        try:
                            os.remove(zip_dir)
                            logging.debug(f'Removed zip: {zip_dir}')
                        except:
                            logging.error(f'Failed to remove zip: {zip_dir}')
            self.find_pdf_files()

    def find_pdf_files(self):
        """
        This function gets the amount of pdf files found in the selected folder or zip file and presents the results in a screen.
        Options are: Continue or stop.

        self.files_to_unlock is an array with path to the found files
        self.empty_dir is an array with the path to empty folders. If empty folder exist they wil be kept in the output directory.
        self.process_dir is the directory of the selected files
        self.pdf_files is the number of pdf's found in the process_dir
        """

        logging.info('Find pdf files')

        # count pdf files
        self.files_to_unlock = []
        self.pdf_files = 0
        self.empty_dir = []
        for root, dirs, files in os.walk(self.process_dir):
            if not len(dirs) and not len(files):
                # Adding the empty directory to list
                self.empty_dir.append(root)
            for name in files:
                name_lower = name.lower()
                if name_lower.endswith(".pdf"):
                    self.pdf_files += 1
                    self.files_to_unlock.append(os.path.join(root, name))

        # print messages
        total_pdfs_unlock = 'Gevonden PDF\'s: ' + str(self.pdf_files)

        self.parent = tk.Tk()
        w = self.parent.winfo_reqwidth()
        h = self.parent.winfo_reqheight()
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws / 2.3) - (w / 2.3)
        y = (hs / 2) - (h / 2)
        self.parent.geometry('+%d+%d' % (x, y))
        self.parent.iconbitmap('logo.ico')
        self.parent.title('Gevonden PDF\'s')
        self.parent.resizable(width="false", height="false")
        self.parent.minsize(width=275, height=100)
        self.parent.maxsize(width=275, height=100)
        self.label = tk.Label(self.parent, text=total_pdfs_unlock).place(
            relx=.1, rely=.2, anchor="w")
        self.doorgaan = tk.Button(self.parent, text='Doorgaan', command=self.process_pdf).place(relx=.63,
                                                                                                rely=.7, anchor="c")
        self.quit = tk.Button(self.parent, text='Stoppen', command=self.cancel).place(
            relx=.86, rely=.7, anchor="c")
        self.parent.protocol("WM_DELETE_WINDOW", self.cancel)

    def open_folder(self, path: str):
        """
        Function that opens the link to the unloked files in the last screen.
        """

        os.startfile(path, 'open')

    def process_pdf(self):
        """
        This function unlocks pdf files, counts the unloked files and presents the results in a final screen.
        Calls the function unlock_pdf in file _functions.unlock_file

        self.single_file sets the value for the use of a single file or not
        out_dir sets the path to the output directory (where unlocked files will be placed)
        self.files_to_unlock is an array with path to the found files
        self.empty_dir is an array with the path to empty folders. If there exist they wil be kept in the output directory
        unlocked_pdfs gives the number of unlocked files

        """
        if not self.single_file:
            self.parent.destroy()
            # set output directory
            out_dir = os.path.join(os.path.dirname(
                self.process_dir), os.path.basename(self.process_dir) + '_ontgrendeld')
            logging.info(f'Output directory: {out_dir}')
        else:
            out_dir = self.process_dir
            logging.info(f'Output directory: {out_dir}')

        uf.unlock_pdf(files_to_unlock=self.files_to_unlock,
                      process_dir=self.process_dir, out_dir=out_dir, single_file=self.single_file)
        logging.info('Finished unlocking PDF files')

        # make empty directories if they exist in the original directory
        if len(self.empty_dir) > 0:
            logging.info('Started creating empty directories')
            for emp_dir in self.empty_dir:
                create_emp_dir = emp_dir.replace(self.process_dir, out_dir)
                try:
                    # Create empty directory in output dir
                    Path(create_emp_dir).mkdir(parents=True, exist_ok=True)
                    logging.debug(
                        f'Creating empty directory: {create_emp_dir}')
                except:
                    logging.error(
                        f'Failed to create empty directory: {create_emp_dir}')
            logging.info('Finished creating empty directories')

        # count unlocked PDF's
        unlocked_pdfs = 0

        for root, dirs, files in os.walk(out_dir):
            for name in files:
                name_lower = name.lower()
                if name_lower.endswith('.pdf'):
                    unlocked_pdfs += 1
        if self.single_file:
            unlocked_pdfs = unlocked_pdfs - self.pdf_files

        # print messages
        klaar = 'Klaar met het ontgrendelen van PDF bestanden.'
        total_unlocked = 'Aantal ontgrendelde bestanden: ' + str(unlocked_pdfs)
        output = 'Ontgrendelde PDF bestanden zijn in map: ' + out_dir
        output2 = 'Let op: Kijk of het ontgrendelen goed is gelukt.'

        self.parent = tk.Tk()
        w = self.parent.winfo_reqwidth()
        h = self.parent.winfo_reqheight()
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws / 3) - (w / 3)
        y = (hs / 2.3) - (h / 2.3)
        self.parent.geometry('+%d+%d' % (x, y))
        self.parent.iconbitmap('logo.ico')
        self.parent.title('Ontgrendelde bestanden')
        self.parent.resizable(width="false", height="false")
        self.parent.minsize(width=800, height=150)
        self.parent.maxsize(width=800, height=150)
        self.label = tk.Label(self.parent, text=klaar).place(
            relx=.03, rely=.1, anchor="w")
        self.label = tk.Label(self.parent, text=total_unlocked).place(
            relx=.03, rely=.25, anchor="w")

        # Define clickable labels
        label1 = tk.Label(self.parent, text=output, fg='blue', cursor='hand2')
        label1.pack()
        label1.bind("<Button-1>", lambda e: self.open_folder(out_dir))
        self.label1 = label1.place(relx=.03, rely=.6, anchor="w")

        self.label = tk.Label(self.parent, text=output2).place(
            relx=.03, rely=.4, anchor="w")

        self.quit = tk.Button(self.parent, text='Sluiten', command=self.ready).place(
            relx=.95, rely=.8, anchor="c")
        self.parent.protocol("WM_DELETE_WINDOW", self.ready)

    def tool_destroy(self):
        """
        Function that destroys the tool if file/folder selection is canceled.
        """
        root.destroy()

    def cancel(self):
        """
        Function that cancels the tool and inserts info in the log file if the process is stopped half-way.
        """

        self.parent.destroy()
        self.parent.quit()
        logging.shutdown()
        logging.info('Tool cancelled')

    def ready(self):
        """
        Function that stops the tool and inserts info in the log file when the process is ended.
        """

        self.parent.destroy()
        self.parent.quit()
        logging.shutdown()
        logging.info('Ready with tool')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
