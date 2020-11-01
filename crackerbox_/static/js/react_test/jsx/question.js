const regeneratorRuntime = require('regenerator-runtime');

const element = React.createElement;

const question = (props) => {
    const initialState = {
        question_type: 'Multiple Choice',
        question: '',
        answer: '',
        option1: '',
        option2: '',
        option3: '',
        qnNo: props.qnNo,
    };
    const [state, setstate] = React.useState(initialState);
    const isStateValid = (state) => {
        for (const [key, value] of Object.entries(state)) {
            if (value === '') {
                if (state.question_type !== 'True or False') {
                    alert(`Blank field ${key} detected`);
                    return false;
                } else {
                    if (key === 'question' || key === 'answer') {
                        alert(`Blank field ${key} detected`);
                        return false;
                    }
                }
            }
        }
        return true;
    };
    const handleQuestionTypeSelect = (event) => {
        event.preventDefault();
        setstate({ ...state, question_type: event.target.text });
    };
    const handleInput = (event) => {
        event.preventDefault();
        const id = event.target.getAttribute('id');

        setstate({ ...state, [id]: event.target.value });
    };
    const handleNext = () => {
        if (!isStateValid(state)) {
            return;
        }
        props.appendQuestions(state);
        setstate(initialState);
    };
    const handlePrev = () => {
        setstate(props.all_questions[state.qnNo - 2]);
    };
    const handleSubmit = () => {
        if (!isStateValid(state)) {
            return;
        }
        props.appendQuestions(state, true);
    };

    React.useEffect(() => {
        setstate({ ...state, qnNo: props.qnNo });
        return () => {};
    }, [props.qnNo]);

    const template = (
        <div className="mx-3">
            <p className="p-1">No: {state.qnNo}</p>
            <div className="input-group mb-3">
                <input
                    id="question"
                    type="text"
                    className="form-control"
                    placeholder="Question text"
                    aria-label="Question"
                    onChange={handleInput}
                    value={state.question}
                />
            </div>

            <div className="input-group mb-3">
                <div className="input-group-prepend">
                    <button type="button" className="btn btn-outline-secondary">
                        Type | {state.question_type}
                    </button>
                    <button
                        type="button"
                        className="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                    >
                        <span className="sr-only">Toggle Dropdown</span>
                    </button>
                    <div className="dropdown-menu">
                        <a
                            className="dropdown-item"
                            href="#"
                            onClick={handleQuestionTypeSelect}
                        >
                            Multiple Choice
                        </a>
                        <a
                            className="dropdown-item"
                            href="#"
                            onClick={handleQuestionTypeSelect}
                        >
                            True or False
                        </a>
                    </div>
                </div>
                <input
                    id="answer"
                    type="text"
                    placeholder="Answer (i.e true, false, ...)"
                    className="form-control"
                    value={state.answer}
                    onChange={handleInput}
                    aria-label="Text input with segmented dropdown button"
                />
            </div>

            <div className="input-group mb-3">
                <input
                    id="option1"
                    type="text"
                    className="form-control"
                    placeholder="option1"
                    aria-label="option1"
                    value={state.option1}
                    onChange={handleInput}
                    disabled={
                        state.question_type !== 'Multiple Choice' ? true : false
                    }
                />
            </div>

            <div className="input-group mb-3">
                <input
                    id="option2"
                    type="text"
                    className="form-control"
                    placeholder="option2"
                    aria-label="option2"
                    onChange={handleInput}
                    value={state.option2}
                    disabled={
                        state.question_type !== 'Multiple Choice' ? true : false
                    }
                />
            </div>

            <div className="input-group mb-3">
                <input
                    id="option3"
                    type="text"
                    className="form-control"
                    placeholder="option3"
                    aria-label="option3"
                    value={state.option3}
                    onChange={handleInput}
                    disabled={
                        state.question_type !== 'Multiple Choice' ? true : false
                    }
                />
            </div>
            <div
                className="btn-group pb-3"
                role="group"
                aria-label="Basic example"
            >
                <button
                    type="button"
                    className="btn btn-dark"
                    disabled={state.qnNo === 1 ? true : false}
                    onClick={handlePrev}
                >
                    prev
                </button>
                <button
                    type="button"
                    className="btn btn-dark"
                    onClick={handleSubmit}
                >
                    submit
                </button>
                <button
                    type="button"
                    className="btn btn-dark"
                    onClick={handleNext}
                >
                    next
                </button>
            </div>
        </div>
    );
    return template;
};

export default question;
