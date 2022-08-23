## Task: 

There is a need to extract filenames from ~20K screenshots. An attempt to use tesseract-ocr keeping in mind the solution will not be prfect but can reduce the need to look at all the screenshot images manually and get the filenames from them.

+ Summary:
    + Crop top left portion of images, use opencv image processing methods to improve the text within the cropped image and then feed the same to tesseract-OCR (https://github.com/tesseract-ocr/tesseract) to recognize the characters in there.
    + Use Regular expressions to extract filename from tesseract-ocr output and further clean up some of the characters.
    + add relevant flags to ensure those to be manually checked are flagged

+ Environment:
    ```
    -----
    cv2                 4.5.4
    matplotlib          3.5.2
    pandas              1.4.3
    pytesseract         0.3.9
    session_info        1.0.0
    -----
    Python 3.9.12 (main, Jun  1 2022, 11:38:51) [GCC 7.5.0]
    Linux-5.15.0-46-generic-x86_64-with-glibc2.31
    -----
    ```

+ How to run the script

    ```
    time python screenshots_ocr.py --path_to_tesseract '/usr/bin/tesseract' --path_to_img_folder /to82sp/'2018 LA Waterbird Colony Photo Analysis' --path_to_output to82_screenshots_filenames.csv
    ```

+ What's in the output file?
    + input_fname - input filename along with path
    + tesseract_output - text that tesseract-ocr recognized
    + regex_cleaned - text after applying regular expression that looks for dateMonthYearCamera#-photonumber.jpg/tif.
    + tesseract_null - flag to indicate if tesseract-ocr did not recognize any characters in the cropped image.
    + regex_failed - flag to indicate files those that failed the regular expression from above
    + post_regex_processed - 2nd set of regular expressions are applied to correct camera number and file extensions. flag to indicate such regular expressions have been applied. 
    + post_regex_out - text after applying 2nd second of regular expressions
    + ends_with_jpg_tif - flag to indicate if the filename ends ini .jpg or .tif.
    + tobe_checked - flag to indicate if the file needs to be manually checked for filename

+ How long does the script take:
    + On a set of 3830 images, it took ~45mins
    + Solution here is not perfect. Out of above 3830, tesseract and regular expressions helped get filenames right for ~80% of the files. Rest 20% would need to be manually looked.Assuming 2mins for each file, 2*760 = ~1400mins = ~24 hours to go through those flagged    