# Webbanhang
function doPost(e) {
  const output = ContentService.createTextOutput();
  output.setMimeType(ContentService.MimeType.JSON);
  // Kiểm tra xem e và e.parameter có tồn tại không
  if (!e || !e.parameter) {
    return output.setContent(JSON.stringify({ result: 'error', message: 'Invalid request' }));
  }
  const data = JSON.parse(e.postData.contents);
  // Gọi hàm run với dữ liệu từ yêu cầu
  const result = run(data);

  return output.setContent(JSON.stringify(result));
}

function run(data) {
  const output = { result: 'success' }; // Mặc định trả về thành công
  const date = data.date;
  const email = data.email;
  const name = data.name;
  const code = data.code;
  const ip = data.ip;

  const sheetId = '1a88YWHlNyaRP9v8MeOMhRnIzr5sIoRKE6m0AHYumKWc'; // Thay thế bằng ID của Google Sheets
  const sheet = SpreadsheetApp.openById(sheetId).getSheetByName('anh'); // Đảm bảo tên Sheet chính xác

  // Thêm một hàng mới vào Google Sheets
  sheet.appendRow([date,email, name, code, ip]);

  return output; // Trả về kết quả
}