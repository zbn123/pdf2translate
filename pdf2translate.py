# -*- coding: utf-8 -*-
"""
Created on Sun Oct 01 14:56:01 2017

@author: acseckin
"""

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from googletrans import Translator

def convert(fname):
    rawfilename="_EN.txt"
    trfilename="_TR.txt"
    translator = Translator(service_urls=['translate.google.com','translate.google.com.tr'])
    pages=None
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    print pagenums
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    newstr=""

    startix=text.find("Abstract")
    stopix=text.find("References")
    print len(text),startix,stopix
    nt=text[startix+8:stopix]
    numberofstr=0
    
    par=0
    parcumle=""
    for c in nt:
        #print numberofstr, ord(c),c        
        if ord(c)==10:
            newstr=newstr+" "
        
        elif (ord(c)==40) or par==1:
            par=1
            if (ord(c)>=32) or (ord(c)<=122) :
                parcumle=parcumle+c
            if (ord(c)==41):
                par=0
        elif (ord(c)==91) or (par==2):
            par=2
            newstr=newstr+c
            if (ord(c)==93) :
                par=0
        elif (ord(c)==46) or (par==3) :
            par=3
            if (ord(c)==32):  
                par=0
                numberofstr+=1
                newstr=newstr+"."
                
                print "EN:",newstr
                translation=translator.translate(newstr, src='en',dest='tr')
                tr=translation.text.encode('utf-8')
                print "TR:", tr
                print "#######################################################"
                
                with open(fname.replace(".pdf","")+rawfilename, "a") as enfile:
                    enfile.write(str(numberofstr)+":"+newstr+"\n")
                    
                with open(fname.replace(".pdf","")+trfilename, "a") as trfile:
                    trfile.write(tr)
                if len(parcumle)>1:
                    ptranslation=translator.translate(parcumle, src='en',dest='tr')
                    ptr=ptranslation.text.encode('utf-8')
                    
                    with open(fname.replace(".pdf","")+trfilename, "a") as trfile:
                        trfile.write(parcumle+"-"+ptr+"\n")
                    parcumle=""
                else:
                    with open(fname.replace(".pdf","")+trfilename, "a") as trfile:
                        trfile.write("\n")
                newstr=""
        elif (ord(c)>=32) or (ord(c)<=122) :
            newstr=newstr+c
#convert example pdf file "doc1.pdf" to text and translate English to Turkish via google translate
convert("doc1.pdf")
