import React, { Component } from 'react';
import { toast } from 'react-toastify'
import { getSettings, setSettings } from '../../../services/helpers';

class Settings extends Component {
    constructor(props){
        super(props);
        const settings = getSettings();
        this.state = {scoreThreshold: settings?.scoreThreshold, boxesCount: settings?.boxesCount}
    }

    handleChange = (name) => (e) => {
        this.setState({
            [name]: e.target.value
        })
    }

    handleLeave = () => {
        this.props.hideModal();
    }

    componentWillUnmount() {
        this.handleLeave();
    }

    onSubmit = (e) => {
        e.preventDefault();
        setSettings(this.state.scoreThreshold, this.state.boxesCount);
        toast.success('Saved settings');
        this.handleLeave();
    }


    render() {
        let {scoreThreshold, boxesCount} = this.state;
        let isMobileWidth = (window.innerWidth <= 1000);
        let trStyle = {padding: '10px', alignItems: 'center'};
        let leftTdStyle = {padding: '10px'};
        let inputAlignRightStyle = {textAlign: 'right'}
        return (
            <div>
                <div
                    className="container text-center my-3 align-items-center"
                    style={{width: isMobileWidth ? '90%' : '90%'}}
                >
                    <table style={{margin: 'auto'}}>
                        <tbody>
                            <tr style={trStyle}>
                                <td style={leftTdStyle}>
                                    <label className="text-muted" htmlFor='scoreThresholdInput'>
                                        Score threshold for a detection
                                    </label>
                                </td>
                                <td>
                                    <input
                                        style={inputAlignRightStyle}
                                        id='scoreThresholdInput'
                                        onChange={this.handleChange("scoreThreshold")}
                                        type="number"
                                        step="0.001"
                                        min={0}
                                        max={1}
                                        className="form-control ml-2"
                                        value={scoreThreshold}
                                    />
                                </td>
                            </tr>
                            <tr style={trStyle}>
                                <td style={leftTdStyle}>
                                    <label className="text-muted" htmlFor='boxesCountInput'>
                                        Max amount of boxes to detect
                                    </label>
                                </td>
                                <td>
                                    <input 
                                        style={inputAlignRightStyle}
                                        id='boxesCountInput'
                                        onChange={this.handleChange("boxesCount")}
                                        type="number" 
                                        step="1"
                                        min={0}
                                        max={20}
                                        className="form-control ml-2"
                                        value={boxesCount}
                                    />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <hr></hr>
                    <button 
                        className="btn btn-outline btn-success btn-raised"
                        onClick={this.onSubmit}
                    >
                        Save
                    </button>
                </div>
            </div>
        )
    }
}

export default Settings