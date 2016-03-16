from selenium import webdriver
import os
import sys
import time
import logging
import datetime


class DailySeries:
    
    def from_cmd(self, logging_enabled=True):

        if logging_enabled:
            logging.basicConfig(filename='occ_idsa_log_{0}.log'.format(datetime.date.today()),
                                level=logging.DEBUG, format='%(asctime)s %(message)s')

        arguments = self.parse_args()
        destination = arguments[0]
        fname = arguments[1]

        self.download_new_data(destination, fname)
    
    def download_new_data(self, dest_dir, new_fname):

        download_page_url = "http://www.optionsclearing.com/webapps/series-added-today?pageNum=1&pageSize=1000"

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", dest_dir)
        fp.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

        driver = webdriver.Firefox(fp)
        driver.get(download_page_url)

        button = driver.find_element_by_xpath('//*[@title="Download as CSV"]')
        button.click()
        time.sleep(2)
        driver.close()
        
        if new_fname:
            for filename in os.listdir(dest_dir):
                if filename == "intra_day_series_adds.csv":
                    os.rename(filename, new_fname)
                    logging.info('... destination file renamed: {0}'.format(new_fname))

    def parse_args(self):

        dir_path = os.getcwd()
        dest_fname = 'seriesadded.csv'
        
        if len(sys.argv) > 1:
            for item in sys.argv:
                if 'dest_dir=' in item:
                    t = item.split('dest_dir=')
                    dir_path = t[1]
                    logging.info('... destination folder specified: {0}'.format(dir_path))
                    
                if 'filename=' in item:
                    t = item.split('filename=')
                    dest_fname = t[1]
                    logging.info('... destination filename specified: {0}'.format(dest_fname))

        argd = [dir_path, dest_fname]
        logging.info('... saving to path: {0}'.format(dir_path))
        logging.info('... arguments passed: {0}'.format(argd))

        return argd
    
    
if __name__ == "__main__":
    occ = DailySeries()
    occ.from_cmd()
