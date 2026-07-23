import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const path = "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(path));
console.log((await workbook.inspect({kind:"sheet,definedName", maxChars:12000})).ndjson);
const errors = await workbook.inspect({kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options:{useRegex:true,maxResults:100}});
console.log(errors.ndjson);
