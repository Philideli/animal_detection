import React, { Component } from 'react';

class DetectionObjectsList extends Component {

	render() {
		const { objects } = this.props;

		return (
			<table className="table table-hover table-info">
                <thead>
                    <tr key={'row-header'}>
                        <th scope="col">{'#'}</th>
                        <th scope="col">Species</th>
                        <th scope="col">Breed</th>
                        <th scope="col">Score</th>
                        <th scope="col">Coordinates</th>
                    </tr>
                </thead>
                <tbody>
                    {Array.isArray(objects) && objects.map((obj, i) => (
                        <tr key={`row-${i}`}>
                            <th scope="row">{i + 1}</th>
                            <td>{obj.species}</td>
                            <td>{obj.class}</td>
                            <td>{obj.score?.toFixed(3)}</td>
                            <td>
                                Top left: {`(${obj.coordinates?.start?.x?.toFixed(0)}, ${obj.coordinates?.start?.y?.toFixed(0)})`}
                                <br></br>
                                Bottom right: {`(${obj.coordinates?.end?.x?.toFixed(0)}, ${obj.coordinates?.end?.y?.toFixed(0)})`}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
		);
	}
}


export default DetectionObjectsList