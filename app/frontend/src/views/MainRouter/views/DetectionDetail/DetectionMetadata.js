import React, { Component } from 'react';

class DetectionMetadata extends Component {

	render() {
		const { metadata } = this.props;
        const filenameStyle = {
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            maxWidth: '2em',
            overflow: 'hidden'
        }

        const executionDateTime = new Date(metadata.timestamp * 1000);

		return (
			<table className="table table-hover table-secondary">
                <tbody>
                    <tr>
                        <th scope="row" className='col-md-6'>Image file name</th>
                        <td className='col-md-6' style={filenameStyle}>{metadata.filename}</td>
                    </tr>
                    <tr>
                        <th scope="row">Image height</th>
                        <td>{metadata.image_height}px</td>
                    </tr>
                    <tr>
                        <th scope="row">Image width</th>
                        <td>{metadata.image_width}px</td>
                    </tr>
                    <tr>
                        <th scope="row" >Max detected boxes</th>
                        <td>{metadata.boxes_count}</td>
                    </tr>
                    <tr>
                        <th scope="row">Score threshold</th>
                        <td>{metadata.score_threshold}</td>
                    </tr>
                    <tr>
                        <th scope="row">Execution time</th>
                        <td>{executionDateTime.toLocaleDateString()} {executionDateTime.toLocaleTimeString()}</td>
                    </tr>
                </tbody>
            </table>
		);
	}
}


export default DetectionMetadata