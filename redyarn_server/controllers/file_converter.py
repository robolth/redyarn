from PyPDF2 import PdfFileReader

import os
import argparse
import json
import mutagen
import csv
import zipfile
import epub_meta

from argparse import ArgumentParser
from datetime import datetime as dt
from xml.etree import ElementTree as etree


def get_pdf_info(file):

    pdf = PdfFileReader(file)

    info = pdf.getDocumentInfo()

    output = {}

    if info.author is not None: output["author"] = info.author
    if info.creator is not None: output["creator"] = info.creator
    if info.producer is not None: output["producer"] = info.producer
    if info.subject is not None: output["subject"] = info.subject
    if info.title is not None: output["title"] = info.title

    num_pages = pdf.getNumPages()
    if num_pages is not None: output["num_pages"] = num_pages

    return output



def get_pdf_text(file):
    
    text = ''

    pdf = PdfFileReader(file)

    num_pages = pdf.getNumPages()

    for page_number in range(num_pages):
        page = pdf.getPage(page_number)
        page_text = page.extractText()
        if page_text is not None and page_text is not '' and page_text is not '/n':
            if page_number > 0 : text = text + '\f' 
            text = text + page_text

    if text is '': text = None

    return(text)


def get_office_info(file):

    if not zipfile.is_zipfile(file):
        return None

    zfile = zipfile.ZipFile(file)
    core_xml = etree.fromstring(zfile.read('docProps/core.xml'))
    app_xml = etree.fromstring(zfile.read('docProps/app.xml'))

    output = {}

    core_mapping = {
       'title': 'Title',
       'subject': 'Subject',
       'creator': 'Author(s)',
       'keywords': 'Keywords',
       'description': 'Description',
       'lastModifiedBy': 'Last Modified By',
       'modified': 'Modified Date',
       'created': 'Created Date',
       'category': 'Category',
       'contentStatus': 'Status',
       'revision': 'Revision'
    }

    for element in core_xml.getchildren():
        for key, title in core_mapping.items():
            if key in element.tag:
                if 'date' in title.lower():
                   text = str(dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ"))
                else:
                   text = element.text
                output[title] = text

    app_mapping = {
        'TotalTime': 'Edit Time (minutes)',
        'Pages': 'Page Count',
        'Words': 'Word Count',
        'Characters': 'Character Count',
        'Lines': 'Line Count',
        'Paragraphs': 'Paragraph Count',
        'Company': 'Company',
        'HyperlinkBase': 'Hyperlink Base',
        'Slides': 'Slide count',
        'Notes': 'Note Count',
        'HiddenSlides': 'Hidden Slide Count',
    }
    for element in app_xml.getchildren():
        for key, title in app_mapping.items():
            if key in element.tag:
                if 'date' in title.lower():
                    text = str(dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ"))
                else:
                    text = element.text
                output[title] = text

    return output




def get_id3_info(file):

    id3_file = mutagen.File(file)

    id3_frames = {'TIT2': 'Title',
                 'TPE1': 'Artist',
                 'TALB': 'Album',
                 'TXXX': 'Custom',
                 'TCON': 'Content Type',
                 'TDRL': 'Date released',
                 'COMM': 'Comments',
                 'TDRC': 'Recording Date'}
    output = {}

    for frames in id3_file.tags.values():
        frame_name = id3_frames.get(frames.FrameID, frames.FrameID)
        desc = getattr(frames, 'desc', "N/A")
        text = getattr(frames, 'text', ["N/A"])[0]
        value = getattr(frames, 'value', "N/A")
        if "date" in frame_name.lower():
            text = str(text)
        output[frame_name]=text
    return output



def get_mp4_info(file):

    mp4_file = mutagen.File(file)

    output = {}

    if mp4_file is not None:

        cp_sym = u"\u00A9"
        qt_tag = {
            cp_sym + 'nam': 'Title', cp_sym + 'art': 'Artist',
            cp_sym + 'alb': 'Album', cp_sym + 'gen': 'Genre',
            'cpil': 'Compilation', cp_sym + 'day': 'Creation Date',
            'cnID': 'Apple Store Content ID', 'atID': 'Album Title ID',
            'plID': 'Playlist ID', 'geID': 'Genre ID', 'pcst': 'Podcast',
            'purl': 'Podcast URL', 'egid': 'Episode Global ID',
            'cmID': 'Camera ID', 'sfID': 'Apple Store Country',
            'desc': 'Description', 'ldes': 'Long Description'}
    #       genre_ids = json.load(open('apple_genres.json'))



        if mp4_file.tags is not None:

            for name, value in mp4_file.tags.items():

                tag_name = qt_tag.get(name, name)

                if isinstance(value, list):
                    value = "; ".join([str(x) for x in value])
                
                output[tag_name] = value

    return output



def get_csv_info(file):

    output = {}

    line = next(file)
    dialect = csv.Sniffer().sniff(line)

    file.seek(0)
    reader = csv.reader(file, dialect)

    output['num_columns'] = line.count(dialect.delimiter) + 1
    output['num_rows'] = len(list(reader))
    output['delimiter'] = dialect.delimiter
    output['lineterminator'] = dialect.lineterminator

    if output == {}: output = None

    return output


def get_epub_info(file):

    temp_path = "temp_epub"

    file.save(temp_path)
#    temp_path = os.path.join("./",)

    output = epub_meta.get_epub_metadata(temp_path,read_cover_image=False, read_toc=True)
    output = dict(output)

    #Cleanup server
    os.remove(temp_path)

    return output




