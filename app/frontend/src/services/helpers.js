import { REACT_APP_API_URL } from '../constants'
import { toast } from 'react-toastify'

export let getApiUrl = (path) => {
    return `${REACT_APP_API_URL}/${path}`;
}

export let makeApiServiceProxyRequest = (url, method, body, successCallback, errorCallback) => {
    fetch(getApiUrl(url), {
        method: method,
        body: body ?? undefined
    })
        .then((response) => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            return data;
        })
        .then(successCallback)
        .catch((error) => {
            errorCallback(error);
            toast.error(error.message ?? JSON.stringify(error));
            console.error(error);
        });
}

export let getSettings = () => {
    return JSON.parse(localStorage.getItem('detection_settings'));
}

export let setSettings = (scoreThreshold, boxesCount) => {
    localStorage.setItem('detection_settings', JSON.stringify({
        scoreThreshold: scoreThreshold,
        boxesCount: boxesCount
    }));
}

export let transitionStyles = {
    fade: {
        entering: {
            opacity: 0
        },
        entered: {
            opacity: 1,
            transition: 'all 150ms ease-in-out'
        },
        exiting: {
            opacity: 0,
            transition: 'all 150ms ease-in-out'
        },
        exited: {
            opacity: 1
        }
    },
    scaleDownBottom: {
        entering: {
            opacity: 0,
            transform: 'translateY(-10px) scale(0.7)',
        },
        entered: {
            opacity: 1
        },
        exiting: {
            opacity: 1,
            transform: 'scale(0.7) translateY(10px)'
        },
        exited: {
            opacity: 0
        },
    },
    scaleTop: {
        entering: {
            opacity: 1,
            transform: 'scaleY(0.4)',
            transformOrigin: '100% 0%',
            transitionDuration: '50ms'
        },
        entered: {
            opacity: 1,
            transform: 'scaleY(1)',
            transformOrigin: '100% 0%',
            transitionDuration: '50ms'
        },
        exiting: {
        },
        exited: {
        }
    },
    heightExpand: {
        entering: {
        },
        entered: {
            height: 'auto',
            overflow: 'visible'
        },
        exiting: {
            opacity: 0,
            transition: 'height 2s'
        },
        exited: {
            transition: 'height 2s',
            height: 0,
        }
    }
};