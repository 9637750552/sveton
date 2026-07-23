import fs from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const previewPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/checklist_portrait_verify.png";
const pythonPath =
  "C:/Users/alvad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
const printSettingsPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/fix_contract_workbook_print_settings.py";

const CHECK = "☐";
const sheetName = "Чек-лист книжный";

const sections = [
  {
    title: "1. До начала осмотра",
    items: [
      "Разместить термометр в предполагаемом месте установки АКБ.",
      "Уточнить у Клиента, какие помещения, щиты и трассы можно фотографировать.",
    ],
  },
  {
    title: "2. Щит и электросеть",
    items: [
      'Фото открытого щита "на столбе".',
      "Фото основного щита до снятия защитной крышки.",
      "Фото списка потребителей, если он прилагается к щиту.",
      "Снять защитную крышку щита.",
      "Фото открытого щита полностью.",
      "Фото щита и номиналов каждого ряда со всех сторон.",
      "Проверить PE/N шины.",
      "Измерить напряжение на каждой фазе.",
      "Установить соответствие автоматов и нагрузок, планируемых в резерв.",
      "Заполнить в Отчете об осмотре информацию по автоматам и нагрузкам из резервной группы.",
      "Проверить наличие мастер-выключателя, определить, какие потребители он обеспечивает, сделать фото.",
      "Фото показаний термометра, записать эти показания.",
      "Проверить наличие дополнительных щитов, которые относятся к работам по выделению резервной группы.",
    ],
  },
  {
    title: "3. Потребители и оборудование",
    items: [
      "Измерить или уточнить номинальную и пиковую мощность погружного насоса или другого оборудования, для которого нет исходных данных.",
      "Фото шильдиков циркуляционных насосов и другого резервируемого оборудования, если доступ к ним возможен.",
      "Проверить, все ли заявленные потребители установлены фактически.",
      "Отметить в Отчете об осмотре все спорные или непонятные нагрузки.",
    ],
  },
  {
    title: "4. Место установки ИБП и трасса",
    items: [
      "Сфотографировать место установки ИБП, инвертора или АКБ по кругу.",
      "Записать размеры помещения, если это нужно для монтажа.",
      "Осмотреть предполагаемую трассу кабеля.",
      "Фото трассы на всем протяжении.",
      "Фото мест проходов через стены или перекрытия.",
    ],
  },
  {
    title: "5. Обязательно проверить",
    items: [
      "Проверить наличие газового отсекателя для газового котла.",
      "Уточнить у Клиента, есть ли трехфазные нагрузки.",
      "Проверить, нет ли радиатора отопления рядом с местом установки ИБП.",
      "Уточнить состав и толщину стены, если потребуются проходы.",
    ],
  },
  {
    title: "6. Заявка на подбор оборудования",
    items: [
      "Заполнить Заявку на подбор оборудования.",
      "Организовать подписание Заявки на подбор оборудования у Клиента либо зафиксировать отказ/невозможность получения подписи.",
    ],
  },
  {
    title: "7. Материалы для отправки Заказчику",
    items: [
      "Фото или скан подписанной Заявки на подбор оборудования либо фиксация отказа/невозможности получения подписи.",
      "Полностью заполненный Отчет об осмотре.",
      "Настоящий заполненный чек-лист.",
      "Скриншот координат Объекта.",
      "Фотоотчет.",
    ],
  },
  {
    title: "8. Завершение",
    items: [
      "Проверено, что все действия по чек-листу выполнены или отмечены как невыполнимые.",
      "В Отчете об осмотре указано, что не удалось проверить и почему.",
      "Комплект материалов передан Заказчику.",
    ],
  },
];

const sectionStyle = {
  fill: "#D9EAF7",
  font: { bold: true, size: 9 },
  verticalAlignment: "center",
  borders: {
    top: { style: "medium", color: "#808080" },
    bottom: { style: "thin", color: "#B7B7B7" },
    left: { style: "thin", color: "#B7B7B7" },
    right: { style: "thin", color: "#B7B7B7" },
  },
};
const itemStyle = {
  fill: "#FFFFFF",
  font: { size: 8 },
  wrapText: true,
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#B7B7B7" },
};
const checkStyle = {
  fill: "#FFFFFF",
  font: { size: 8 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#B7B7B7" },
};
const noteStyle = {
  fill: "#FFFFFF",
  font: { size: 8 },
  wrapText: true,
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
};

function fmt(range, style) {
  range.format = style;
  range.format.font.name = "Calibri";
}

function mergeValue(sheet, range, value, style) {
  const target = sheet.getRange(range);
  target.merge();
  target.values = [[value]];
  fmt(target, style);
}

function restorePrintSettings() {
  const result = spawnSync(pythonPath, [printSettingsPath], { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(result.stderr || "Failed to restore print settings");
  }
  if (result.stdout.trim()) console.log(result.stdout.trim());
}

const input = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const sheet = workbook.worksheets.getOrAdd(sheetName);

sheet.showGridLines = false;
sheet.getRange("A1:D80").unmerge();
sheet.getRange("A1:D80").clear({ applyTo: "all" });

mergeValue(sheet, "A1:D1", "Чек-лист осмотра места монтажа ИБП", {
  fill: "#1F4E78",
  font: { bold: true, color: "#FFFFFF", size: 13 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
});
mergeValue(sheet, "A2:D2", "Книжный вариант для печати", {
  fill: "#FFFFFF",
  font: { italic: true, color: "#666666", size: 8 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
});

let row = 4;
for (const section of sections) {
  mergeValue(sheet, `A${row}:D${row}`, section.title, sectionStyle);
  row += 1;

  for (const item of section.items) {
    sheet.getRange(`A${row}`).values = [[CHECK]];
    fmt(sheet.getRange(`A${row}`), checkStyle);
    mergeValue(sheet, `B${row}:D${row}`, item, itemStyle);
    row += 1;
  }

  row += 1;
}

mergeValue(sheet, `A${row}:D${row}`, "Что не удалось выполнить по чек-листу и почему:", noteStyle);
row += 1;
mergeValue(sheet, `A${row}:D${row}`, "", noteStyle);
row += 1;
mergeValue(sheet, `A${row}:D${row}`, "", noteStyle);
row += 2;
mergeValue(sheet, `A${row}:D${row}`, 'Исполнитель: __________________ / ____________________  "___" ____________ 20__ г.', noteStyle);
row += 1;
mergeValue(sheet, `A${row}:D${row}`, 'Ответственное лицо Заказчика: ______________ / ______________  "___" ____________ 20__ г.', noteStyle);

const lastRow = row;

sheet.getRange("A:A").format.columnWidth = 5;
sheet.getRange("B:D").format.columnWidth = 21;
sheet.getRange("1:1").format.rowHeight = 22;
sheet.getRange("2:2").format.rowHeight = 18;
sheet.getRange(`3:${lastRow}`).format.rowHeight = 18;
sheet.getRange("13:14").format.rowHeight = 28;
sheet.getRange("25:26").format.rowHeight = 26;
sheet.getRange("45:46").format.rowHeight = 24;
sheet.getRange(`${lastRow - 3}:${lastRow - 2}`).format.rowHeight = 24;
sheet.freezePanes.freezeRows(3);

const inspect = await workbook.inspect({
  kind: "table",
  sheetId: sheetName,
  range: `A1:D${lastRow}`,
  tableMaxRows: 80,
  tableMaxCols: 4,
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
  sheetName,
  range: `A1:D${lastRow}`,
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(workbookPath);
restorePrintSettings();

console.log(`saved:${workbookPath}`);
console.log(`sheet:${sheetName}`);
console.log(`range:A1:D${lastRow}`);
console.log(`preview:${previewPath}`);
