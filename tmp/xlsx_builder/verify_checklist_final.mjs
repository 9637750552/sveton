import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const previewPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/checklist_final_verify.png";

const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const inspect = await workbook.inspect({
  kind: "table",
  sheetId: "Чек-лист",
  range: "A23:J35",
  tableMaxRows: 13,
  tableMaxCols: 10,
  maxChars: 8000,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Чек-лист",
  range: "A1:J39",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
console.log(`preview:${previewPath}`);
