"use strict";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

var regeneratorRuntime = require('regenerator-runtime');

var _require = require('./questionCard'),
    QuestionCard = _require["default"];

var element = React.createElement;
var domContainer = document.querySelector('#entry_point');
var hostname = window.location.hostname;
hostname = hostname === "127.0.0.1" ? "127.0.0.1:8000" : "studyquizzer.com";
var initialState = {
  questions: [],
  status: 0,
  isLoading: true,
  score: 0,
  total: 0
};
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

var quizzerEntry = function quizzerEntry() {
  var _React$useState = React.useState(initialState),
      _React$useState2 = _slicedToArray(_React$useState, 2),
      state = _React$useState2[0],
      setstate = _React$useState2[1];

  var populate = /*#__PURE__*/function () {
    var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
      var _yield$axios$get$catc, data;

      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              _context.next = 2;
              return axios.get("https://".concat(hostname, "/docjson/crackerbox/documents/").concat(unique_id))["catch"](function (err) {
                return console.log(err);
              });

            case 2:
              _yield$axios$get$catc = _context.sent;
              data = _yield$axios$get$catc.data;

            case 4:
              if (!(data.status === 1 || data.status === 0)) {
                _context.next = 11;
                break;
              }

              _context.next = 7;
              return axios.get("https://".concat(hostname, "/docjson/crackerbox/documents/").concat(unique_id))["catch"](function (err) {
                return console.log(err);
              });

            case 7:
              data = _context.sent;
              data = data.data;
              _context.next = 4;
              break;

            case 11:
              if (data.status === 2) {
                setstate(_objectSpread(_objectSpread({}, data), {}, {
                  isLoading: false,
                  total: data.questions.length,
                  score: 0
                }));
              }

            case 12:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }));

    return function populate() {
      return _ref.apply(this, arguments);
    };
  }();

  var updateScore = function updateScore() {
    setstate(function (oldState) {
      return _objectSpread(_objectSpread({}, oldState), {}, {
        score: oldState.score + 1
      });
    });
  };

  React.useEffect(function () {
    populate();
    return function () {};
  }, []);
  React.useEffect(function () {
    axios.post("https://".concat(hostname, "/crackerbox/save_result/"), {
      score: state.score,
      total: state.total,
      id: unique_id
    })["catch"](function (err) {
      return console.log(err);
    });
    return function () {};
  }, [state.score, state.questions]);
  var template = /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, state.isLoading ? /*#__PURE__*/React.createElement("div", {
    className: "text-center align-items-center"
  }, /*#__PURE__*/React.createElement("div", {
    className: "spinner-border text-dark my-5",
    role: "status"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sr-only"
  }, "Loading..."))) : /*#__PURE__*/React.createElement("div", {
    className: "row"
  }, state.questions.map(function (d, ix) {
    return /*#__PURE__*/React.createElement("div", {
      className: "col-12 col-md-6",
      key: ix
    }, /*#__PURE__*/React.createElement("div", {
      className: "px-2"
    }, /*#__PURE__*/React.createElement(QuestionCard, {
      question: d,
      id: unique_id,
      updateScore: updateScore
    })));
  })));
  return template;
};

ReactDOM.render(element(quizzerEntry), domContainer);