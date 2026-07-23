import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const workbookPath = "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
console.log((await workbook.inspect({kind:"sheet,region,definedName", tableMaxRows: 4, tableMaxCols: 8, maxChars: 12000})).ndjson);
