"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

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

var question = function question(props) {
  var initialState = {
    question_type: 'Multiple Choice',
    question: '',
    answer: '',
    option1: '',
    option2: '',
    option3: '',
    qnNo: props.qnNo
  };

  var _React$useState = React.useState(initialState),
      _React$useState2 = _slicedToArray(_React$useState, 2),
      state = _React$useState2[0],
      setstate = _React$useState2[1];

  var isStateValid = function isStateValid(state) {
    for (var _i2 = 0, _Object$entries = Object.entries(state); _i2 < _Object$entries.length; _i2++) {
      var _Object$entries$_i = _slicedToArray(_Object$entries[_i2], 2),
          key = _Object$entries$_i[0],
          value = _Object$entries$_i[1];

      if (value === '') {
        if (state.question_type !== 'True or False') {
          alert("Blank field ".concat(key, " detected"));
          return false;
        } else {
          if (key === 'question' || key === 'answer') {
            alert("Blank field ".concat(key, " detected"));
            return false;
          }
        }
      }
    }

    return true;
  };

  var handleQuestionTypeSelect = function handleQuestionTypeSelect(event) {
    event.preventDefault();
    setstate(_objectSpread(_objectSpread({}, state), {}, {
      question_type: event.target.text
    }));
  };

  var handleInput = function handleInput(event) {
    event.preventDefault();
    var id = event.target.getAttribute('id');
    setstate(_objectSpread(_objectSpread({}, state), {}, _defineProperty({}, id, event.target.value)));
  };

  var handleNext = function handleNext() {
    if (!isStateValid(state)) {
      return;
    }

    props.appendQuestions(state);
    setstate(initialState);
  };

  var handlePrev = function handlePrev() {
    setstate(props.all_questions[state.qnNo - 2]);
  };

  var handleSubmit = function handleSubmit() {
    if (!isStateValid(state)) {
      return;
    }

    props.appendQuestions(state, true);
  };

  React.useEffect(function () {
    setstate(_objectSpread(_objectSpread({}, state), {}, {
      qnNo: props.qnNo
    }));
    return function () {};
  }, [props.qnNo]);
  var template = /*#__PURE__*/React.createElement("div", {
    className: "mx-3"
  }, /*#__PURE__*/React.createElement("p", {
    className: "p-1"
  }, "No: ", state.qnNo), /*#__PURE__*/React.createElement("div", {
    className: "input-group mb-3"
  }, /*#__PURE__*/React.createElement("input", {
    id: "question",
    type: "text",
    className: "form-control",
    placeholder: "Question text",
    "aria-label": "Question",
    onChange: handleInput,
    value: state.question
  })), /*#__PURE__*/React.createElement("div", {
    className: "input-group mb-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "input-group-prepend"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "btn btn-outline-secondary"
  }, "Type | ", state.question_type), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "btn btn-outline-secondary dropdown-toggle dropdown-toggle-split",
    "data-toggle": "dropdown",
    "aria-haspopup": "true",
    "aria-expanded": "false"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sr-only"
  }, "Toggle Dropdown")), /*#__PURE__*/React.createElement("div", {
    className: "dropdown-menu"
  }, /*#__PURE__*/React.createElement("a", {
    className: "dropdown-item",
    href: "#",
    onClick: handleQuestionTypeSelect
  }, "Multiple Choice"), /*#__PURE__*/React.createElement("a", {
    className: "dropdown-item",
    href: "#",
    onClick: handleQuestionTypeSelect
  }, "True or False"))), /*#__PURE__*/React.createElement("input", {
    id: "answer",
    type: "text",
    placeholder: "Answer (i.e true, false, ...)",
    className: "form-control",
    value: state.answer,
    onChange: handleInput,
    "aria-label": "Text input with segmented dropdown button"
  })), /*#__PURE__*/React.createElement("div", {
    className: "input-group mb-3"
  }, /*#__PURE__*/React.createElement("input", {
    id: "option1",
    type: "text",
    className: "form-control",
    placeholder: "option1",
    "aria-label": "option1",
    value: state.option1,
    onChange: handleInput,
    disabled: state.question_type !== 'Multiple Choice' ? true : false
  })), /*#__PURE__*/React.createElement("div", {
    className: "input-group mb-3"
  }, /*#__PURE__*/React.createElement("input", {
    id: "option2",
    type: "text",
    className: "form-control",
    placeholder: "option2",
    "aria-label": "option2",
    onChange: handleInput,
    value: state.option2,
    disabled: state.question_type !== 'Multiple Choice' ? true : false
  })), /*#__PURE__*/React.createElement("div", {
    className: "input-group mb-3"
  }, /*#__PURE__*/React.createElement("input", {
    id: "option3",
    type: "text",
    className: "form-control",
    placeholder: "option3",
    "aria-label": "option3",
    value: state.option3,
    onChange: handleInput,
    disabled: state.question_type !== 'Multiple Choice' ? true : false
  })), /*#__PURE__*/React.createElement("div", {
    className: "btn-group pb-3",
    role: "group",
    "aria-label": "Basic example"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "btn btn-dark",
    disabled: state.qnNo === 1 ? true : false,
    onClick: handlePrev
  }, "prev"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "btn btn-dark",
    onClick: handleSubmit
  }, "submit"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "btn btn-dark",
    onClick: handleNext
  }, "next")));
  return template;
};

var _default = question;
exports["default"] = _default;