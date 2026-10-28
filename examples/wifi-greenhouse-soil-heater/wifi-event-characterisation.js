// SPDX-License-Identifier: MIT
// Project-authored XFSM example diagnostic; not adapted from third-party code.
// Requires an ESP32-C3 Espruino build with the built-in Wifi module.
// Credentials are read from wifi-event-config.json in Espruino Storage and
// are never printed by this program.

(function () {
  var wifi = require("Wifi");
  var Storage = require("Storage");
  var CONFIG_FILE = "wifi-event-config.json";
  var TRACE_PREFIX = "WIFI_DIAG ";
  var startedAt = getTime();
  var sequence = 0;
  var connectOperation = 0;
  var disconnectOperation = 0;
  var connectTimer;
  var config;
  var lastProfileName;

  if (global.WifiEventCharacterisation &&
      typeof global.WifiEventCharacterisation.stop === "function") {
    global.WifiEventCharacterisation.stop();
  }

  function safeValue(value, depth) {
    var kind = typeof value;
    var result;
    var key;

    if (value === null) return null;
    if (kind === "undefined") return null;
    if (kind === "string" || kind === "number" || kind === "boolean") {
      return value;
    }
    if (kind === "function") return "[function]";
    if (depth >= 5) return "[maximum depth]";

    result = Array.isArray(value) ? [] : {};
    for (key in value) {
      if (Object.prototype.hasOwnProperty.call(value, key)) {
        var lowerKey = key.toLowerCase();
        if (lowerKey.indexOf("pass") >= 0 ||
            lowerKey.indexOf("ssid") >= 0) {
          result[key] = "[redacted]";
        } else {
          try {
            result[key] = safeValue(value[key], depth + 1);
          } catch (error) {
            result[key] = "[unreadable: " + String(error) + "]";
          }
        }
      }
    }
    return result;
  }

  function trace(kind, name, details) {
    var record = {
      format: "xfsm-wifi-event-characterisation-v1",
      sequence: ++sequence,
      elapsedMs: Math.round((getTime() - startedAt) * 1000),
      dateMs: Date.now(),
      kind: kind,
      name: name
    };
    if (details !== undefined) record.details = safeValue(details, 0);
    print(TRACE_PREFIX + JSON.stringify(record));
  }

  function observe(label) {
    var observation = {};
    try {
      observation.wifiDetails = safeValue(wifi.getDetails(), 0);
    } catch (error) {
      observation.getDetailsError = String(error);
    }
    try {
      observation.ip = safeValue(wifi.getIP(), 0);
    } catch (error) {
      observation.getIPError = String(error);
    }
    trace("observation", label, observation);
    return observation;
  }

  function nativeListener(name) {
    return function (details) {
      trace("native_event", name, {eventDetails: details});
      observe("after_native_" + name);
    };
  }

  var listeners = {
    associated: nativeListener("associated"),
    connected: nativeListener("connected"),
    disconnected: nativeListener("disconnected"),
    dhcp_timeout: nativeListener("dhcp_timeout")
  };

  function installListeners() {
    wifi.on("associated", listeners.associated);
    wifi.on("connected", listeners.connected);
    wifi.on("disconnected", listeners.disconnected);
    wifi.on("dhcp_timeout", listeners.dhcp_timeout);
    trace("diagnostic", "listeners_installed", {
      events: ["associated", "connected", "disconnected", "dhcp_timeout"]
    });
  }

  function removeListeners() {
    wifi.removeListener("associated", listeners.associated);
    wifi.removeListener("connected", listeners.connected);
    wifi.removeListener("disconnected", listeners.disconnected);
    wifi.removeListener("dhcp_timeout", listeners.dhcp_timeout);
    trace("diagnostic", "listeners_removed");
  }

  function profileNames() {
    var names = [];
    var name;
    if (!config || !config.profiles) return names;
    for (name in config.profiles) {
      if (Object.prototype.hasOwnProperty.call(config.profiles, name)) {
        names.push(name);
      }
    }
    return names;
  }

  function reloadConfig() {
    config = Storage.readJSON(CONFIG_FILE, true);
    if (!config || !config.profiles) {
      config = undefined;
      trace("configuration", "missing_or_invalid", {storageFile: CONFIG_FILE});
      return false;
    }
    trace("configuration", "loaded", {
      storageFile: CONFIG_FILE,
      profiles: profileNames(),
      startupProfile: config.startupProfile || null,
      connectTimeoutMs: config.connectTimeoutMs || null
    });
    return true;
  }

  function cancelConnectTimeout(reason) {
    if (!connectTimer) return;
    clearTimeout(connectTimer);
    connectTimer = undefined;
    trace("timer", "connect_timeout_cancelled", {reason: reason});
  }

  function armConnectTimeout(operation, timeoutMs) {
    if (!(timeoutMs > 0)) return;
    connectTimer = setTimeout(function () {
      connectTimer = undefined;
      trace("timer", "application_connect_timeout", {
        operation: operation,
        timeoutMs: timeoutMs,
        nativeConnectionLeftRunning: true
      });
      observe("at_application_connect_timeout");
    }, timeoutMs);
    trace("timer", "connect_timeout_armed", {
      operation: operation,
      timeoutMs: timeoutMs
    });
  }

  function connect(profileName, timeoutMs) {
    var profile;
    var options;
    var operation;

    if (!config && !reloadConfig()) return false;
    profile = config.profiles[profileName];
    if (!profile || typeof profile.ssid !== "string" || !profile.ssid) {
      trace("configuration", "profile_invalid", {profile: profileName});
      return false;
    }

    cancelConnectTimeout("new_connect_request");
    lastProfileName = profileName;
    operation = ++connectOperation;
    if (!(timeoutMs >= 0)) timeoutMs = config.connectTimeoutMs;
    options = {};
    if (typeof profile.password === "string") options.password = profile.password;
    if (profile.allChannels === true) options.allChannels = true;

    trace("operation", "connect_requested", {
      operation: operation,
      profile: profileName,
      ssid: profile.ssid,
      timeoutMs: timeoutMs || null
    });
    observe("before_connect_" + operation);
    armConnectTimeout(operation, timeoutMs);

    try {
      wifi.connect(profile.ssid, options, function (error, details) {
        if (operation === connectOperation) {
          cancelConnectTimeout("connect_callback");
        }
        trace("callback", "connect", {
          operation: operation,
          callbackForCurrentOperation: operation === connectOperation,
          error: error === null || error === undefined ? null : String(error),
          callbackDetails: details
        });
        observe("after_connect_callback_" + operation);
      });
    } catch (error) {
      cancelConnectTimeout("connect_exception");
      trace("exception", "connect", {
        operation: operation,
        error: String(error)
      });
      observe("after_connect_exception_" + operation);
      return false;
    }
    return true;
  }

  function disconnect() {
    var operation = ++disconnectOperation;
    var callbackCount = 0;
    cancelConnectTimeout("disconnect_request");
    trace("operation", "disconnect_requested", {operation: operation});
    observe("before_disconnect_" + operation);
    try {
      wifi.disconnect(function () {
        callbackCount++;
        trace("callback", "disconnect", {
          operation: operation,
          callbackCount: callbackCount
        });
        observe("after_disconnect_callback_" + operation + "_" + callbackCount);
      });
    } catch (error) {
      trace("exception", "disconnect", {
        operation: operation,
        error: String(error)
      });
      observe("after_disconnect_exception_" + operation);
      return false;
    }
    return true;
  }

  function reconnect(profileName, timeoutMs) {
    return connect(profileName || lastProfileName, timeoutMs);
  }

  function stop() {
    cancelConnectTimeout("diagnostic_stop");
    removeListeners();
    trace("diagnostic", "stopped", {
      wifiDisconnectNotRequested: true
    });
  }

  global.WifiEventCharacterisation = {
    connect: connect,
    reconnect: reconnect,
    disconnect: disconnect,
    observe: observe,
    reloadConfig: reloadConfig,
    cancelConnectTimeout: cancelConnectTimeout,
    stop: stop
  };

  trace("diagnostic", "started", {
    board: process.env.BOARD || "UNKNOWN",
    version: process.env.VERSION || "UNKNOWN",
    gitCommit: process.env.GIT_COMMIT || "UNKNOWN",
    configFile: CONFIG_FILE
  });
  installListeners();
  observe("startup");

  if (reloadConfig() && config.startupProfile) {
    setTimeout(function () {
      connect(config.startupProfile, config.connectTimeoutMs);
    }, 0);
  }
}());
