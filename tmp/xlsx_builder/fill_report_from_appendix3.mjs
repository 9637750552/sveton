import fs from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const previewPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/report_after.png";
const pythonPath =
  "C:/Users/alvad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
const printSettingsPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/fix_contract_workbook_print_settings.py";

const CHECK = "☐";

const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const sheet = workbook.worksheets.getItem("Отчет");

const titleStyle = {
  fill: "#1F4E78",
  font: { bold: true, color: "#FFFFFF", size: 13 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const subtitleStyle = {
  font: { italic: true, color: "#666666", size: 8 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const sectionStyle = {
  fill: "#D9EAF7",
  font: { bold: true, size: 8 },
  verticalAlignment: "center",
  borders: {
    top: { style: "medium", color: "#808080" },
    bottom: { style: "thin", color: "#B7B7B7" },
    left: { style: "thin", color: "#B7B7B7" },
    right: { style: "thin", color: "#B7B7B7" },
  },
};
const headerStyle = {
  fill: "#2F75B5",
  font: { bold: true, color: "#FFFFFF", size: 7 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#B7B7B7" },
};
const labelStyle = {
  fill: "#FFFFFF",
  font: { size: 7 },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#B7B7B7" },
};
const inputStyle = {
  fill: "#FFFFFF",
  font: { size: 7 },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
};
const noteStyle = {
  fill: "#FFFFFF",
  font: { size: 7 },
  verticalAlignment: "top",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
};
const checkStyle = {
  fill: "#FFFFFF",
  font: { size: 7 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
};

function fmt(range, style) {
  range.format = style;
  range.format.font.name = "Calibri";
}

function mergeValue(range, value, style) {
  const target = sheet.getRange(range);
  target.merge();
  target.values = [[value]];
  fmt(target, style);
}

function writeCheck(row, text, note = "") {
  sheet.getRange(`A${row}`).values = [[CHECK]];
  fmt(sheet.getRange(`A${row}`), checkStyle);
  mergeValue(`B${row}:F${row}`, text, labelStyle);
  mergeValue(`G${row}:J${row}`, note, inputStyle);
}

function writeIssue(row, text) {
  sheet.getRange(`A${row}`).values = [[CHECK]];
  fmt(sheet.getRange(`A${row}`), checkStyle);
  mergeValue(`B${row}:E${row}`, text, labelStyle);
  mergeValue(`F${row}:J${row}`, "", inputStyle);
}

function restorePrintSettings() {
  const result = spawnSync(pythonPath, [printSettingsPath], { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(result.stderr || "Failed to restore print settings");
  }
  if (result.stdout.trim()) console.log(result.stdout.trim());
}

sheet.getRange("A1:J50").unmerge();
sheet.getRange("A1:J50").clear({ applyTo: "contents" });
fmt(sheet.getRange("A1:J44"), noteStyle);

mergeValue("A1:J1", "Отчет об осмотре", titleStyle);
mergeValue("A2:J2", 'Приложение N 3 к договору N ____ от "___" ____________ 20__ г.', subtitleStyle);

mergeValue("A4:J4", "1. Данные отчета", sectionStyle);
const reportRows = [
  ["Дата осмотра", "", "Исполнитель", ""],
  ["Объект / адрес объекта", "", "Дата отправки отчета Заказчику", ""],
];
sheet.getRange("A5:J6").values = reportRows.map(([a, b, c, d]) => [a, b, b, b, b, c, d, d, d, d]);
fmt(sheet.getRange("A5:A6"), labelStyle);
fmt(sheet.getRange("B5:E6"), inputStyle);
fmt(sheet.getRange("F5:F6"), labelStyle);
fmt(sheet.getRange("G5:J6"), inputStyle);
for (const ref of ["B5:E5", "G5:J5", "B6:E6", "G6:J6"]) sheet.getRange(ref).merge();

writeCheck(7, "Заявка на подбор оборудования заполнена и подписана Клиентом", "☐ да / ☐ нет / ☐ клиент отказался / ☐ подпись невозможно получить");
writeCheck(8, "Чек-лист осмотра места монтажа ИБП приложен", "☐ да / ☐ нет / ☐ не требуется");
writeCheck(9, "Фотоотчет приложен", "☐ да / ☐ нет / ☐ не требуется");

mergeValue("A11:J11", "2. Раскладка автоматов по щитам", sectionStyle);
mergeValue(
  "A12:J12",
  "Перечислить только автоматы резервной группы. Нумерация: слева направо и сверху вниз; первый автомат - верхний левый, последний - нижний правый.",
  noteStyle,
);

const headers = [
  "Щит / место",
  "N",
  "Что фактически питает",
  "УЗО/диф",
  "Фаза",
  "Комментарий",
];
sheet.getRange("A13:J13").values = [[headers[0], headers[1], headers[2], null, null, headers[3], headers[4], headers[5], null, null]];
fmt(sheet.getRange("A13:J13"), headerStyle);
sheet.getRange("C13:E13").merge();
sheet.getRange("H13:J13").merge();

for (let row = 14; row <= 23; row += 1) {
  sheet.getRange(`A${row}:J${row}`).values = [["", "", "", "", "", "", "", "", "", ""]];
  fmt(sheet.getRange(`A${row}:J${row}`), inputStyle);
  sheet.getRange(`C${row}:E${row}`).merge();
  sheet.getRange(`H${row}:J${row}`).merge();
}

mergeValue("A24:J24", "Если автоматов больше, чем строк в таблице, зарисовать схему щита вручную и приложить фото схемы.", noteStyle);
mergeValue("A25:J25", "Ручная схема щита / щитов:", sectionStyle);
for (let row = 26; row <= 29; row += 1) {
  mergeValue(`A${row}:J${row}`, "", inputStyle);
}

mergeValue("A30:J30", "Особенности щита, соединений, УЗО/дифов, PE/N, дополнительных щитов:", sectionStyle);
mergeValue("A31:J31", "", inputStyle);

mergeValue("A33:J33", "3. Непроверенные или спорные вопросы", sectionStyle);
sheet.getRange("A34").values = [[""]];
fmt(sheet.getRange("A34"), headerStyle);
mergeValue("B34:E34", "Вопрос / ограничение", headerStyle);
mergeValue("F34:J34", "Описание", headerStyle);
const issueRows = [
  "Что не удалось проверить на объекте",
  "Выявлены ограничения по месту установки ИБП",
  "Выявлены ограничения по прокладке кабельной трассы",
  "Есть опасные или непонятные места в щитах",
  "Есть сложности с выделением резервных автоматов в отдельную группу",
  "Есть расхождения с данными из Заявки",
  "Дальнейшие работы невозможны без уточнений",
  "Требуется решение Заказчика для продолжения",
];
issueRows.forEach((text, index) => writeIssue(35 + index, text));

mergeValue("A43:J43", "Исполнитель подтверждает, что отчет заполнен по результатам осмотра Объекта и содержит сведения, материалы, ограничения и выводы в пределах фактически выполненных действий.", noteStyle);
mergeValue("A44:E44", 'Исполнитель: __________________ / ____________________  "___" ____________ 20__ г.', noteStyle);
mergeValue("F44:J44", 'Ответственное лицо Заказчика: ______________ / ______________  "___" ____________ 20__ г.', noteStyle);

sheet.getRange("A:A").format.columnWidth = 14;
sheet.getRange("B:B").format.columnWidth = 5;
sheet.getRange("C:E").format.columnWidth = 12;
sheet.getRange("F:F").format.columnWidth = 10;
sheet.getRange("G:G").format.columnWidth = 8;
sheet.getRange("H:J").format.columnWidth = 12;
sheet.getRange("1:1").format.rowHeight = 20;
sheet.getRange("2:43").format.rowHeight = 17;
sheet.getRange("12:12").format.rowHeight = 28;
sheet.getRange("24:24").format.rowHeight = 22;
sheet.getRange("26:29").format.rowHeight = 18;
sheet.getRange("34:34").format.rowHeight = 18;
sheet.getRange("35:42").format.rowHeight = 26;
sheet.getRange("43:44").format.rowHeight = 24;
sheet.freezePanes.freezeRows(13);

const inspect = await workbook.inspect({
  kind: "table",
  sheetId: "Отчет",
  range: "A1:J44",
  tableMaxRows: 45,
  tableMaxCols: 10,
  maxChars: 12000,
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
  sheetName: "Отчет",
  range: "A1:J44",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(workbookPath);
restorePrintSettings();

console.log(`saved:${workbookPath}`);
console.log(`preview:${previewPath}`);
