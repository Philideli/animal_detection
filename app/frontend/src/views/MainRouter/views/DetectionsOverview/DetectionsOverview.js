import React, { Component } from 'react';
import { makeApiServiceProxyRequest } from '../../../../services/helpers';
import BigLoadingCentered from '../../../../components/reusables/BigLoadingCentered'
import Dropdown from 'react-bootstrap/Dropdown';
import { FontAwesomeIcon as Icon } from '@fortawesome/react-fontawesome'
import { faSearch, faList, faTrash } from '@fortawesome/free-solid-svg-icons'
import ModalRoot from '../../../../components/ModalRoot';
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom/cjs/react-router-dom.min';
import DetectionMetadata from '../DetectionDetail/DetectionMetadata';

class DetectionsOverview extends Component {

	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			detectionsData: null,
			showDeleteModal: false,
			detectionIdForModal: null,
			showPropertiesModal: false,
			propertiesForModal: null,
		};
	}

	componentDidMount() {
		this.loadData();
	}

	handleDelete = (id) => {
		this.setState({loading: true});
		makeApiServiceProxyRequest(`detection/${id}`, 'delete', undefined,
			(data) => {
				if (data?.success) {
					this.loadData(this.hideModal);
					toast.info(`Detection ${id} was deleted`);
				}
			},
			() => this.setState({loading: false})
		);
	}

	loadData = (callback) => {
		this.setState({loading: true});
		makeApiServiceProxyRequest(`detections/overview`, 'get', undefined, 
			(data) => {
				this.setState({ loading: false, detectionsData: data });
				if (callback) {
					callback();
				}
			},
			() => this.setState({loading: false})
		);
	};

	showDeleteModal = (id) => {
		this.setState({ showDeleteModal: true, detectionIdForModal: id });
	}

	showPropertiesModal = (properties, id) => {
		this.setState({ showPropertiesModal: true, propertiesForModal: properties, detectionIdForModal: id});
	}

	hideModal = () => {
		this.setState({ showDeleteModal: false, showPropertiesModal: false, detectionIdForModal: null, propertiesForModal: null });
	}

	render() {
		let isMobileWidth = (window.innerWidth <= 1000);
		const { loading, detectionsData: data, showDeleteModal, showPropertiesModal, detectionIdForModal, propertiesForModal } = this.state;

		const showModal = showDeleteModal || showPropertiesModal;
		let modalComponent = [];
		
		if (showPropertiesModal) {
			modalComponent = (
				<div
                    className="container text-center my-3 align-items-center"
                    style={{width: isMobileWidth ? '90%' : '90%'}}
                >
					<h4 className='text-center mb-4'>Metadata for detection with Id {detectionIdForModal}</h4>
					<div className="table-responsive-md">
						<DetectionMetadata metadata={propertiesForModal ?? {}}/>
					</div>
				</div>
			);
		} else if (showDeleteModal) {
			modalComponent = (
				<div
                    className="container text-center my-3 align-items-center"
                    style={{width: isMobileWidth ? '90%' : '90%'}}
                >
					<p>Are you sure that you want to delete the detection with Id {detectionIdForModal}?</p>
					<div className='d-flex flex-nowrap'>
						<div className="ml-auto ml-3">
							<button onClick={this.hideModal} className="btn btn-raised mr-3" disabled={loading}>
								Cancel
							</button>
							<button onClick={() => this.handleDelete(detectionIdForModal)} className="btn btn-danger btn-raised" disabled={loading}>
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

		const detections = data?.detections;

		const filenameStyle = {
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            maxWidth: '17em',
            overflow: 'hidden'
        }

		return (
			<div className="container my-5">
				<ModalRoot show={showModal} hideModal={this.hideModal}>
					{showModal && modalComponent}
				</ModalRoot>
				<div className="card">
					<div className="card-body">
						<h1 className='text-center mb-4'>Animal detections overview</h1>
						<div className="table-responsive-md">
							<table className="table table-hover table-light">
								<thead>
									<tr key={'row-header'}>
										<th scope="col">{'#'}</th>
										<th scope="col">File name</th>
										<th scope="col">Execution time</th>
										<th scope="col">Number of detected boxes</th>
										<th scope="col"></th>
									</tr>
								</thead>
								<tbody>
									{Array.isArray(detections) && detections.map((d, i) => (
										<tr key={`row-${i}`}>
											<th scope="row"><Link to={`/detection/${d.id}`}>{d.id}</Link></th>
											<td style={filenameStyle}><Link to={`/detection/${d.id}`}>{d?.metadata?.filename}</Link></td>
											<td>
												{new Date(d?.metadata?.timestamp * 1000).toLocaleDateString()}
												{' '}
												{new Date(d?.metadata?.timestamp * 1000).toLocaleTimeString()}
											</td>
											<td>{d?.objects?.length ?? 0}</td>
											<td>
												<Dropdown
													key={`row-button-${i}`}
													id={`dropdown-split-button-${i}`}
												>
													<Dropdown.Toggle variant="info">
														More
													</Dropdown.Toggle>
													<Dropdown.Menu>
														<Link className="dropdown-item d-flex flex-nowrap" to={`/detection/${d.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
															<Icon icon={faSearch} size='sm' className='mr-2'/> Open
														</Link>
														<Dropdown.Item className='d-flex flex-nowrap' onClick={() => this.showPropertiesModal(d?.metadata, d?.id)}>
															<Icon icon={faList} size='sm' className='mr-2'/> See metadata
														</Dropdown.Item>
														<Dropdown.Divider />
														<Dropdown.Item className='d-flex flex-nowrap' onClick={() => this.showDeleteModal(d?.id)}>
															<Icon icon={faTrash} size='sm' className='mr-2'/> Delete
														</Dropdown.Item>
													</Dropdown.Menu>
												</Dropdown>
											</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default DetectionsOverview