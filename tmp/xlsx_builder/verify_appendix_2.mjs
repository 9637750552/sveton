import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const repoRoot = path.resolve("..", "..");
const filePath =
  process.env.APPENDIX_2_VERIFY_PATH ||
  path.join(repoRoot, "01_docs", "operations", "contracts", "appendix_2_object_inspection_request.xlsx");
const previewPath = path.join(repoRoot, "tmp", "xlsx_builder", "appendix_2_print_verify.png");

const input = await FileBlob.load(filePath);
const workbook = await SpreadsheetFile.importXlsx(input);

const inspect = await workbook.inspect({
  kind: "table",
  sheetId: "Приложение N 2",
  range: "A1:E39",
  tableMaxRows: 40,
  tableMaxCols: 5,
  maxChars: 4000,
});
console.log(inspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Приложение N 2",
  range: "A1:E39",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
console.log(`preview:${previewPath}`);
