import logging
import os

"""
    This file is called from the main file ontgrendel_tool_gui and from the file _functions.unzip_files
    
    Author: Joana Cardoso
"""

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                    filename='Logging_UnlockTool.log'
                    )  # to see log in console remove filename


def check_length(des_dir: str, file: str):
    """
    This function checks the length of selected files.

    des_dir is the path to the destination directory
    file is the path to the file
    filename is the name of the file

    @return file_name the name to be saved in case it has a too long name
    @return long_name is True if the name is too long, default is False
    """

    logging.info(f'Checking length')
    counter = 1
    long_name = False

    if len(os.path.join(des_dir, file)) > 246:
        long_name = True
        logging.info(f'Long name:{long_name}')
        try:
            lastChunk = os.path.basename(file)
            max_length = len(
                lastChunk) - (len(os.path.join(des_dir, os.path.basename(file))) - 242)
            logging.info(f'Max length:{max_length}')
            fileName, fileExtension = os.path.splitext(lastChunk)
            logging.info(f'File name: {fileName}')
            logging.info(f'File extension: {fileExtension}')
            file_name = os.path.join(des_dir, fileName.replace(fileName, fileName[
                :max_length]) + fileExtension)
            logging.debug(f'Shortening name: {file} into {file_name}')
            logging.info(
                f'Path length: {len(os.path.join(des_dir, os.path.basename(file)))}')
        except:
            logging.error(f'Failed to shorten name: {file} into {file_name}')
        if os.path.exists(file_name):
            try:
                file_name = os.path.join(des_dir, fileName.replace(fileName, fileName[
                    :max_length]) + "_" + str(
                    counter) + fileExtension)
                counter += 1
                logging.debug(f'Renaming: {file} into {file_name}')
            except:
                logging.error(f'Failed to rename: {file} into {file_name}')
    else:
        file_name = os.path.join(des_dir, file)

    return file_name, long_name
