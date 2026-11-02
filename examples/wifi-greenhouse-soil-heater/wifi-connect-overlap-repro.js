// SPDX-License-Identifier: MIT
// Minimal Web IDE/REPL reproduction for overlapping Wifi.connect callbacks.

var wifi = require("Wifi");
var callbackCount = 0;

function result(name) {
  return function (err) {
    callbackCount++;
    print(name, "callback:", err);
  };
}

print("starting connection 1");

wifi.connect(
  "XFSM-NO-SUCH-AP-1",
  {password: "12345678"},
  result("connection 1")
);

setTimeout(function () {
  print("starting connection 2");

  try {
    wifi.connect(
      "XFSM-NO-SUCH-AP-2",
      {password: "12345678"},
      result("connection 2")
    );

    print("connection 2 returned normally");
  } catch (err) {
    print("connection 2 threw:", err);
  }
}, 6000);

setTimeout(function () {
  print("callback count after 30 seconds:", callbackCount);
  print("details:", wifi.getDetails());
  print("IP:", wifi.getIP());
}, 30000);
