import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const workbookPath = "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
try {
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
  console.log((await workbook.inspect({kind:"sheet,definedName", maxChars:10000})).ndjson);
  const errors = await workbook.inspect({kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options:{useRegex:true,maxResults:100}});
  console.log(errors.ndjson);
  const out = await SpreadsheetFile.exportXlsx(workbook);
  await out.save("C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/roundtrip_diagnostic.xlsx");
  console.log('artifact_import_export_ok=true');
} catch (error) {
  console.error(error);
  process.exit(1);
}
