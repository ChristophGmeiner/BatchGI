# Process for Gathering structured data out of a PDF

This git repo describes a process for a pharmaceutical company on how to derive structured informations from release forms to structured form. In this case structured form means a csv file and a document in a MongoDB.

This is done using Python. The applied modules are explained in the notebook.

## Business Problem
A pharmaceutical company needs to match their batch numbers to some other information. Unfortunately all these information is only stored in printed out documents.
But fortunately they all have the same structure and the same wording.
See an example below.

<img src=img1.png>

We need to extract the ChB, MatNr, FS; GI and FOL number and save them (think about that this operation has to be carried out on several 1000s of documents) in a structured way as mentioned above.

So all the paper documents are scanned into a single big document with several 1000s pages.

## Files

### Batch_GI_PDF.ipynb
This notebook describes thw whole process.

### Batch_GI_PDF.py
This is a production-ready Python script.

You can use the script for many documents (with single or multiple pages) at once.

Please be aware, that this only works for image-like pdfs. Pure text pdf documents will be much faster and easier, but these are not covered in this repo.