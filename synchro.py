from shutil import copytree, copy2
import os
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz
import logging
import filecmp 


class Synchro(object):
    def __init__(self, source_folder, destination_folder, log_file_path):
        
        self.source_folder = os.path.abspath(source_folder)
        self.destination_folder = os.path.abspath(destination_folder)
        self.log_file_path = os.path.abspath(log_file_path)
        self.copyfiles = None
        self.sched = BlockingScheduler(timezone=pytz.timezone('Europe/Berlin'))
        self.logging = logging
        
    def initial_copy(self):
        self.copyfiles = copytree(self.source_folder, self.destination_folder, symlinks=True, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False)

    def log_path_folder(self):
        self.logging.basicConfig(filename=self.log_file_path, level=logging.DEBUG,format="%(asctime)s %(message)s")
        self.logging.debug("Logging test...")
        self.logging.info("The program is working as expected")
        self.logging.warning("The program may not function properly")
        self.logging.error("The program encountered an error")
        self.logging.critical("The program crashed")
             
    def synchronise(self):
        print('Tick! The time is: %s' % datetime.now())
        self.compare_directories(self.source_folder, self.destination_folder)

    def compare_directories(self, left, right):
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self.compare_directories(os.path.join(left, d), os.path.join(right, d))
        if comparison.left_only:
            self.copy_files(comparison.left_only, left, right)
        left_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                left_modified = os.stat(os.path.join(left, d)).st_mtime
                right_modified = os.stat(os.path.join(right, d)).st_mtime
                if left_modified > right_modified:
                    left_newer.append(d)
            self.copy_files(left_newer, left, right)

    def copy_files(self, file_list, src, dest):
        for file in file_list:
            srcpath = os.path.join(src, os.path.basename(file))
            if os.path.isdir(srcpath):
                shutil.copytree(srcpath, os.path.join(dest, os.path.basename(file)))
                print('Copied directory \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
                self.logging.info('the file was copied with success from the source_folder to the destination folder')
            else:
                shutil.copy2(srcpath, dest)
                print('Copied \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
                self.logging.info('the file was copied with success from the source_folder to the destination folder')
             
    def periodic_save(self):
        self.sched.add_job(self.synchronise,'interval', seconds=20)
        self.sched.start()