"use strict";

var _question = _interopRequireDefault(require("./question"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && Symbol.iterator in Object(iter)) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return; var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

var regeneratorRuntime = require('regenerator-runtime');

var element = React.createElement;
var domContainer = document.querySelector('#entry_point');
var hostname = window.location.hostname;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

var quizzerEntry = function quizzerEntry() {
  var initialState = {
    title: '',
    questions: [],
    submitNow: false
  };

  var _React$useState = React.useState(initialState),
      _React$useState2 = _slicedToArray(_React$useState, 2),
      state = _React$useState2[0],
      setstate = _React$useState2[1];

  var appendQuestions = function appendQuestions(questions) {
    var submitNow = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

    if (state.questions.length === 0 || state.questions.length + 1 > 1 && questions.qnNo > state.questions[state.questions.length - 1].qnNo) {
      setstate(function (oldstate) {
        return _objectSpread(_objectSpread({}, oldstate), {}, {
          questions: [].concat(_toConsumableArray(oldstate.questions), [questions]),
          submitNow: submitNow
        });
      });
    }
  };

  React.useEffect(function () {
    if (state.submitNow) {
      handleSubmit();
    }

    return function () {};
  }, [state.submitNow]);

  var handleChange = function handleChange(event) {
    event.preventDefault();
    var id = event.target.getAttribute('id');
    setstate(_objectSpread(_objectSpread({}, state), {}, _defineProperty({}, id, event.target.value)));
  };

  var handleSubmit = function handleSubmit() {
    if (state.title === '') {
      alert("Field title can't be empty.");
      return;
    }

    axios.post("https://".concat(hostname, ":8000/crackerbox/create_quizzer_test/"), {
      data: state
    }).then(function (resp) {
      return window.location.replace("https://".concat(hostname, ":8000/crackerbox/"));
    });
  };

  var template = /*#__PURE__*/React.createElement("div", {
    className: "container-fluid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "row align-items-center",
    style: {
      height: '100%',
      backgroundColor: 'rgba(209, 232, 241, 0.09)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "col-12 col-md-3 px-4"
  }, /*#__PURE__*/React.createElement("form", null, /*#__PURE__*/React.createElement("div", {
    className: "form-group no-padding text-center"
  }, /*#__PURE__*/React.createElement("label", {
    htmlFor: "title"
  }, "Title"), /*#__PURE__*/React.createElement("input", {
    type: "text",
    className: "form-control",
    id: "title",
    "aria-describedby": "titleInput",
    value: state.title,
    onChange: handleChange
  }), /*#__PURE__*/React.createElement("small", {
    id: "titleInput",
    className: "form-text text-muted"
  }, "What is the title of this test?")))), /*#__PURE__*/React.createElement("div", {
    className: "col-12 col-md-9 px-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card mx-2"
  }, /*#__PURE__*/React.createElement(_question["default"], {
    qnNo: state.questions.length + 1,
    appendQuestions: appendQuestions,
    all_questions: state.questions
  })))));
  return template;
};

ReactDOM.render(element(quizzerEntry), domContainer);