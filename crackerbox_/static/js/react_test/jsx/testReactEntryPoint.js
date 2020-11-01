import Question from './question';

const regeneratorRuntime = require('regenerator-runtime');

const element = React.createElement;
const domContainer = document.querySelector('#entry_point');
const hostname = window.location.hostname;

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

const quizzerEntry = () => {
    const initialState = { title: '', questions: [], submitNow: false };
    const [state, setstate] = React.useState(initialState);
    const appendQuestions = (questions, submitNow = false) => {
        if (
            state.questions.length === 0 ||
            (state.questions.length + 1 > 1 &&
                questions.qnNo >
                    state.questions[state.questions.length - 1].qnNo)
        ) {
            setstate((oldstate) => ({
                ...oldstate,
                questions: [...oldstate.questions, questions],
                submitNow: submitNow,
            }));
        }
    };
    React.useEffect(() => {
        if (state.submitNow) {
            handleSubmit();
        }
        return () => {};
    }, [state.submitNow]);

    const handleChange = (event) => {
        event.preventDefault();
        const id = event.target.getAttribute('id');
        setstate({ ...state, [id]: event.target.value });
    };

    const handleSubmit = () => {
        if (state.title === '') {
            alert("Field title can't be empty.");
            return;
        }
        axios
            .post(`https://${hostname}:8000/crackerbox/create_quizzer_test/`, {
                data: state,
            })
            .then((resp) =>
                window.location.replace(`https://${hostname}:8000/crackerbox/`)
            );
    };
    const template = (
        <div className="container-fluid">
            <div
                className="row align-items-center"
                style={{
                    height: '100%',
                    backgroundColor: 'rgba(209, 232, 241, 0.09)',
                }}
            >
                <div className="col-12 col-md-3 px-4">
                    <form>
                        <div className="form-group no-padding text-center">
                            <label htmlFor="title">Title</label>
                            <input
                                type="text"
                                className="form-control"
                                id="title"
                                aria-describedby="titleInput"
                                value={state.title}
                                onChange={handleChange}
                            />
                            <small
                                id="titleInput"
                                className="form-text text-muted"
                            >
                                What is the title of this test?
                            </small>
                        </div>
                    </form>
                </div>
                <div className="col-12 col-md-9 px-0">
                    <div className="card mx-2">
                        <Question
                            qnNo={state.questions.length + 1}
                            appendQuestions={appendQuestions}
                            all_questions={state.questions}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
    return template;
};

ReactDOM.render(element(quizzerEntry), domContainer);
