import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import MainRouter from './views/MainRouter'
import ToastRoot from './components/ToastRoot'

/**
 * The main component, that gets rendered by the DOM.
 * At the same time it is the main router for the whole app.
 *
 * @component
 * @memberOf components
 */
class App extends Component {
    render() {
        return (
            <div>
                <Router>
                    <ToastRoot />
                    <Switch>
                        <Route
                            path=""
                            component={MainRouter}
                        />
                    </Switch>
                </Router>
            </div>
        );
    }
}

export default App;