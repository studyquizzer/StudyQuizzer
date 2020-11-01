

const QuestionCard = ({ question, updateScore }) => {
    const answer = question.answer;
    const initialState = {
        hasClicked: false,
        clickedAnswer: [],
        answer: answer,
        correct: false,
    };
    const [state, setstate] = React.useState(initialState);
    const type = question.type;
    let options = question.options;
    const setAnswer = (option) => {
        if (!state.hasClicked) {
            setstate(oldState => ({
                ...oldState,
                hasClicked: true,
                clickedAnswer: option,
            }));
        }
        if (state.answer === option[1]) {
            updateScore();
        }
    };

    const resortOption = (option, value) => {
        if (state.hasClicked && state.clickedAnswer[0] === option) {
            if (state.clickedAnswer[1] === answer) {
                return 'bg-success'
            }
            else {
                return 'bg-danger'
            }
        } else  if (state.hasClicked) {
            if (state.answer === value) {
                return 'bg-success';
            } else {
                return '';
            }
        }
    };

    const template =
        type === 'MCQ' ? (
            <ul className="list-group">
                <li
                    className="list-group-item list-group-item-action"
                    style={{ backgroundColor: '#dddd' }}
                >
                    {question.text}
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption('a', options[0])
                    }
                    onClick={() => {
                        setAnswer(['a', options[0]]);
                    }}
                >
                    <span>A ></span> {options[0]}
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption('b', options[1])
                    }
                    onClick={() => {
                        setAnswer(['b', options[1]]);
                    }}
                >
                    <span>B ></span> {options[1]}
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption('c', options[2])
                    }
                    onClick={() => {
                        setAnswer(['c', options[2]]);
                    }}
                >
                    <span>C ></span> {options[2]}
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption('d', options[3])
                    }
                    onClick={() => {
                        setAnswer(['d', options[3]]);
                    }}
                >
                    <span>D ></span> {options[3]}
                </li>
            </ul>
        ) : (
            <ul className="list-group">
                <li
                    className="list-group-item list-group-item-action"
                    style={{ backgroundColor: '#dddd' }}
                >
                    {question.text}
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption(true, 'True')
                    }
                    onClick={() => {
                        setAnswer([true, 'True']);
                    }}
                >
                    true
                </li>
                <li
                    className={
                        'list-group-item list-group-item-action ' +
                        resortOption(false, 'False')
                    }
                    onClick={() => {
                        setAnswer([false, 'False']);
                    }}
                >
                    false
                </li>
            </ul>
        );
    return template;
};

export default QuestionCard;