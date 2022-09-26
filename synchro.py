from shutil import copytree, copy2
import os
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz
import logging
import filecmp 


class Synchro(object):
    def __init__(self, source_folder, destination_folder, log_file_path, synchronisation_content):
        
        self.source_folder = os.path.abspath(source_folder)
        self.destination_folder = os.path.abspath(destination_folder)
        self.log_file_path = os.path.abspath(log_file_path)
        self.copyfiles = None
        self.sched = BlockingScheduler(timezone=pytz.timezone('Europe/Berlin'))
        self.synchronisation_content = synchronisation_content
        self.logging = logging
        self.logging.basicConfig(filename=self.log_file_path, level=logging.DEBUG,format="%(asctime)s %(message)s")
        
    def initial_copy(self):
        self.copyfiles = copytree(self.source_folder, self.destination_folder, symlinks=True, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False)
        self.logging.info("Initial copy from folder" + self.source_folder + " to destination folder" + self.destination_folder)
 
    def synchronise(self):
        print('Tick! The time is: %s' % datetime.now())
        self.compare_files_directories(self.source_folder, self.destination_folder)
        self.logging.info("informations from folder" + self.source_folder + " are synchronize with success to destination folder" + self.destination_folder)
        
    def compare_files_directories(self, left, right):
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for dir in comparison.common_dirs:
                self.compare_files_directories(os.path.join(left, dir), os.path.join(right, dir))
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
                self.logging.info('Copied directory \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
            else:
                shutil.copy2(srcpath, dest)
                self.logging.info('Copied \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
             
    def periodic_save(self):
        self.sched.add_job(self.synchronise,'interval', seconds=int(self.synchronisation_content))
        self.sched.start()