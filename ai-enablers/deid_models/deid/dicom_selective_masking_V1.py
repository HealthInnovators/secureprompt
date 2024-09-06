import pytesseract as pt
import numpy as np
from bs4 import BeautifulSoup
import re
from typing import List
from PIL import Image
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class DicomSelectiveMasking:

    @staticmethod
    def image_preprocess(pixel_array, frames):
        '''

        :param pixel_array: Numpy array for pre-processing
        :param frames: Number of frames in the array
        :return: Processed Numpy array
        '''
        if frames > 1:
            image = pixel_array[0]
        else:
            image = pixel_array

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]
        #image = cv2.subtract(255, image)
        return image

    @staticmethod
    def _match_word(ocr_words, token_list):
        """Method that extracts the Bounding box information from Tessaract output (ocr_words)
            based upon the configured tags (self.tags)

        Args:
            ocr_words: Word Tags extracted from Tesseract OCR

        Returns:
            A list of items with each item being a tuple giving Bounding Box information of the format (startX, StartY, endX, endY)
            Example:[(143, 45, 180, 67), (43, 145, 80, 167)]
        """
        result = []
        for token in token_list:
            search_string_arr = token.split()
            for search_string in search_string_arr:
                temp = [s for s in ocr_words if search_string.lower().strip().strip("'").strip(",") == s.text.lower().strip().strip("'").strip(",")
                        and s.attrs['class'][0] == 'ocrx_word']
                if len(temp) != 0:
                    result = result + temp
        return list(set(result))

    @staticmethod
    def _mask_image(coordinates, pixel_array):
        """ Selectively Mask image based on bounding box information
        Mask color is set to black by default

        Args:
            coordinates: A list of coordinates to be masked in image
            pixel_array: The pixel array to be masked

        Returns:
            Masked Image as per coordinates
        """
        pixel_array_tmp = pixel_array.copy()
        ''' setting mask color to black '''
        mask_color = 0
        for coordinate in coordinates:
            minc, minr, maxc, maxr = coordinate
            if pixel_array_tmp.ndim == 3:
                pixel_array_tmp[minr:maxr, minc:maxc, 0] = mask_color
                pixel_array_tmp[minr:maxr, minc:maxc, 1] = mask_color
                pixel_array_tmp[minr:maxr, minc:maxc, 2] = mask_color
            if pixel_array_tmp.ndim == 4:
                pixel_array_tmp[:, minr:maxr, minc:maxc, 0] = mask_color
                pixel_array_tmp[:, minr:maxr, minc:maxc, 1] = mask_color
                pixel_array_tmp[:, minr:maxr, minc:maxc, 2] = mask_color
        return pixel_array_tmp

    def selective_mask(self, pixel_array, frames, token_list: List = []):
        """ Process Pixel Array, pass it via Tesseract for OCR extraction and selectively mask the image by matching
         OCR output (bounding box) against the tokens

        Args:
            pixel_array: The pixel array to be OCRed and masked
            token_list: List of string token names to be masked; By default, if no mask is given, all identified text items are masked
            frames: Number of frames in pixel array

        Returns:
            Bounding box array, Masked Image
        """
        ocr_output = pt.image_to_pdf_or_hocr(self.image_preprocess(pixel_array, frames), extension="hocr").decode('utf-8')
        soup = BeautifulSoup(ocr_output, "html.parser")
        ocr_words = soup.find_all('span')
        if not token_list:
            word_match_list = [s for s in ocr_words if len(s.text.strip()) != 0 and s.attrs['class'][0] == 'ocrx_word']
        else:
            word_match_list = self._match_word(ocr_words, token_list)

        bbox_all = []
        for match in word_match_list:
            bbox = re.search('bbox (.*);', match.attrs['title']).group(1).split(' ')
            # print(bbox)
            bbox = [int(i) for i in bbox]
            bbox_all.append(bbox)

        result = self._mask_image(bbox_all, pixel_array)
        return bbox_all, result


if __name__ == "__main__":
    pix_array = np.array(Image.open('./test_data/input.jpeg'))
    no_frames=1
    mask = ['Test Hospital', '41200920070905', 'V2008', 'ETT', 'Apex', 'SR', 'PHILIPS', 'Adult', 'TUC', 'FR', 'TIB']
    bounding_box, masked_image = DicomSelectiveMasking().selective_mask(pix_array, no_frames, token_list=mask)
    Image.fromarray(masked_image).save('output.jpg')


