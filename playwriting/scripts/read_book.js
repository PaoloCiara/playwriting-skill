// Save the text of a PDF, with page marks, so chapters can be read. macOS only.
//   osascript -l JavaScript read_book.js BOOK.pdf OUT.txt [first page] [last page]
ObjC.import('Quartz');
function run(a) {
  const d = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(a[0]));
  if (!d || !d.pageCount) return 'could not open ' + a[0];
  const first = a[2] ? +a[2] : 1, last = a[3] ? +a[3] : d.pageCount, out = [];
  for (let i = first; i <= Math.min(last, d.pageCount); i++)
    out.push('=== PAGE ' + i + ' ===\n' + (ObjC.unwrap(d.pageAtIndex(i - 1).string) || ''));
  $(out.join('\n')).writeToFileAtomicallyEncodingError(a[1], true, 4, null);
  return 'pages ' + first + '-' + Math.min(last, d.pageCount) + ' saved';
}
