import React, { Component } from 'react';
import Settings from '../../../components/Settings'
import { FontAwesomeIcon as Icon } from '@fortawesome/react-fontawesome'
import { faCog, faPaw, faPlay, faHistory } from '@fortawesome/free-solid-svg-icons'
import NavItem from "../../../../components/reusables/navbar/NavItem";
import ModalRoot from '../../../../components/ModalRoot/ModalRoot';
import './MainMenu.css';

class MainMenu extends Component {
	constructor(props){
		super(props);
		this.state = {
			display: false,
			settingsIconInFocus: false,
			showSettings: false,
			showBrandSeparator: true,
			hoveredBrand: true,
		}
	}

	toggleSettingsHover = (e) => {
		e.preventDefault();
		this.setState({settingsIconInFocus: !this.state.settingsIconInFocus});
	}

	showSettingsModal = () => {
		this.setState({showSettings: true});
	}

	hideSettingsModal = () => {
		this.setState({showSettings: false});
	}

	toggleNavbar = (e) => {
		e.preventDefault();
		this.setState({display: !this.state.display, showBrandSeparator: !this.state.showBrandSeparator});
	}
			
	render() {
		let { pathname } = this.props.location;
		let { display, showSettings, showBrandSeparator } = this.state;
		return (
			<nav className="navbar navbar-expand-lg navbar-light sticky-top" style={{backgroundColor: 'lightblue'}}>
				<ModalRoot show={showSettings} hideModal={this.hideSettingsModal}>
					{showSettings && (
						<Settings hideModal={this.hideSettingsModal}/>
					)}
				</ModalRoot>
				<button
					className="navbar-toggler"
					type="button"
					onClick={this.toggleNavbar}
				>
					<span className="navbar-toggler-icon" />
				</button>
				<div className={(display ? '' : 'collapse ') + "navbar-collapse"}>
					<NavItem 
						pageURI={pathname}
						path={pathname}
						brand
					>
						<div className='shake-on-hover'>
							<Icon icon={faPaw}/> Animal breed detector
						</div>
					</NavItem>
					{showBrandSeparator && (
						<div style={{'borderLeft': '1px solid gray', 'height': '40px'}}></div>
					)}
					<ul className="navbar-nav mr-auto ml-3">
						<NavItem
							pageURI={pathname}
							path="/run"
							name="Run new detection"
							key={-2}
						>
							<Icon icon={faPlay} size='sm'/> Run new detection
						</NavItem>
						<NavItem
							pageURI={pathname}
							path="/overview"
							name="History"
							key={-1}
						>
							<Icon icon={faHistory} size='sm'/> History
						</NavItem>
						{this.props.children}
					</ul>
					<ul className="navbar-nav">
						<NavItem
							pageURI={pathname}
							name="Settings"
							onClick={this.showSettingsModal}
							key={0}
						>
							<Icon icon={faCog} size='sm'/> Settings 
						</NavItem>
					</ul>
				</div>
			</nav>
		);
	}
}

export default MainMenu