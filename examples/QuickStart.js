// SPDX-License-Identifier: MIT
// Project-authored XFSM example; not adapted from XState documentation.
// Requires an Espruino build with XFSM enabled.

var XFSM = require("XFSM");
var assign = XFSM.assign;

var machine = XFSM.createMachine({
  id: "QuickStart",
  context: { pulses: 0 },
  initial: "idle",
  states: {
    idle: {
      on: {
        START: "running"
      }
    },
    running: {
      on: {
        PULSE: {
          actions: [
            assign({
              pulses: function (context, event) {
                return context.pulses + event.amount;
              }
            }),
            "reportPulse"
          ]
        },
        STOP: "idle"
      }
    }
  }
}, {
  actions: {
    reportPulse: function (context, event) {
      print("pulse", event.amount, "total", context.pulses);
    }
  }
});

var actor = XFSM.createActor(machine);

var subscription = actor.subscribe(function (snapshot) {
  print(snapshot.status, JSON.stringify(snapshot.value),
        JSON.stringify(snapshot.context));
});

actor.start();
actor.send("START");
actor.send({ type: "PULSE", amount: 2 });

var snapshot = actor.getSnapshot();
print(snapshot.matches("running")); // true

actor.send("STOP");
actor.stop();
subscription.unsubscribe();
