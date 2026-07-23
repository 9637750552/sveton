import fs from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath =
  "C:/Users/alvad/Documents/Sveton/01_docs/operations/contracts/appendix_2_object_inspection_request.xlsx";
const previewPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/checklist_after.png";
const pythonPath =
  "C:/Users/alvad/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
const printSettingsPath =
  "C:/Users/alvad/Documents/Sveton/tmp/xlsx_builder/fix_contract_workbook_print_settings.py";

const CHECK = "☐";

const sections = [
  {
    side: "left",
    row: 2,
    title: "1. До начала осмотра",
    items: [
      "Разместить термометр в предполагаемом месте установки АКБ.",
      "Уточнить у Клиента, какие помещения, щиты и трассы можно фотографировать.",
    ],
  },
  {
    side: "left",
    row: 8,
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
    side: "left",
    row: 23,
    title: "3. Потребители и оборудование",
    items: [
      "Измерить или уточнить номинальную и пиковую мощность погружного насоса или другого оборудования, для которого нет исходных данных.",
      "Фото шильдиков циркуляционных насосов и другого резервируемого оборудования, если доступ к ним возможен.",
      "Проверить, все ли заявленные потребители установлены фактически.",
      "Отметить в Отчете об осмотре все спорные или непонятные нагрузки.",
    ],
  },
  {
    side: "right",
    row: 29,
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
    side: "right",
    row: 2,
    title: "5. Обязательно проверить",
    items: [
      "Проверить наличие газового отсекателя для газового котла.",
      "Уточнить у Клиента, есть ли трехфазные нагрузки.",
      "Проверить, нет ли радиатора отопления рядом с местом установки ИБП.",
      "Уточнить состав и толщину стены, если потребуются проходы.",
    ],
  },
  {
    side: "right",
    row: 8,
    title: "6. Заявка на подбор оборудования",
    items: [
      "Заполнить Заявку на подбор оборудования.",
      "Организовать подписание Заявки на подбор оборудования у Клиента либо зафиксировать отказ/невозможность получения подписи.",
    ],
  },
  {
    side: "right",
    row: 14,
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
    side: "right",
    row: 23,
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
  font: { bold: true, size: 8 },
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
  borders: { preset: "all", style: "thin", color: "#B7B7B7" },
};

function rangesFor(side, row) {
  if (side === "left") {
    return {
      header: `A${row}:E${row}`,
      checkCol: "A",
      text: (r) => `B${r}:E${r}`,
    };
  }
  return {
    header: `F${row}:J${row}`,
    checkCol: "F",
    text: (r) => `G${r}:J${r}`,
  };
}

function applyFontName(range) {
  range.format.font.name = "Calibri";
}

function writeSection(sheet, section) {
  const refs = rangesFor(section.side, section.row);
  const header = sheet.getRange(refs.header);
  header.merge();
  header.values = [[section.title]];
  header.format = sectionStyle;
  applyFontName(header);

  section.items.forEach((item, index) => {
    const row = section.row + 1 + index;
    const check = sheet.getRange(`${refs.checkCol}${row}`);
    const text = sheet.getRange(refs.text(row));
    text.merge();
    check.values = [[CHECK]];
    text.values = [[item]];
    check.format = checkStyle;
    text.format = itemStyle;
    applyFontName(check);
    applyFontName(text);
  });
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
const sheet = workbook.worksheets.getItem("Чек-лист");

sheet.getRange("A1:J44").unmerge();
sheet.getRange("A1:J44").clear({ applyTo: "contents" });
sheet.getRange("A1:J39").format = noteStyle;

sheet.getRange("A1:J1").merge();
sheet.getRange("A1").values = [["Чек-лист осмотра места монтажа ИБП"]];
sheet.getRange("A1:J1").format = {
  fill: "#1F4E78",
  font: { bold: true, color: "#FFFFFF", size: 13 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
applyFontName(sheet.getRange("A1:J1"));

for (const section of sections) {
  writeSection(sheet, section);
}

sheet.getRange("A36:J36").merge();
sheet.getRange("A36").values = [["Что не удалось выполнить по чек-листу и почему:"]];
sheet.getRange("A36:J36").format = noteStyle;

sheet.getRange("A37:J37").merge();
sheet.getRange("A38:J38").merge();
sheet.getRange("A37:J38").format = noteStyle;

sheet.getRange("A39:E39").merge();
sheet.getRange("F39:J39").merge();
sheet.getRange("A39").values = [['Исполнитель: __________________ / ____________________  "___" ____________ 20__ г.']];
sheet.getRange("F39").values = [['Ответственное лицо Заказчика: ______________ / ______________  "___" ____________ 20__ г.']];
sheet.getRange("A39:J39").format = noteStyle;

sheet.getRange("A1:J44").format.font.name = "Calibri";
sheet.getRange("A1:J44").format.wrapText = true;
sheet.getRange("1:1").format.rowHeight = 20;
sheet.getRange("2:39").format.rowHeight = 18;
sheet.getRange("15:15").format.rowHeight = 24;
sheet.getRange("24:24").format.rowHeight = 30;
sheet.getRange("37:38").format.rowHeight = 22;
sheet.getRange("39:39").format.rowHeight = 24;

const inspect = await workbook.inspect({
  kind: "table",
  sheetId: "Чек-лист",
  range: "A1:J39",
  tableMaxRows: 40,
  tableMaxCols: 10,
  maxChars: 14000,
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

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(workbookPath);
restorePrintSettings();

console.log(`saved:${workbookPath}`);
console.log(`preview:${previewPath}`);
