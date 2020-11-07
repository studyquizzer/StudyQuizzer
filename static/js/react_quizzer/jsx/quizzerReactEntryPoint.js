const regeneratorRuntime = require('regenerator-runtime');
const { default: QuestionCard } = require('./questionCard');

const element = React.createElement;
const domContainer = document.querySelector('#entry_point');
const hostname = window.location.hostname;
console.log(hostname)
console.log(hostname)
console.log(hostname)
console.log(hostname)
console.log("hostname")
const initialState = {
    questions: [],
    status: 0,
    isLoading: true,
    score: 0,
    total: 0,
};

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

const quizzerEntry = () => {
    const [state, setstate] = React.useState(initialState);

    const populate = async () => {
        let { data } = await axios
            .get(
                `https://${hostname}/docjson/crackerbox/documents/${unique_id}`
            )
            .catch((err) => console.log(err));
        while (data.status === 1 || data.status === 0) {
            data = await axios
                .get(
                    `https://${hostname}/docjson/crackerbox/documents/${unique_id}`
                )
                .catch((err) => console.log(err));
            data = data.data;
        }

        if (data.status === 2) {
            setstate({
                ...data,
                isLoading: false,
                total: data.questions.length,
                score: 0,
            });
        }
    };

    const updateScore = () => {
        setstate((oldState) => ({ ...oldState, score: oldState.score + 1 }));
    };

    React.useEffect(() => {
        populate();
        return () => {};
    }, []);

    React.useEffect(() => {
        axios
            .post(`https://${hostname}/crackerbox/save_result/`, {
                score: state.score,
                total: state.total,
                id: unique_id,
            })
            .catch((err) => console.log(err));
        return () => {};
    }, [state.score, state.questions]);

    const template = (
        <div className="container">
            {state.isLoading ? (
                <div className="text-center align-items-center">
                    <div
                        className="spinner-border text-dark my-5"
                        role="status"
                    >
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
            ) : (
                <div className="row">
                    {state.questions.map((d, ix) => (
                        <div className="col-12 col-md-6" key={ix}>
                            <div className="px-2">
                                <QuestionCard
                                    question={d}
                                    id={unique_id}
                                    updateScore={updateScore}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
    return template;
};

ReactDOM.render(element(quizzerEntry), domContainer);
