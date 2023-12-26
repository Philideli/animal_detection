import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import MainMenu from './components/MainMenu';
import Main from './views/Main';
import RunDetection from './views/RunDetection';
import DetectionDetail from './views/DetectionDetail';
import {join as joinPaths} from 'path';
import DetectionsOverview from './views/DetectionsOverview/DetectionsOverview';

/**
 * This router is responsible for routing to all components.
 * This is the core of the website,
 * all most important features are on this router
 * @memberOf components.views
 * @component
 */
class MainRouter extends Component {

	constructor(props) {
		super(props);
		this.state = {
			mainMenuAdditionalComponents: []
		};
	}

	addMainMenuAdditionalComponent = (component) => {

		this.setState({ mainMenuAdditionalComponents: [...this.state.mainMenuAdditionalComponents, component]});
	}

	removeMainMenuAdditionalComponent = (component) => {
		this.setState({ mainMenuAdditionalComponents: this.state.mainMenuAdditionalComponents.filter(c => c !== component) });
	}

	render() {
		let { path } = this.props.match;
		let { addMainMenuAdditionalComponent, removeMainMenuAdditionalComponent } = this;
		return (
			<div>
				<MainMenu 
					{...this.props} 
				>
					{this.state.mainMenuAdditionalComponents}
				</MainMenu>
				<Switch>
					<Route
						exact path={`${path}`}
						component={Main}
					/>
					<Route
						exact path={`${joinPaths(path, 'run')}`}
						component={RunDetection}
					/>
					<Route
						exact path={`${joinPaths(path, 'overview')}`}
						component={DetectionsOverview}
					/>
					<Route
						exact path={`${joinPaths(path, 'detection', ':id')}`}
						render={(props) => (
							<DetectionDetail 
								{...props}
								addNavigation={addMainMenuAdditionalComponent}
								removeNavigation={removeMainMenuAdditionalComponent}
							/>
						)}
					/>
				</Switch>
			</div>
		);
	}
}

export default MainRouter;