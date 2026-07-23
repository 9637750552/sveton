import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = path.resolve("..", "..");
const outPath =
  process.env.APPENDIX_2_OUT_PATH ||
  path.join(
    repoRoot,
    "01_docs",
    "operations",
    "contracts",
    "appendix_2_object_inspection_request.xlsx",
  );
const previewPath = path.join(
  repoRoot,
  "tmp",
  "xlsx_builder",
  "appendix_2_preview.png",
);

const wb = Workbook.create();
const sheet = wb.worksheets.add("Приложение N 2");
sheet.showGridLines = false;

sheet.getRange("A1:E1").merge();
sheet.getRange("A1").values = [["Приложение N 2"]];
sheet.getRange("A2:E2").merge();
sheet.getRange("A2").values = [["Заявка на осмотр объекта"]];
sheet.getRange("A3:E3").merge();
sheet.getRange("A3").values = [["к договору N ____ от \"___\" ____________ 20__ г."]];

sheet.getRange("A5:E5").merge();
sheet.getRange("A5").values = [["1. Данные по заявке"]];
sheet.getRange("A6:B12").values = [
  ["Поле", "Значение"],
  ["Заказчик / ответственное лицо Светон", ""],
  ["Клиент - Ф.И.О. или наименование организации", ""],
  ["Контакты клиента", ""],
  ["Адрес объекта", ""],
  ["Срок исполнения заявки", ""],
  ["Стоимость выезда / услуг Исполнителя", ""],
];

sheet.getRange("A14:E14").merge();
sheet.getRange("A14").values = [["2. Что передано исполнителю"]];
sheet.getRange("A15:C23").values = [
  ["Отметка", "Материал", "Комментарий"],
  ["☐", "Фото щита от клиента", ""],
  ["☐", "Фото места установки ИБП от клиента", ""],
  ["☐", "Фото предполагаемой трассы от клиента", ""],
  ["☐", "Схема / план помещений от клиента", ""],
  ["☐", "Электрическая схема энергоснабжения объекта от клиента", ""],
  ["☐", "Предварительный список нагрузок, устанавливаемых в резерв", ""],
  ["☐", "Особые условия объекта от клиента", ""],
  ["☐", "Иное", ""],
];

sheet.getRange("A25:E25").merge();
sheet.getRange("A25").values = [["3. Что нужно проверить/измерить"]];
sheet.getRange("A26:C32").values = [
  ["Отметка", "Проверка", "Комментарий"],
  ["☐", "3.1. Проверить состояние электросети.", ""],
  ["☐", "3.2. Проверить возможность установки ИБП, инвертора и АКБ.", ""],
  ["☐", "3.3. Проверить состояние щита клиента.", ""],
  ["☐", "3.4. Определить состав и мощности нагрузок, устанавливаемых в резерв.", ""],
  ["☐", "3.5. Определить автоматы резервной группы.", ""],
  ["☐", "3.6. Проверить возможность прокладки кабельной трассы.", ""],
];

sheet.getRange("A35:E39").values = [
  ["Исполнитель / монтажник", "", "", "Подпись", ""],
  ["", "", "", "", ""],
  ["Ответственное лицо Светон", "", "", "Подпись", ""],
  ["", "", "", "", ""],
  ["Дата", "", "", "", ""],
];

sheet.getRange("B6:E6").merge();
sheet.getRange("B7:E12").merge(true);
sheet.getRange("C15:E15").merge();
sheet.getRange("C16:E23").merge(true);
sheet.getRange("C26:E26").merge();
sheet.getRange("C27:E32").merge(true);

const titleStyle = {
  font: { bold: true, color: "#FFFFFF", size: 15 },
  fill: "#244062",
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const subtitleStyle = {
  font: { bold: true, color: "#244062", size: 13 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const sectionStyle = {
  font: { bold: true, color: "#FFFFFF" },
  fill: "#5B9BD5",
  verticalAlignment: "center",
};
const headerStyle = {
  font: { bold: true, color: "#FFFFFF" },
  fill: "#2F75B5",
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const inputStyle = {
  fill: "#FFFFFF",
  verticalAlignment: "top",
};
const border = { preset: "all", style: "thin", color: "#D9E2F3" };

sheet.getRange("A1:E1").format = titleStyle;
sheet.getRange("A2:E2").format = subtitleStyle;
sheet.getRange("A3:E3").format = {
  font: { italic: true, color: "#666666" },
  horizontalAlignment: "center",
};
sheet.getRange("A5:E5").format = sectionStyle;
sheet.getRange("A14:E14").format = sectionStyle;
sheet.getRange("A25:E25").format = sectionStyle;
sheet.getRange("A6:E6").format = headerStyle;
sheet.getRange("A15:E15").format = headerStyle;
sheet.getRange("A26:E26").format = headerStyle;

sheet.getRange("A6:E12").format.borders = border;
sheet.getRange("A15:E23").format.borders = border;
sheet.getRange("A26:E32").format.borders = border;
sheet.getRange("A35:E39").format.borders = border;

sheet.getRange("B7:E12").format = inputStyle;
sheet.getRange("C16:E23").format = inputStyle;
sheet.getRange("C27:E32").format = inputStyle;
sheet.getRange("B35:B39").format = inputStyle;
sheet.getRange("E35:E39").format = inputStyle;

sheet.getRange("A15:A23").format = {
  horizontalAlignment: "center",
  verticalAlignment: "center",
  font: { size: 14 },
};
sheet.getRange("A26:A32").format = {
  horizontalAlignment: "center",
  verticalAlignment: "center",
  font: { size: 14 },
};

sheet.getRange("A1:E39").format.wrapText = true;
sheet.getRange("A1:E39").format.font.name = "Arial";

sheet.getRange("A:A").format.columnWidth = 34;
sheet.getRange("B:B").format.columnWidth = 58;
sheet.getRange("C:C").format.columnWidth = 42;
sheet.getRange("D:D").format.columnWidth = 18;
sheet.getRange("E:E").format.columnWidth = 32;
sheet.getRange("1:1").format.rowHeight = 28;
sheet.getRange("2:2").format.rowHeight = 24;
sheet.getRange("3:3").format.rowHeight = 22;
sheet.getRange("5:5").format.rowHeight = 22;
sheet.getRange("14:14").format.rowHeight = 22;
sheet.getRange("25:25").format.rowHeight = 22;
sheet.getRange("7:12").format.rowHeight = 34;
sheet.getRange("16:23").format.rowHeight = 30;
sheet.getRange("27:32").format.rowHeight = 30;
sheet.getRange("35:39").format.rowHeight = 28;

sheet.freezePanes.freezeRows(6);

const inspect = await wb.inspect({
  kind: "table",
  sheetId: "Приложение N 2",
  range: "A1:E39",
  tableMaxRows: 40,
  tableMaxCols: 5,
  maxChars: 5000,
});
console.log(inspect.ndjson);

const errors = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const preview = await wb.render({
  sheetName: "Приложение N 2",
  range: "A1:E39",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(outPath);
console.log(`saved:${outPath}`);
console.log(`preview:${previewPath}`);
