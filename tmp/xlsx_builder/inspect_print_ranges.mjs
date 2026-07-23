import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const workbookPath = "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
for (const [sheetId, range] of [["Заявка","A1:E39"],["Подбор оборудования","B1:AO54"]]) {
  console.log((await workbook.inspect({kind:"table", sheetId, range, tableMaxRows:6, tableMaxCols:10, maxChars:6000})).ndjson);
}
