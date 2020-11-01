'use strict';

const element = React.createElement;
const domContainer = document.querySelector('#entry_point');

console.log(element)
alert()

class test extends React.Component {
    constructor(props) {
        super(props);
        this.state = { liked: false };
    }
    alert()

    render() {

        return element('button', { onClick: () => this.setState({ liked: true }) },
            'Like'
        )
    }
}
ReactDOM.render(element(test), domContainer);
