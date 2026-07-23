import { spawnSync } from "node:child_process";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const repairedPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/appendix_2_object_inspection_request_repaired_tmp.xlsx";
const pythonPath =
  "C:/Users/alvad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
const printSettingsPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/fix_contract_workbook_print_settings.py";

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(repairedPath);

const result = spawnSync(pythonPath, [printSettingsPath], {
  encoding: "utf8",
  env: {
    ...process.env,
    CONTRACT_WORKBOOK_PATH: repairedPath,
  },
});
if (result.status !== 0) {
  throw new Error(result.stderr || "Failed to restore print settings");
}
if (result.stdout.trim()) console.log(result.stdout.trim());
console.log(`repaired:${repairedPath}`);
