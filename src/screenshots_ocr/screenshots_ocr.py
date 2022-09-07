
import cv2, os
from pytesseract import pytesseract
import matplotlib.pyplot as plt
import glob
import re
import pandas as pd
import numpy as np
import session_info
import argparse
import csv

def set_tesseract_cmd(path_to_tesseract = '/usr/bin/tesseract'):    
    pytesseract.tesseract_cmd = path_to_tesseract


def get_fname_from_images(path_to_img_folder, write_to_file=False, path_outfile=None):
    images = glob.glob(os.path.join(path_to_img_folder,'**', "*.JPG"), recursive=True)
    print("----- \n")
    print(f"Detected {len(images)} JPG files recursively within '{path_to_img_folder}'")
    orig_fname = []
    tesseract_out = []
    regex_cleaned = []
    tesseract_none = []
    regex_failed = []
    post_regex = []
    post_regex_out = []
    for f in images:
        img  = cv2.imread(f, cv2.IMREAD_UNCHANGED)
        img_cropped = img[0:35, 0:380]
        rgb = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
        b = rgb.copy()
        b[:,:,0] = 0
        b[:,:,2] = 0
        gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray,1)#cv2.GaussianBlur(gray, (1,1), 30)#cv2.medianBlur(gray,1)#
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU )[1]
        config = ('-l eng --oem 3 --psm 3')
        text = pytesseract.image_to_string(thresh,config=config)
        if text == '':
            config = ('-l eng --oem 3 --psm 6')
            text = pytesseract.image_to_string(thresh,config=config)
            if text == '':
                tesseract_none.append(1)
            else:
                tesseract_none.append(0)    
        else:
            tesseract_none.append(0)    
        orig_fname.append(f)
        tesseract_out.append(text)
        #print(text)
        text = re.sub('\s*?','', text)        
        #text = text.replace('\n','').replace('(1/1)','').replace('25%','')       
        #regex='\d{2}[a-zA-Z]+\d{4}\w+[-]\d*.[jt][pi][fg]'
        #pattern = r'\d{2}\w+[-]\w+\.[jt][pi][fg]'
        #pattern = r'\d{2}[A-Za-z]+\w+[-]\w+\.*?[jt][pi][fgt]'
        #pattern = r'\d{2}[A-Za-z]+[\w?~]+[-]*\w+[\.,:]*?[jiot][pif]*[fgt]*'
        pattern = r'\d{1,2}[A-Za-z]+[2][0][12][0-9]Cam[\w?~]+[-]*\w+[\.,:]*?[jiotJT][pifPT]*[fgtGF]*'
        if re.search(pattern, text):
            text = re.search(pattern, text).group()
            regex_failed.append(0)
        else:
            regex_failed.append(1)    
        regex_cleaned.append(text)
        # post regex
        # 
        
        num_changes = 0
        if 'Camera?' or 'Cameraz' in text:
            text = re.sub('Camera\?|Cameraz', 'Camera2', text)
            num_changes += 1
        if 'Cameral' or 'Camerat' or 'Camerai' or 'Camnerat' or 'Camera!' in text:
            to_match = ['Cameral','Camerat','Camerai','Camnerat', 'Camera!']
            text = re.sub('|'.join(to_match), 'Camera1', text)            
            num_changes += 1
        if 'Comere' in text:
            text = re.sub('Comere', 'Camera', text)
            num_changes += 1
        if 'Cardi' or 'Cardt' or 'Cardl' in text:
            text = re.sub('Cardi|Cardt|Cardl', 'Card1', text)
        if 'Card?' or 'Cardz' in text:
            text = re.sub('Card\?|Cardz', 'Card2', text)
        if re.search('3une|}une', text[0:11]):
            text = re.sub('3une|}une','June',text[0:11]) + text[11:len(text)]
        if re.search('thay|Mhay|hay|tay', text[0:11]):
            text = re.sub('thay|Mhay|hay|tay','May',text[0:11]) + text[11:len(text)]    

        if not re.search('\.', text[len(text)-10:len(text)]):
            #if ',jpg' or ',jp' or ',pg' or ',og' in text:
            if re.search('[jop][pog]*[g]*',text[len(text)-10:len(text)]): 
                to_m1 = [',jpg' ,',jp',',pg',',p', ',og','jpg','jp','jog','j', 'og', ',jog', ',ipg']        
                text = text[0:len(text)-10] + re.sub('|'.join(to_m1), '.jpg', text[len(text)-10:len(text)])
                num_changes += 1
            elif re.search('[ti][if]*[f]*', text[len(text)-10:len(text)]):
                to_m2 = ['tif','ti','if', ',tif', ',if', ',f', ':if', ',tf', 'tf', ',ti']        
                text = text[0:len(text)-10] + re.sub('|'.join(to_m2), '.tif', text[len(text)-10:len(text)])
                num_changes += 1
        else:
            #if  '.ipg' or '.jp' or '.j' or '.ip' in text:
            if re.search('ipg|jp|j|ip|pg|jg', text[len(text)-10:len(text)]):
            #if re.search('[ij][p]*[g]*', text):
                to_match_jpg = ['.ipg','.jp','.j','.ip', '.pg', '.jg', '.og']
                if not re.search('\.jpg',text):
                    text = text[0:len(text)-10] + re.sub('|'.join(to_match_jpg),'.jpg',text[len(text)-10:len(text)])
                    #text = re.sub('|'.join(to_match_jpg), '.jpg', text)
                    num_changes += 1
            elif re.search('tf|ti|t|if|i*', text[len(text)-10:len(text)]):
                #re.search('[ti][if]*[f]*', text):
                to_match_tif = ['.tf','.if','.ti','.i',':if','.t', '.8f']
                if not re.search('\.tif', text[len(text)-10:len(text)]):
                    text = text[0:len(text)-10] + re.sub('|'.join(to_match_tif),'.tif',text[len(text)-10:len(text)])
                    num_changes += 1                                  

        text = text.replace('\n','').replace('(1/1)','').replace('25%','')
        if num_changes > 0:
            post_regex.append(1)
        else:
            post_regex.append(0)
        post_regex_out.append(text)                        

    outdf = pd.DataFrame({'input_fname':orig_fname,
                          'tesseract_output':tesseract_out,
                          'regex_cleaned':regex_cleaned,
                          'tesseract_null': tesseract_none,
                          'regex_failed': regex_failed,
                          'post_regex_processed':post_regex,
                          'post_regex_out':post_regex_out})

    outdf['ends_with_jpg_tif'] = outdf['post_regex_out'].apply(lambda x: 1 if x.endswith(('.jpg', '.JPG', '.tif', '.TIF')) else 0)
    outdf['tobe_checked'] = list(map(lambda x,y: 1 if re.sub('\s*?','', x) == y else 0, tesseract_out, regex_cleaned ))
    outdf['final_tobe_checked'] = np.where(np.logical_and(outdf.ends_with_jpg_tif == 0, outdf.tobe_checked==0), 1, outdf.tobe_checked)
    
    if write_to_file:
        # replace \n with \\n
        outdf.loc[:, "tesseract_output"] = outdf["tesseract_output"].apply(lambda x : x.replace('\n', '\\n'))
        if path_outfile is not None:                      
            outdf.to_csv(path_outfile, sep=',', index=False, quoting = csv.QUOTE_ALL)        
    else:
        return outdf

if __name__ == "__main__":
    """Usage:
    time python src/screenshots_ocr/screenshots_ocr.py --path_to_tesseract '/usr/bin/tesseract' \
        --path_to_img_folder /to82sp/'Task 2 2021 Waterbird Colony Photo Analysis' \
        --path_to_output /z/Projects/AvianAI/to82_2021_screenshots_filenames.csv
    """
    args_parser = argparse.ArgumentParser(description='Fetch filename from screenshots using Tesseract OCR')
    args_parser.add_argument('--path_to_tesseract', help = 'Path to where Tsseract executable is installed', required=True)
    args_parser.add_argument('--path_to_img_folder', help = 'Path to parent directory where all images are located- JPG files are recursively read from all subdirectories.', required=True)
    args_parser.add_argument('--path_to_output', help = 'Path to output file', required=True)
    args = args_parser.parse_args()

    tess_path = args.path_to_tesseract
    img_folder = args.path_to_img_folder
    out_file = args.path_to_output

    print("Session Information:\n")
    session_info.show()

    set_tesseract_cmd(path_to_tesseract = tess_path)
    get_fname_from_images(img_folder, write_to_file=True, path_outfile=out_file)









