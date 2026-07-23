import { Workbook } from "@oai/artifact-tool";

const wb = Workbook.create();
console.log(wb.help("*", {
  search: "print|page|layout|margin|orientation|fit|scale|paper",
  include: "index,examples,notes",
  maxChars: 12000,
}).ndjson);
