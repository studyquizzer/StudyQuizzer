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

var QuestionCard = function QuestionCard(_ref) {
  var question = _ref.question,
      updateScore = _ref.updateScore;
  var answer = question.answer;
  var initialState = {
    hasClicked: false,
    clickedAnswer: [],
    answer: answer,
    correct: false
  };

  var _React$useState = React.useState(initialState),
      _React$useState2 = _slicedToArray(_React$useState, 2),
      state = _React$useState2[0],
      setstate = _React$useState2[1];

  var type = question.type;
  var options = question.options;

  var setAnswer = function setAnswer(option) {
    if (!state.hasClicked) {
      setstate(function (oldState) {
        return _objectSpread(_objectSpread({}, oldState), {}, {
          hasClicked: true,
          clickedAnswer: option
        });
      });
    }

    if (state.answer === option[1]) {
      updateScore();
    }
  };

  var resortOption = function resortOption(option, value) {
    if (state.hasClicked && state.clickedAnswer[0] === option) {
      if (state.clickedAnswer[1] === answer) {
        return 'bg-success';
      } else {
        return 'bg-danger';
      }
    } else if (state.hasClicked) {
      if (state.answer === value) {
        return 'bg-success';
      } else {
        return '';
      }
    }
  };

  var template = type === 'MCQ' ? /*#__PURE__*/React.createElement("ul", {
    className: "list-group"
  }, /*#__PURE__*/React.createElement("li", {
    className: "list-group-item list-group-item-action",
    style: {
      backgroundColor: '#dddd'
    }
  }, question.text), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption('a', options[0]),
    onClick: function onClick() {
      setAnswer(['a', options[0]]);
    }
  }, /*#__PURE__*/React.createElement("span", null, "A >"), " ", options[0]), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption('b', options[1]),
    onClick: function onClick() {
      setAnswer(['b', options[1]]);
    }
  }, /*#__PURE__*/React.createElement("span", null, "B >"), " ", options[1]), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption('c', options[2]),
    onClick: function onClick() {
      setAnswer(['c', options[2]]);
    }
  }, /*#__PURE__*/React.createElement("span", null, "C >"), " ", options[2]), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption('d', options[3]),
    onClick: function onClick() {
      setAnswer(['d', options[3]]);
    }
  }, /*#__PURE__*/React.createElement("span", null, "D >"), " ", options[3])) : /*#__PURE__*/React.createElement("ul", {
    className: "list-group"
  }, /*#__PURE__*/React.createElement("li", {
    className: "list-group-item list-group-item-action",
    style: {
      backgroundColor: '#dddd'
    }
  }, question.text), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption(true, 'True'),
    onClick: function onClick() {
      setAnswer([true, 'True']);
    }
  }, "true"), /*#__PURE__*/React.createElement("li", {
    className: 'list-group-item list-group-item-action ' + resortOption(false, 'False'),
    onClick: function onClick() {
      setAnswer([false, 'False']);
    }
  }, "false"));
  return template;
};

var _default = QuestionCard;
exports["default"] = _default;