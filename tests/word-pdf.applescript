-- Opens a docx in Microsoft Word and saves it as PDF, for page images of
-- what Word shows. Not part of tests/verify.py. Run with absolute paths:
--
--     osascript tests/word-pdf.applescript /abs/in.docx /abs/out.pdf
--
-- For LibreOffice's view, run
-- `soffice --headless --convert-to pdf in.docx --outdir <folder>`.
on run argv
	set inPath to item 1 of argv
	set outPath to item 2 of argv
	tell application "Microsoft Word"
		open (POSIX file inPath)
		set d to active document
		save as d file name outPath file format format PDF
		close d saving no
	end tell
end run
