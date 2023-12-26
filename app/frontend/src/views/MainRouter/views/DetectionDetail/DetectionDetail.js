import React, { Component } from 'react';
import { getSettings } from '../../../../services/helpers';
import { makeApiServiceProxyRequest, getApiUrl } from '../../../../services/helpers';
import BigLoadingCentered from '../../../../components/reusables/BigLoadingCentered'
import { Redirect } from 'react-router-dom';
import { FontAwesomeIcon as Icon } from '@fortawesome/react-fontawesome'
import { faRedo, faTrash, faArrowLeft, faInfoCircle, faEye } from '@fortawesome/free-solid-svg-icons'
import ModalRoot from '../../../../components/ModalRoot';
import NavItem from '../../../../components/reusables/navbar/NavItem';
import DetectionMetadata from './DetectionMetadata';
import { toast } from 'react-toastify'
import DetectionObjectsList from './DetectionObjectsList';

class DetectionDetail extends Component {

	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			detectionData: null,
			redirectToOverview: false,
			showDeleteModal: false,
			showOriginalImageModal: false,
		};
	}

	get id() {
		return this.props?.match?.params?.id
	}

	get pathname() {
		return this.props?.location?.pathname;
	}

	componentDidMount() {
		this.loadData();

		this.navigationComponent = (
			<NavItem
				pageURI={this.pathname}
				path={`/detection/${this.id}`}
				name="Detection detail"
				key={-1}
			>
				<Icon icon={faEye} size='sm'/> Detection result {this.id}
			</NavItem>
		)

		this.props.addNavigation(this.navigationComponent);
	}

	componentWillUnmount() {
		this.props.removeNavigation(this.navigationComponent);
		this.navigationComponent = null;
	}

	loadData = () => {
		this.setState({loading: true});
		makeApiServiceProxyRequest(`detection/${this.id}`, 'get', undefined, 
			(data) => {
				this.setState({ loading: false, detectionData: data });
			},
			() => this.setState({loading: false})
		);
	};

	handleRerun = () => {
		let settings = getSettings();

		let body = {
			'boxes_count': settings?.boxesCount,
			'score_threshold': settings?.scoreThreshold
		}

		this.setState({loading: true});

		makeApiServiceProxyRequest(`detection/${this.id}/rerun`, 'put', JSON.stringify(body),
			(data) => {
				if (data?.success) {
					this.loadData();
					toast.success(`Sucessfully executed animal detection again`);
				}
			},
			() => this.setState({loading: false})
		);
	}

	handleDelete = () => {
		this.setState({loading: true});
		makeApiServiceProxyRequest(`detection/${this.id}`, 'delete', undefined,
			(data) => {
				if (data?.success) {
					this.setState({ redirectToOverview: true })
					toast.info(`Detection ${this.id} was deleted`);
				}
			},
			() => this.setState({loading: false})
		);
	}

	redirectToOverview = () => {
		this.setState({redirectToOverview: true});
	}

	showDeleteModal = (e) => {
		e.preventDefault();
		this.setState({showDeleteModal: true});
	}

	showOriginalImageModal = (e) => {
		e.preventDefault();
		this.setState({showOriginalImageModal: true});
	}

	hideModal = () => {
		this.setState({ showDeleteModal: false, showOriginalImageModal: false });
	}

	render() {
		const imageStyle = {
			height: '450px',
			borderRadius: '15px',
		};
		let isMobileWidth = (window.innerWidth <= 1000);
		
		const { loading, detectionData: data, redirectToOverview, showDeleteModal, showOriginalImageModal } = this.state;

		const showModal = showDeleteModal || showOriginalImageModal;
		let modalComponent = [];
		
		if (showOriginalImageModal) {
			modalComponent = (
				<div
                    className="container text-center my-3 align-items-center"
                    style={{width: isMobileWidth ? '90%' : '90%'}}
                >
					<img
						src={getApiUrl(`detection/${this.id}/image/original`)}
						alt="Original"
						className="img-fluid"
					/>
				</div>
			);
		} else if (showDeleteModal) {
			modalComponent = (
				<div
                    className="container text-center my-3 align-items-center"
                    style={{width: isMobileWidth ? '90%' : '90%'}}
                >
					<p>Are you sure that you want to delete this detection?</p>
					<div className='d-flex flex-nowrap'>
						<div className="ml-auto ml-3">
							<button onClick={this.hideModal} className="btn btn-raised mr-3" disabled={loading}>
								Cancel
							</button>
							<button onClick={this.handleDelete} className="btn btn-danger btn-raised" disabled={loading}>
								Yes, delete
							</button>
						</div>
					</div>
					{loading && (<BigLoadingCentered></BigLoadingCentered>)}
				</div>
			);
		}

		if (!data) {
			return (
				<BigLoadingCentered></BigLoadingCentered>
			);
		}

		return (
			<div className="container my-5">
				<ModalRoot show={showModal || showOriginalImageModal} hideModal={this.hideModal}>
					{showModal && modalComponent}
				</ModalRoot>
				{redirectToOverview && (<Redirect to={`/overview`} />)}
				<div className="card">
					<div className="card-body">
						<div className='d-flex flex-wrap mb-3'>
							<div className="mr-auto">
								<button onClick={this.redirectToOverview} className="btn btn-raised">
									<Icon icon={faArrowLeft} size='sm'/> Back to overview
								</button>
							</div>
							<div>
								<button onClick={this.showOriginalImageModal} className="btn btn-raised btn-info">
									<Icon icon={faInfoCircle} size='sm'/> Show Original image
								</button>
							</div>
						</div>
						<div className='d-flex justify-content-center'>
							{loading ? 
								(
									<div style={imageStyle}>
										<BigLoadingCentered></BigLoadingCentered>
									</div>
								) : (
									<img 
										src={getApiUrl(`detection/${this.id}/image/result?${new Date().getTime()}`)}
										alt="Result"
										className="img-fluid img-thumbnail"
										style={imageStyle}
									/>
								)
							}
						</div>
						<hr></hr>
						<div className="row my-3" style={{display: (data?.metadata && data?.objects) ? '' : 'none'}}>
							<div className="col-md-5 align-items-center">
								<div className='col-md-12'>
									<h3 className='text-center'>Metadata</h3>
									<div className="table-responsive-md">
										<DetectionMetadata metadata={data?.metadata ?? {}} />
									</div>
								</div>
							</div>
							<div className="col-md-7 align-items-center">
								<div className='col-md-12'>
									<h3 className='text-center'>Detected animals</h3>
									<div className="table-responsive-md">
										<DetectionObjectsList objects={data?.objects ?? []} />
									</div>
								</div>
							</div>
						</div>
						<hr></hr>
						<div className='d-flex flex-wrap'>
							<div className="mr-auto">
								<button onClick={this.handleRerun} className="btn btn-primary btn-raised" disabled={loading}>
									<Icon icon={faRedo} size='sm'/> Run analysis again
								</button>
							</div>

							<div className='d-flex justify-content-center'>
								<button onClick={this.showDeleteModal} className="btn btn-raised btn-danger" disabled={loading}>
									<Icon icon={faTrash} size='sm'/> Delete detection
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default DetectionDetail