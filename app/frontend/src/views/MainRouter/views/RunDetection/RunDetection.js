import React, { Component } from 'react';
import { getSettings } from '../../../../services/helpers';
import { makeApiServiceProxyRequest } from '../../../../services/helpers';
import { Redirect } from 'react-router-dom';
import { toast } from 'react-toastify'
import BigLoadingCentered from '../../../../components/reusables/BigLoadingCentered'
import { FontAwesomeIcon as Icon } from '@fortawesome/react-fontawesome'
import { faPlay, faUpload } from '@fortawesome/free-solid-svg-icons'

class RunDetection extends Component {

	constructor(props) {
		super(props);
		this.state = {
			imagePreview: null,
			fileBlob: null,
			fileName: null,
			loading: false,
			detectionIdForRedirect: null
		};
		this.uploadInputRef = React.createRef();
	}

	handleImageChange = (e) => {
		const file = e.target.files[0];
		const reader = new FileReader();

		reader.onloadend = () => {
			this.setState({
				imagePreview: reader.result,
				fileName: file.name,
				fileBlob: file
			});
		};

		if (file) {
			reader.readAsDataURL(file);
		}
	};

	handleImageUploadClick = (e) => {
		e.preventDefault();
		this.uploadInputRef.current.click();
	}

	removeFile = () => {
		this.setState({imagePreview: null, fileName: null, fileBlob: null});
	}

	handleStartAnalysis = () => {
		let settings = getSettings();

		let body = new FormData();
		body.append('image', this.state?.fileBlob);
		body.append('boxes_count', settings?.boxesCount);
		body.append('score_threshold', settings?.scoreThreshold);

		this.setState({loading: true});
		makeApiServiceProxyRequest('detection/run', 'post', body, 
			(data) => {
				this.setState({ loading: false, detectionIdForRedirect: data?.id });
				toast.success(`Sucessfully executed animal detection`);
			},
			() => this.setState({loading: false})
		);
	};

	render() {
		const imageStyle = {
			height: '450px',
			borderRadius: '15px',
		};

		const imagePlaceholderStyle = {
			...imageStyle,
			width: '50%',
			border: '2px dashed #ccc',
			display: 'flex',
			justifyContent: 'center',
			alignItems: 'center',
			textAlign: 'center'
		}
		

		const { imagePreview, fileName, detectionIdForRedirect, loading } = this.state;
		return (
			<div className="container my-5">
				{detectionIdForRedirect && (<Redirect to={`/detection/${detectionIdForRedirect}`} />)}
				<div className="card">
					<div className="card-body">
						<div className='d-flex justify-content-center'>
							{imagePreview ? (
								loading ? 
									(
										<div style={imageStyle}>
											<BigLoadingCentered></BigLoadingCentered>
										</div>
									) : (
										<img 
											src={imagePreview}
											alt="Uploaded"
											className="img-fluid img-thumbnail"
											style={imageStyle}
										/>
									)
							) : (
								<div style={imagePlaceholderStyle}>
									<span>No image uploaded yet</span>
								</div>
							)}
						</div>
						<hr></hr>
						<div className='d-flex flex-wrap'>
							<div className="mr-auto">
								{imagePreview && (
									<button onClick={this.handleStartAnalysis} className="btn btn-primary btn-raised" disabled={loading}>
										<Icon icon={faPlay} size='sm'/> Start Analysis
									</button>
								)}
							</div>

							<div className='d-flex flex-wrap'>
								{fileName && (
									<div
										className="d-flex flex-nowrap justify-content-center mr-3 my-1 align-items-center px-2"
										style={{border: '1px solid lightgray', borderRadius: '7.5px'}}
									>
										<span className='mr-1'>{fileName}</span>
										<button
											onClick={this.removeFile}
											className="close"
											disabled={loading}
										>
											<span aria-hidden="true">&times;</span>
										</button>
									</div>
								)}

								<button onClick={this.handleImageUploadClick} className="btn btn-raised btn-info" disabled={loading}>
									<Icon icon={faUpload} size='sm'/> Upload image
								</button>
								
								<input
									onChange={this.handleImageChange}
									className="form-control btn"
									type="file"
									id="imageUpload"
									accept="image/*"
									style={{display: 'none'}}
									ref={this.uploadInputRef}
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default RunDetection