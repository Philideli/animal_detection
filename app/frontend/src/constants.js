export let REACT_APP_API_URL = (() => {
	switch(process.env.NODE_ENV){
		case 'production':
			return process.env.REACT_APP_API_URL || 'http://localhost:8000'
		case 'development':
			return process.env.REACT_APP_DEV_API_URL || 'http://localhost:8000'
		case 'test':
			return process.env.REACT_APP_TEST_API_URL || 'http://localhost:8000'
		default:
			return 'http://localhost:8000'
	}
})();