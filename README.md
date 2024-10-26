# text-to-datamatrix

This repository provides some tools to convert text to datamatrix codes and back.

## Usage

### Text to datamatrix

Dump a plain text file into the `data` folder and run this bit of code:

```Python
from text_to_datamatrix import TextToDatamatrix

text_to_datamatrix = TextToDatamatrix()
text_to_datamatrix.convert('data/text.txt', 'datamatrix.png')
```

The result will be a .png file containing datamatrices with the text. This will also work other plain text files, like .sql and .py.

### Datamatrix to text

To convert datamatrices back to text, run this bit of code:

```Python
from text_to_datamatrix import DatamatrixToText

datamatrix_to_text = DatamatrixToText()
datamatrix_to_text.convert('data/datamatrix.png', 'text.txt')
```

The result will be a .txt file in the `export` folder containing the plain text. If the .png file contains more than one datamatrix, the result will be a .txt file containing all the concatenated text.

### Reading from a .pdf file

If the datamatrices are in a scanned .pdf file, you can use the `pdf_to_png` tool to convert the datamatrices to text:

```Python
from utils import pdf_to_png

pdf_to_png('../data/boarding-pass.pdf')

```

The result will be a .png file per page that can be converted to text using the `datamatrix_to_text` tool. As this will be most likely used in the case of _scanned_ files, the quality of the result using the `DatamatrixToText` class on the acquired .png file will rely on the quality of the scanned file.

## Quality

The quality of the `DatamatrixToText` class depends on the quality of the .png file. If the .png file is a converted .pdf file, the quality might be lower than expected. It is recommended to create individual data matrices of 30 x 30 mm for high quality results.

## License

Use this and be cool enough to share it with the world :)
