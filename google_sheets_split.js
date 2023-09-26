//Compares BU from MainSheet (which is ELC data) with that of the TechLeader sheet
//It then creates a new sheet for each TechLeader name that is found and adds the corresponding row from MainSheet
//The purpose is to split employee info by tech leader for things like software license evals 


function createSheetsFromMainSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var mainSheet = spreadsheet.getSheetByName("MainSheet");
  var mainData = mainSheet.getDataRange().getValues();
  
  var techLeaderSheet = spreadsheet.getSheetByName("TechLeader");
  var techLeaderData = techLeaderSheet.getDataRange().getValues();
  
  for (var i = 1; i < mainData.length; i++) {
    var mainValue = mainData[i][5]; // Value in Column F of MainSheet
    for (var j = 1; j < techLeaderData.length; j++) {
      var techLeaderValue = techLeaderData[j][0]; // Value in Column A of TechLeader sheet
      
      if (mainValue == techLeaderValue) {
        var targetSheetName = techLeaderData[j][5]; // Value in Column F of TechLeader sheet
        var targetSheet = spreadsheet.getSheetByName(targetSheetName);
        if (!targetSheet) {
          targetSheet = spreadsheet.insertSheet(targetSheetName);
          targetSheet.appendRow(mainSheet.getRange(1, 1, 1, mainSheet.getLastColumn()).getValues()[0]);
        }
        targetSheet.appendRow(mainData[i]);
        break;
      }
    }
  }
}
