import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const previewDir = "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder";

const sheets = [
  ["Заявка", "A1:E39", "request_print_verify.png"],
  ["Отчет", "A1:J44", "report_print_verify.png"],
  ["Чек-лист", "A1:J39", "checklist_print_verify.png"],
  ["Подбор оборудования", "B1:AO54", "equipment_request_print_verify.png"],
];

const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);

for (const [sheetId, range, fileName] of sheets) {
  const inspect = await workbook.inspect({
    kind: "table",
    sheetId,
    range,
    tableMaxRows: 6,
    tableMaxCols: 10,
    maxChars: 5000,
  });
  console.log(inspect.ndjson);

  const preview = await workbook.render({
    sheetName: sheetId,
    range,
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    `${previewDir}/${fileName}`,
    new Uint8Array(await preview.arrayBuffer()),
  );
  console.log(`preview:${previewDir}/${fileName}`);
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);
