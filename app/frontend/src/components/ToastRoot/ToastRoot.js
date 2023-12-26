import React, { Component } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'
/*
 * Important for custom toasts
 */
toast.configure();
/**
 * Allows to display toast in left bottom corner.
 * There should only be one ToastRoot per app.
 *
 * @memberOf components.common
 * @component
 */
class ToastRoot extends Component {
    render() {
        return (
            <div>
                <ToastContainer
                    autoClose={3000}
                    position="bottom-left"
                />
            </div>
        );
    }
}

export default ToastRoot;
