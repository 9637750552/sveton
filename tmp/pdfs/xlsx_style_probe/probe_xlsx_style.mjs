import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const outputDir = "C:/Users/alvad/Documents/Sveton/tmp/pdfs/xlsx_style_probe";

await fs.mkdir(outputDir, { recursive: true });

const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const summary = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 8000,
  tableMaxRows: 8,
  tableMaxCols: 8,
  tableMaxCellChars: 80,
});
await fs.writeFile(path.join(outputDir, "summary.ndjson"), summary.ndjson, "utf8");
console.log(summary.ndjson);

const sheets = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 4000 });
await fs.writeFile(path.join(outputDir, "sheets.ndjson"), sheets.ndjson, "utf8");

const sheetNames = [];
for (const line of sheets.ndjson.split(/\r?\n/)) {
  if (!line.trim()) continue;
  try {
    const record = JSON.parse(line);
    if (record.name) sheetNames.push(record.name);
  } catch {}
}

for (const sheetName of sheetNames) {
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 1.5,
    format: "png",
  });
  const bytes = new Uint8Array(await preview.arrayBuffer());
  const safe = sheetName.replace(/[\\/:*?"<>|]/g, "_");
  await fs.writeFile(path.join(outputDir, `${safe}.png`), bytes);
  console.log(`rendered ${sheetName}`);
}
